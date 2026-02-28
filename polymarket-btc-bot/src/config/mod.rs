use serde::{Deserialize, Serialize};
use config::{Config, ConfigError, Environment, File};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Settings {
    pub trading: TradingConfig,
    pub binance: BinanceConfig,
    pub polymarket: PolymarketConfig,
    pub pricing: PricingConfig,
    pub risk: RiskConfig,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TradingConfig {
    pub scan_interval_ms: u64,
    pub min_edge_threshold: f64,
    pub min_trade_size_usd: f64,
    pub risk_free_rate: f64,
    pub default_volatility: f64,
    pub max_open_positions: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BinanceConfig {
    pub websocket_url: String,
    pub api_key: Option<String>,
    pub api_secret: Option<String>,
    pub symbol: String,
    pub reconnect_interval_ms: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PolymarketConfig {
    pub api_url: String,
    pub gamma_api_url: String,
    pub ws_url: String,
    pub api_key: String,
    pub api_secret: String,
    pub passphrase: String,
    pub wallet_private_key: String,
    pub rpc_url: String,
    pub chain_id: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PricingConfig {
    pub use_implied_volatility: bool,
    pub volatility_lookback_hours: u64,
    pub volatility_update_interval_ms: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RiskConfig {
    pub kelly_fraction: f64,
    pub max_position_size_usd: f64,
    pub max_daily_loss_usd: f64,
    pub max_drawdown_percent: f64,
    pub correlation_threshold: f64,
    pub stop_loss_enabled: bool,
    pub stop_loss_percent: f64,
}

impl Settings {
    pub fn new() -> Result<Self, ConfigError> {
        let run_mode = std::env::var("RUN_MODE").unwrap_or_else(|_| "development".into());

        let s = Config::builder()
            // Start with default configuration
            .set_default("trading.scan_interval_ms", 100)?
            .set_default("trading.min_edge_threshold", 0.02)?
            .set_default("trading.min_trade_size_usd", 10.0)?
            .set_default("trading.risk_free_rate", 0.05)?
            .set_default("trading.default_volatility", 0.6)?
            .set_default("trading.max_open_positions", 10)?
            
            .set_default("binance.websocket_url", "wss://stream.binance.com:9443/ws/btcusdt@trade")?
            .set_default("binance.symbol", "BTCUSDT")?
            .set_default("binance.reconnect_interval_ms", 5000)?
            
            .set_default("polymarket.api_url", "https://clob.polymarket.com")?
            .set_default("polymarket.gamma_api_url", "https://gamma-api.polymarket.com")?
            .set_default("polymarket.ws_url", "wss://ws-sub.clob.polymarket.com/ws")?
            .set_default("polymarket.chain_id", 137)? // Polygon mainnet
            
            .set_default("pricing.use_implied_volatility", true)?
            .set_default("pricing.volatility_lookback_hours", 24)?
            .set_default("pricing.volatility_update_interval_ms", 60000)?
            
            .set_default("risk.kelly_fraction", 0.25)? // Quarter Kelly for safety
            .set_default("risk.max_position_size_usd", 1000.0)?
            .set_default("risk.max_daily_loss_usd", 5000.0)?
            .set_default("risk.max_drawdown_percent", 0.10)?
            .set_default("risk.correlation_threshold", 0.7)?
            .set_default("risk.stop_loss_enabled", true)?
            .set_default("risk.stop_loss_percent", 0.05)?
            
            // Add configuration from file
            .add_source(File::with_name(&format!("config/{}"
, run_mode)).required(false))
            .add_source(File::with_name("config/local").required(false))
            
            // Add environment variables (prefixed with BOT_)
            .add_source(Environment::with_prefix("BOT").separator("__"))
            
            .build()?;

        s.try_deserialize()
    }

    pub fn validate(&self) -> Result<(), ConfigError> {
        // Validate trading parameters
        if self.trading.min_edge_threshold <= 0.0 {
            return Err(ConfigError::Message(
                "min_edge_threshold must be positive".into()));
        }
        
        if self.trading.min_trade_size_usd < 1.0 {
            return Err(ConfigError::Message(
                "min_trade_size_usd must be at least $1".into()));
        }

        // Validate risk parameters
        if self.risk.kelly_fraction <= 0.0 || self.risk.kelly_fraction > 1.0 {
            return Err(ConfigError::Message(
                "kelly_fraction must be between 0 and 1".into()));
        }

        if self.risk.max_position_size_usd <= 0.0 {
            return Err(ConfigError::Message(
                "max_position_size_usd must be positive".into()));
        }

        // Validate Polymarket credentials are present
        if self.polymarket.api_key.is_empty() 
            || self.polymarket.api_secret.is_empty()
            || self.polymarket.wallet_private_key.is_empty() {
            return Err(ConfigError::Message(
                "Polymarket API credentials and wallet private key are required".into()));
        }

        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_default_config() {
        let config = Settings::new().unwrap();
        assert!(config.trading.min_edge_threshold > 0.0);
        assert!(config.risk.kelly_fraction > 0.0 && config.risk.kelly_fraction <= 1.0);
    }
}
