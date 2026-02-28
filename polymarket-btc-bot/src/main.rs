use std::sync::Arc;
use tokio::sync::{mpsc, RwLock};
use tokio::net::TcpListener;
use tracing::{info, error, warn};
use anyhow::Result;

mod config;
mod dashboard;
mod exchange;

use config::Settings;
use dashboard::{DashboardState, TradeRecord};
use exchange::binance::BinanceFeed;
use exchange::polymarket::PolymarketClient;

#[derive(Debug, Clone)]
pub struct TradeSignal {
    pub market_id: String,
    pub side: String,
    pub size: f64,
    pub expected_value: f64,
    pub edge: f64,
}

#[derive(Debug, Clone)]
pub struct MarketState {
    pub current_price: f64,
    pub timestamp: chrono::DateTime<chrono::Utc>,
}

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt()
        .with_env_filter(tracing_subscriber::EnvFilter::from_default_env())
        .init();

    info!("Polymarket BTC Trading Bot v0.1.0");

    let settings = Settings::new()?;
    info!("Configuration loaded");

    // Initialize exchange clients
    let polymarket_client = PolymarketClient::new(&settings.polymarket).await?;
    info!("Polymarket client connected");

    // Test getting markets
    match polymarket_client.get_active_btc_markets().await {
        Ok(markets) => info!("Found {} BTC markets", markets.len()),
        Err(e) => error!("Failed to get markets: {}", e),
    }

    // Initialize dashboard
    let dashboard_state = DashboardState::new();
    {
        let mut bot_config = dashboard_state.bot_config.write().await;
        bot_config.min_edge_threshold = settings.trading.min_edge_threshold;
        bot_config.kelly_fraction = settings.risk.kelly_fraction;
        bot_config.max_position_size = settings.risk.max_position_size_usd;
        bot_config.max_daily_loss = settings.risk.max_daily_loss_usd;
    }

    // Start dashboard server
    let app = dashboard::create_router(dashboard_state.clone());
    let listener = TcpListener::bind("0.0.0.0:8080").await?;
    info!("Dashboard at http://localhost:8080");

    let _dashboard_handle = tokio::spawn(async move {
        axum::serve(listener, app).await.unwrap();
    });

    // Start price feed from Binance
    let (price_tx, mut price_rx) = mpsc::channel::<f64>(100);
    let binance_feed = BinanceFeed::new(&settings.binance).await?;
    let _binance_handle = tokio::spawn(async move {
        if let Err(e) = binance_feed.run(price_tx).await {
            error!("Binance feed error: {}", e);
        }
    });

    // Price update loop
    let dashboard_state_price = dashboard_state.clone();
    let _price_updater = tokio::spawn(async move {
        while let Some(price) = price_rx.recv().await {
            let mut current_price = dashboard_state_price.current_price.write().await;
            *current_price = Some(price);
        }
    });

    // Main trading loop
    let mut interval = tokio::time::interval(
        tokio::time::Duration::from_millis(settings.trading.scan_interval_ms)
    );

    {
        let mut status = dashboard_state.bot_status.write().await;
        status.running = true;
    }

    loop {
        interval.tick().await;
        
        let is_running = {
            let status = dashboard_state.bot_status.read().await;
            status.running
        };

        if !is_running {
            continue;
        }

        // Get current price
        let current_price = {
            *dashboard_state.current_price.read().await
        };

        if current_price.is_none() {
            warn!("Waiting for price feed...");
            continue;
        }

        let price = current_price.unwrap();

        // Get markets and look for opportunities
        match polymarket_client.get_active_btc_markets().await {
            Ok(markets) => {
                info!("Found {} BTC markets", markets.len());
                for market in markets {
                    // Simple edge calculation
                    let fair_price = 0.5;
                    let market_price = market.best_yes_price;
                    let edge = (fair_price - market_price).abs();

                    let bot_config = dashboard_state.bot_config.read().await;
                    if edge > bot_config.min_edge_threshold {
                        info!("Found opportunity: {} with edge {:.2}%", market.id, edge * 100.0);
                        
                        // Execute trade
                        let outcome = if fair_price > market_price { "Yes" } else { "No" };
                        match polymarket_client.execute_trade(&market.id, outcome, 10.0).await {
                            Ok(order) => {
                                info!("Trade executed: {}", order.id);
                                
                                let trade = TradeRecord {
                                    id: order.id,
                                    timestamp: chrono::Utc::now(),
                                    market_id: market.id.clone(),
                                    side: outcome.to_string(),
                                    size: 10.0,
                                    price: order.price,
                                    expected_value: edge * 10.0,
                                    edge,
                                    pnl: None,
                                    status: "FILLED".to_string(),
                                };
                                
                                let mut trades = dashboard_state.trade_history.write().await;
                                trades.push(trade);
                                
                                let mut metrics = dashboard_state.performance_metrics.write().await;
                                metrics.total_trades += 1;
                                
                                let mut status = dashboard_state.bot_status.write().await;
                                status.last_trade_time = Some(chrono::Utc::now());
                                status.open_positions += 1;
                            }
                            Err(e) => {
                                error!("Trade failed: {}", e);
                                let mut status = dashboard_state.bot_status.write().await;
                                status.errors_count += 1;
                            }
                        }
                    }
                }
            }
            Err(e) => {
                error!("Failed to get markets: {:?}", e);
            }
        }

        {
            let mut status = dashboard_state.bot_status.write().await;
            status.uptime_seconds += settings.trading.scan_interval_ms / 1000;
        }
    }
}
