//! Polymarket Builder API Client
//! 
//! Uses the Polymarket CLOB (Central Limit Order Book) API for trading.
//! Authentication requires API key, secret, and passphrase.

use serde::{Deserialize, Serialize};
use std::time::{SystemTime, UNIX_EPOCH};
use tracing::{debug, info, warn};
use anyhow::{Result, Context};
use hmac::{Hmac, Mac};
use sha2::Sha256;

use crate::config::PolymarketConfig;

// Type alias for HMAC-SHA256
type HmacSha256 = Hmac<Sha256>;

/// Market information from Polymarket
#[derive(Debug, Clone, Deserialize)]
pub struct MarketInfo {
    pub id: String,
    pub condition_id: String,
    pub question: String,
    pub description: String,
    pub category: String,
    pub active: bool,
    pub closed: bool,
    pub archived: bool,
    #[serde(rename = "accepting_orders")]
    pub accepting_orders: bool,
    #[serde(rename = "minimum_order_size")]
    pub minimum_order_size: f64,
    #[serde(rename = "minimum_tick_size")]
    pub minimum_tick_size: f64,
    pub outcomes: Vec<String>,
    #[serde(rename = "outcomePrices")]
    pub outcome_prices: Vec<String>,
    #[serde(default)]
    pub strike_price: f64,
    #[serde(default)]
    pub time_to_expiry: f64,
    #[serde(default)]
    pub best_yes_price: f64,
    #[serde(default)]
    pub best_no_price: f64,
    #[serde(default)]
    pub yes_ask: f64,
    #[serde(default)]
    pub yes_bid: f64,
    #[serde(default)]
    pub no_ask: f64,
    #[serde(default)]
    pub no_bid: f64,
    #[serde(default)]
    pub volume: f64,
    #[serde(default)]
    pub liquidity: f64,
}

/// Order information
#[derive(Debug, Clone, Deserialize)]
pub struct OrderInfo {
    pub id: String,
    #[serde(rename = "marketId")]
    pub market_id: String,
    pub side: String,
    pub size: f64,
    pub price: f64,
    pub status: OrderStatus,
    #[serde(rename = "createdAt")]
    pub created_at: String,
}

#[derive(Debug, Clone, Deserialize)]
#[serde(rename_all = "UPPERCASE")]
pub enum OrderStatus {
    Pending,
    Open,
    Filled,
    Partial,
    Cancelled,
    Rejected,
}

/// Order book data
#[derive(Debug, Clone, Deserialize)]
pub struct OrderBook {
    #[serde(rename = "marketId")]
    pub market_id: String,
    pub bids: Vec<PriceLevel>,
    pub asks: Vec<PriceLevel>,
    pub timestamp: Option<u64>,
}

#[derive(Debug, Clone, Deserialize)]
pub struct PriceLevel {
    pub price: String,
    pub size: String,
}

/// Polymarket API client with Builder API authentication
pub struct PolymarketClient {
    config: PolymarketConfig,
    http_client: reqwest::Client,
}

/// Order request for creating new orders
#[derive(Debug, Clone, Serialize)]
struct CreateOrderRequest {
    #[serde(rename = "marketId")]
    market_id: String,
    #[serde(rename = "outcome")]
    outcome: String,
    #[serde(rename = "side")]
    side: String,
    #[serde(rename = "price")]
    price: String,
    #[serde(rename = "size")]
    size: String,
}

impl PolymarketClient {
    pub async fn new(config: &PolymarketConfig) -> Result<Self> {
        let http_client = reqwest::Client::builder()
            .timeout(std::time::Duration::from_secs(30))
            .build()
            .context("Failed to create HTTP client")?;

        let client = Self {
            config: config.clone(),
            http_client,
        };

        // Test connection
        match client.get_health().await {
            Ok(()) => info!("Polymarket Builder API client initialized successfully"),
            Err(e) => warn!("Polymarket health check failed: {}", e),
        }

        Ok(client)
    }

    /// Generate authentication headers for Builder API
    fn generate_auth_headers(
        &self,
        method: &str,
        endpoint: &str,
        body: Option<&str>,
    ) -> Result<Vec<(&'static str, String)>> {
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)?
            .as_millis()
            .to_string();

        // Create message to sign: timestamp + method + endpoint + body
        let message = format!(
            "{}{}{}{}",
            timestamp,
            method.to_uppercase(),
            endpoint,
            body.unwrap_or("")
        );

        // Create HMAC-SHA256 signature
        let mut mac = HmacSha256::new_from_slice(self.config.api_secret.as_bytes())
            .map_err(|e| anyhow::anyhow!("Invalid API secret: {}", e))?;
        mac.update(message.as_bytes());
        let signature = hex::encode(mac.finalize().into_bytes());

        Ok(vec![
            ("POLYMARKET-API-KEY", self.config.api_key.clone()),
            ("POLYMARKET-SIGNATURE", signature),
            ("POLYMARKET-TIMESTAMP", timestamp),
            ("POLYMARKET-PASSPHRASE", self.config.passphrase.clone()),
        ])
    }

    /// Check API health
    async fn get_health(&self) -> Result<()> {
        let url = format!("{}/health", self.config.api_url);

        let response = self.http_client
            .get(&url)
            .send()
            .await
            .context("Health check request failed")?;

        if response.status().is_success() {
            Ok(())
        } else {
            Err(anyhow::anyhow!("Health check failed: {}", response.status()))
        }
    }

    /// Get active BTC 5-minute markets by querying specific slugs
    pub async fn get_active_btc_markets(&self) -> Result<Vec<MarketInfo>> {
        let mut btc_markets = Vec::new();
        
        // Generate potential BTC up/down market slugs for the next few time windows
        // Each market is 5 minutes, so we check current time and next few windows
        let current_ts = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs() as i64;
        
        // Round to nearest 5-minute boundary and check several windows
        let base_ts = (current_ts / 300) * 300; // 300 seconds = 5 minutes
        
        // Check current and next 5 time windows (25 minutes of markets)
        for i in 0..6 {
            let ts = base_ts + (i * 300);
            let slug = format!("btc-updown-5m-{}", ts);
            
            match self.get_market_by_slug(&slug).await {
                Ok(market) => {
                    if market.active && !market.closed {
                        info!("Found active BTC market: {} (slug: {})", market.question, slug);
                        btc_markets.push(market);
                    }
                }
                Err(_) => {
                    // Market doesn't exist or error, continue to next
                    debug!("Market not found for slug: {}", slug);
                }
            }
        }
        
        // Also try the general markets endpoint as fallback (Gamma API)
        let url = format!("{}/markets", self.config.gamma_api_url);

        if let Ok(response) = self.http_client.get(&url).send().await {
            if response.status().is_success() {
                if let Ok(json) = response.json::<serde_json::Value>().await {
                    // Extract data array - API returns either { data: [...] } or direct array
                    let data = if let Some(arr) = json.as_array() {
                        arr.clone()
                    } else if let Some(arr) = json.get("data").and_then(|d| d.as_array()) {
                        arr.clone()
                    } else {
                        Vec::new()
                    };

                    for market in data {
                        let question = market.get("question")
                            .and_then(|q| q.as_str())
                            .unwrap_or("");
                        
                        // Filter for BTC 5-minute markets
                        let q_lower = question.to_lowercase();
                        let is_btc = q_lower.contains("bitcoin") || q_lower.contains("btc");
                        let is_5min = q_lower.contains("5 minute") || q_lower.contains("5-minute") || 
                                      q_lower.contains("up or down") || q_lower.contains("up/down");
                        
                        if is_btc && is_5min {
                            if let Ok(market_info) = self.parse_market_info(&market) {
                                // Avoid duplicates
                                if !btc_markets.iter().any(|m: &MarketInfo| m.condition_id == market_info.condition_id) {
                                    btc_markets.push(market_info);
                                }
                            }
                        }
                    }
                }
            }
        }

        info!("Found {} active BTC 5-minute markets", btc_markets.len());
        Ok(btc_markets)
    }
    
    /// Get market by slug using Gamma API (no auth required)
    async fn get_market_by_slug(&self, slug: &str) -> Result<MarketInfo> {
        // Use Gamma API for market discovery (public, no auth needed)
        let url = format!("{}/markets?slug={}", self.config.gamma_api_url, slug);

        let response = self.http_client
            .get(&url)
            .send()
            .await
            .context("Failed to fetch market by slug from Gamma API")?;

        if !response.status().is_success() {
            return Err(anyhow::anyhow!("Market not found: {}", slug));
        }

        let json: serde_json::Value = response.json().await
            .context("Failed to parse market response")?;
        
        // Response is an array with one market
        let market = json.get(0)
            .ok_or_else(|| anyhow::anyhow!("Empty market response"))?;
        
        self.parse_market_info(market)
    }
    
    /// Parse market info from JSON
    fn parse_market_info(&self, market: &serde_json::Value) -> Result<MarketInfo> {
        let question = market.get("question")
            .and_then(|q| q.as_str())
            .unwrap_or("");
        
        let id = market.get("condition_id")
            .and_then(|i| i.as_str())
            .unwrap_or("")
            .to_string();
        
        let active = market.get("active")
            .and_then(|a| a.as_bool())
            .unwrap_or(false);
        
        let closed = market.get("closed")
            .and_then(|c| c.as_bool())
            .unwrap_or(false);
        
        // Get prices from outcomePrices or tokens
        let mut best_yes_price = 0.0;
        let mut best_no_price = 0.0;
        
        // Try outcomePrices first
        if let Some(prices) = market.get("outcomePrices").and_then(|p| p.as_array()) {
            if prices.len() >= 2 {
                best_yes_price = prices[0].as_str().and_then(|s| s.parse().ok()).unwrap_or(0.0);
                best_no_price = prices[1].as_str().and_then(|s| s.parse().ok()).unwrap_or(0.0);
            }
        }
        
        // Fallback to tokens
        if best_yes_price == 0.0 && best_no_price == 0.0 {
            if let Some(tokens) = market.get("tokens").and_then(|t| t.as_array()) {
                for (i, token) in tokens.iter().enumerate() {
                    if let Some(price) = token.get("price").and_then(|p| p.as_f64()) {
                        if i == 0 {
                            best_yes_price = price;
                        } else if i == 1 {
                            best_no_price = price;
                        }
                    }
                }
            }
        }
        
        Ok(MarketInfo {
            id: id.clone(),
            condition_id: market.get("condition_id")
                .and_then(|c| c.as_str())
                .unwrap_or("")
                .to_string(),
            question: question.to_string(),
            description: market.get("description")
                .and_then(|d| d.as_str())
                .unwrap_or("")
                .to_string(),
            category: market.get("category")
                .and_then(|c| c.as_str())
                .unwrap_or("")
                .to_string(),
            active,
            closed,
            archived: market.get("archived")
                .and_then(|a| a.as_bool())
                .unwrap_or(false),
            accepting_orders: market.get("accepting_orders")
                .and_then(|a| a.as_bool())
                .unwrap_or(false),
            minimum_order_size: market.get("minimum_order_size")
                .and_then(|m| m.as_f64())
                .unwrap_or(0.0),
            minimum_tick_size: market.get("minimum_tick_size")
                .and_then(|m| m.as_f64())
                .unwrap_or(0.0),
            outcomes: Vec::new(),
            outcome_prices: Vec::new(),
            strike_price: 0.0,
            time_to_expiry: 0.0,
            best_yes_price,
            best_no_price,
            yes_ask: 0.0,
            yes_bid: 0.0,
            no_ask: 0.0,
            no_bid: 0.0,
            volume: 0.0,
            liquidity: 0.0,
        })
    }

    /// Get market by ID
    pub async fn get_market(&self, market_id: &str) -> Result<MarketInfo> {
        let endpoint = format!("/markets/{}", market_id);
        let url = format!("{}{}", self.config.api_url, endpoint);

        let headers = self.generate_auth_headers("GET", &endpoint, None)?;

        let mut request = self.http_client.get(&url);
        for (key, value) in headers {
            request = request.header(key, value);
        }

        let response = request
            .send()
            .await
            .context("Failed to fetch market")?;

        if !response.status().is_success() {
            return Err(anyhow::anyhow!("Market not found: {}", market_id));
        }

        let mut market: MarketInfo = response.json().await
            .context("Failed to parse market response")?;

        // Parse outcome prices
        if let (Some(yes_price), Some(no_price)) = (
            market.outcome_prices.get(0).and_then(|p| p.parse().ok()),
            market.outcome_prices.get(1).and_then(|p| p.parse().ok())
        ) {
            market.best_yes_price = yes_price;
            market.best_no_price = no_price;
        }

        Ok(market)
    }

    /// Get order book for a market
    pub async fn get_order_book(&self, market_id: &str) -> Result<OrderBook> {
        let endpoint = format!("/books/{}", market_id);
        let url = format!("{}{}", self.config.api_url, endpoint);

        let headers = self.generate_auth_headers("GET", &endpoint, None)?;

        let mut request = self.http_client.get(&url);
        for (key, value) in headers {
            request = request.header(key, value);
        }

        let response = request
            .send()
            .await
            .context("Failed to fetch order book")?;

        if !response.status().is_success() {
            return Err(anyhow::anyhow!("Order book not found: {}", market_id));
        }

        let order_book: OrderBook = response.json().await
            .context("Failed to parse order book response")?;

        Ok(order_book)
    }

    /// Execute a trade
    pub async fn execute_trade(
        &self,
        market_id: &str,
        outcome: &str,
        size: f64,
    ) -> Result<OrderInfo> {
        info!(
            "Executing trade: Market={}, Outcome={}, Size=${:.2}",
            market_id, outcome, size
        );

        self.place_order(
            market_id,
            outcome,
            "BUY",
            0.5, // Default price
            size,
        ).await
    }

    /// Place an order on Polymarket
    async fn place_order(
        &self,
        market_id: &str,
        outcome: &str,
        side: &str,
        price: f64,
        size: f64,
    ) -> Result<OrderInfo> {
        let endpoint = "/orders";
        let url = format!("{}{}", self.config.api_url, endpoint);

        let request = CreateOrderRequest {
            market_id: market_id.to_string(),
            outcome: outcome.to_string(),
            side: side.to_string(),
            price: format!("{:.4}", price),
            size: format!("{:.4}", size),
        };

        let body = serde_json::to_string(&request)?;
        let headers = self.generate_auth_headers("POST", endpoint, Some(&body))?;

        debug!("Placing order: {:?}", request);

        let mut req_builder = self.http_client.post(&url);
        for (key, value) in headers {
            req_builder = req_builder.header(key, value);
        }

        let response = req_builder
            .json(&request)
            .send()
            .await
            .context("Failed to submit order")?;

        if !response.status().is_success() {
            let status = response.status();
            let text = response.text().await.unwrap_or_default();
            return Err(anyhow::anyhow!("Order submission failed {}: {}", status, text));
        }

        let order: OrderInfo = response.json().await
            .context("Failed to parse order response")?;

        info!("Order submitted successfully: ID={}", order.id);
        Ok(order)
    }

    /// Get available USDC balance
    pub async fn get_available_balance(&self) -> Result<f64> {
        let endpoint = "/balance";
        let url = format!("{}{}", self.config.api_url, endpoint);

        let headers = self.generate_auth_headers("GET", endpoint, None)?;

        let mut request = self.http_client.get(&url);
        for (key, value) in headers {
            request = request.header(key, value);
        }

        let response = request
            .send()
            .await
            .context("Failed to fetch balance")?;

        if !response.status().is_success() {
            return Err(anyhow::anyhow!("Failed to get balance: {}", response.status()));
        }

        #[derive(Deserialize)]
        struct BalanceResponse {
            #[serde(rename = "availableBalance")]
            available_balance: String,
        }

        let data: BalanceResponse = response.json().await
            .context("Failed to parse balance response")?;

        data.available_balance.parse::<f64>()
            .context("Failed to parse balance as float")
    }

    /// Cancel an order
    pub async fn cancel_order(&self, order_id: &str) -> Result<()> {
        let endpoint = format!("/orders/{}", order_id);
        let url = format!("{}{}", self.config.api_url, endpoint);

        let headers = self.generate_auth_headers("DELETE", &endpoint, None)?;

        let mut request = self.http_client.delete(&url);
        for (key, value) in headers {
            request = request.header(key, value);
        }

        let response = request
            .send()
            .await
            .context("Failed to cancel order")?;

        if response.status().is_success() {
            info!("Order {} cancelled successfully", order_id);
            Ok(())
        } else {
            Err(anyhow::anyhow!("Failed to cancel order: {}", response.status()))
        }
    }

    /// Get open orders
    pub async fn get_open_orders(&self) -> Result<Vec<OrderInfo>> {
        let endpoint = "/orders?status=OPEN";
        let url = format!("{}{}", self.config.api_url, endpoint);

        let headers = self.generate_auth_headers("GET", endpoint, None)?;

        let mut request = self.http_client.get(&url);
        for (key, value) in headers {
            request = request.header(key, value);
        }

        let response = request
            .send()
            .await
            .context("Failed to fetch open orders")?;

        if !response.status().is_success() {
            return Err(anyhow::anyhow!("Failed to get open orders: {}", response.status()));
        }

        let orders: Vec<OrderInfo> = response.json().await
            .context("Failed to parse orders response")?;

        Ok(orders)
    }
}

impl Clone for PolymarketClient {
    fn clone(&self) -> Self {
        Self {
            config: self.config.clone(),
            http_client: self.http_client.clone(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_market_parsing() {
        let json = r#"{
            "id": "test-market",
            "conditionId": "cond-123",
            "question": "Will Bitcoin be above $50,000 in 5 minutes?",
            "description": "Test market",
            "category": "Crypto",
            "active": true,
            "closed": false,
            "outcomes": ["Yes", "No"],
            "outcomePrices": ["0.55", "0.45"]
        }"#;

        let market: MarketInfo = serde_json::from_str(json).expect("Failed to parse");
        assert_eq!(market.id, "test-market");
        assert!(market.active);
    }
}
