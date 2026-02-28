//! Binance WebSocket price feed for real-time BTC price discovery

use futures::{SinkExt, StreamExt};
use serde::Deserialize;
use std::sync::Arc;
use tokio::sync::RwLock;
use tokio::time::{interval, Duration};
use tokio_tungstenite::{connect_async, MaybeTlsStream, WebSocketStream};
use tracing::{debug, error, info, trace, warn};
use anyhow::{Result, Context};

use crate::config::BinanceConfig;

/// Binance trade message from WebSocket
#[derive(Debug, Clone, Deserialize)]
struct TradeMessage {
    #[serde(rename = "e")]
    event_type: String,
    #[serde(rename = "E")]
    event_time: u64,
    #[serde(rename = "s")]
    symbol: String,
    #[serde(rename = "p")]
    price: String,
    #[serde(rename = "q")]
    quantity: String,
}

/// Binance WebSocket feed handler
pub struct BinanceFeed {
    config: BinanceConfig,
}

impl BinanceFeed {
    pub async fn new(config: &BinanceConfig) -> Result<Self> {
        Ok(Self {
            config: config.clone(),
        })
    }

    /// Run the WebSocket feed
    pub async fn run(
        self,
        price_tx: tokio::sync::mpsc::Sender<f64>,
    ) -> Result<()> {
        info!("Starting Binance WebSocket feed for {}", self.config.symbol);

        let mut reconnect_interval = interval(Duration::from_millis(self.config.reconnect_interval_ms));

        loop {
            reconnect_interval.tick().await;

            match self.connect_and_stream(&price_tx).await {
                Ok(()) => {
                    info!("WebSocket stream ended normally");
                }
                Err(e) => {
                    error!("WebSocket error: {}. Reconnecting...", e);
                }
            }

            tokio::time::sleep(Duration::from_millis(self.config.reconnect_interval_ms)).await;
        }
    }

    async fn connect_and_stream(
        &self,
        price_tx: &tokio::sync::mpsc::Sender<f64>,
    ) -> Result<()> {
        let url = url::Url::parse(&self.config.websocket_url)
            .context("Failed to parse WebSocket URL")?;

        info!("Connecting to Binance WebSocket...");
        let (ws_stream, _) = connect_async(url).await
            .context("Failed to connect to Binance WebSocket")?;
        
        info!("Connected to Binance WebSocket");

        let (_, mut read) = ws_stream.split();

        while let Some(msg) = read.next().await {
            match msg {
                Ok(tokio_tungstenite::tungstenite::Message::Text(text)) => {
                    if let Ok(trade) = serde_json::from_str::<TradeMessage>(&text) {
                        if trade.event_type == "trade" {
                            if let Ok(price) = trade.price.parse::<f64>() {
                                let _ = price_tx.send(price).await;
                                debug!("BTC Price: ${:.2}", price);
                            }
                        }
                    }
                }
                Ok(tokio_tungstenite::tungstenite::Message::Ping(data)) => {
                    // Pong response would go here if we had the sink
                }
                Ok(tokio_tungstenite::tungstenite::Message::Close(_)) => {
                    info!("WebSocket closed by server");
                    break;
                }
                Err(e) => {
                    return Err(e.into());
                }
                _ => {}
            }
        }

        Ok(())
    }
}
