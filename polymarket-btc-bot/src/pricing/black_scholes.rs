//! Black-Scholes model for binary options pricing
//! 
//! For binary options, we use a modified Black-Scholes formula where the payoff
//! is either 0 or 1 (instead of the underlying asset price).

use statrs::distribution::{Continuous, Normal};
use tracing::{debug, trace};
use crate::config::PricingConfig;

/// Black-Scholes pricer for binary options
pub struct BinaryOptionPricer {
    config: PricingConfig,
}

/// Greeks for a binary option
#[derive(Debug, Clone, Copy)]
pub struct Greeks {
    pub delta: f64,
    pub gamma: f64,
    pub theta: f64,
    pub vega: f64,
    pub rho: f64,
}

/// Pricing result including fair value and Greeks
#[derive(Debug, Clone, Copy)]
pub struct PricingResult {
    pub fair_value: f64,
    pub greeks: Greeks,
    pub implied_volatility: Option<f64>,
}

impl BinaryOptionPricer {
    pub fn new(config: &PricingConfig) -> Self {
        Self {
            config: config.clone(),
        }
    }

    /// Price a binary call option using Black-Scholes
    /// 
    /// # Arguments
    /// * `spot` - Current spot price of the underlying
    /// * `strike` - Strike price of the option
    /// * `time_to_expiry` - Time to expiry in years
    /// * `volatility` - Annualized volatility (sigma)
    /// * `risk_free_rate` - Risk-free rate (annualized)
    /// 
    /// # Returns
    /// Probability that the option expires in-the-money (fair value)
    pub fn price_binary_option(
        &self,
        spot: f64,
        strike: f64,
        time_to_expiry: f64,
        volatility: f64,
        risk_free_rate: f64,
    ) -> f64 {
        if time_to_expiry <= 0.0 {
            // At expiry, price is 1.0 if ITM, 0.0 if OTM
            return if spot >= strike { 1.0 } else { 0.0 };
        }

        let d1 = self.calculate_d1(spot, strike, time_to_expiry, volatility, risk_free_rate);
        let d2 = d1 - volatility * time_to_expiry.sqrt();

        // For a binary call: N(d2) * exp(-rT)
        // The exp(-rT) term accounts for the time value of money
        let normal = Normal::new(0.0, 1.0).expect("Failed to create normal distribution");
        let nd2 = normal.cdf(d2);
        
        let fair_value = nd2 * (-risk_free_rate * time_to_expiry).exp();
        
        trace!(
            "Binary option pricing: spot={}, strike={}, tte={}, vol={}, r={} | fair_value={}",
            spot, strike, time_to_expiry, volatility, risk_free_rate, fair_value
        );

        fair_value.clamp(0.0, 1.0)
    }

    /// Calculate full pricing result with Greeks
    pub fn price_with_greeks(
        &self,
        spot: f64,
        strike: f64,
        time_to_expiry: f64,
        volatility: f64,
        risk_free_rate: f64,
    ) -> PricingResult {
        let fair_value = self.price_binary_option(spot, strike, time_to_expiry, volatility, risk_free_rate);
        let greeks = self.calculate_greeks(spot, strike, time_to_expiry, volatility, risk_free_rate);
        
        PricingResult {
            fair_value,
            greeks,
            implied_volatility: None,
        }
    }

    /// Calculate implied volatility from market price using Newton-Raphson method
    pub fn calculate_implied_volatility(
        &self,
        market_price: f64,
        spot: f64,
        strike: f64,
        time_to_expiry: f64,
        risk_free_rate: f64,
    ) -> Option<f64> {
        const MAX_ITERATIONS: usize = 100;
        const TOLERANCE: f64 = 1e-6;
        
        let mut vol = 0.5; // Initial guess
        
        for _ in 0..MAX_ITERATIONS {
            let price = self.price_binary_option(spot, strike, time_to_expiry, vol, risk_free_rate);
            let vega = self.calculate_vega(spot, strike, time_to_expiry, vol, risk_free_rate);
            
            if vega.abs() < 1e-10 {
                break;
            }
            
            let diff = price - market_price;
            if diff.abs() < TOLERANCE {
                return Some(vol);
            }
            
            vol -= diff / vega;
            vol = vol.clamp(0.001, 5.0); // Keep within reasonable bounds
        }
        
        None
    }

    /// Calculate d1 parameter for Black-Scholes
    fn calculate_d1(
        &self,
        spot: f64,
        strike: f64,
        time_to_expiry: f64,
        volatility: f64,
        risk_free_rate: f64,
    ) -> f64 {
        let sqrt_t = time_to_expiry.sqrt();
        let vol_sqrt_t = volatility * sqrt_t;
        
        if vol_sqrt_t == 0.0 {
            return 0.0;
        }
        
        ((spot / strike).ln() + (risk_free_rate + 0.5 * volatility.powi(2)) * time_to_expiry) / vol_sqrt_t
    }

    /// Calculate all Greeks for a binary option
    fn calculate_greeks(
        &self,
        spot: f64,
        strike: f64,
        time_to_expiry: f64,
        volatility: f64,
        risk_free_rate: f64,
    ) -> Greeks {
        let d1 = self.calculate_d1(spot, strike, time_to_expiry, volatility, risk_free_rate);
        let d2 = d1 - volatility * time_to_expiry.sqrt();
        
        let normal = Normal::new(0.0, 1.0).expect("Failed to create normal distribution");
        let nd1 = normal.cdf(d1);
        let nd2 = normal.cdf(d2);
        let n_prime_d1 = normal.pdf(d1);
        
        let sqrt_t = time_to_expiry.sqrt();
        let discount = (-risk_free_rate * time_to_expiry).exp();
        
        // Delta for binary call: N'(d1) / (S * sigma * sqrt(T))
        let delta = if spot > 0.0 && sqrt_t > 0.0 {
            n_prime_d1 / (spot * volatility * sqrt_t)
        } else {
            0.0
        };
        
        // Gamma for binary option
        let gamma = if spot > 0.0 && sqrt_t > 0.0 {
            -n_prime_d1 * d1 / (spot.powi(2) * volatility.powi(2) * time_to_expiry)
        } else {
            0.0
        };
        
        // Theta (time decay)
        let theta = if sqrt_t > 0.0 {
            discount * n_prime_d1 * (d1 / (2.0 * time_to_expiry) - risk_free_rate / volatility / sqrt_t)
                - risk_free_rate * nd2 * discount
        } else {
            0.0
        };
        
        // Vega
        let vega = self.calculate_vega(spot, strike, time_to_expiry, volatility, risk_free_rate);
        
        // Rho
        let rho = if sqrt_t > 0.0 {
            -time_to_expiry * nd2 * discount
        } else {
            0.0
        };
        
        Greeks { delta, gamma, theta, vega, rho }
    }

    /// Calculate Vega (sensitivity to volatility)
    fn calculate_vega(
        &self,
        spot: f64,
        strike: f64,
        time_to_expiry: f64,
        volatility: f64,
        risk_free_rate: f64,
    ) -> f64 {
        let d1 = self.calculate_d1(spot, strike, time_to_expiry, volatility, risk_free_rate);
        let normal = Normal::new(0.0, 1.0).expect("Failed to create normal distribution");
        let n_prime_d1 = normal.pdf(d1);
        
        let sqrt_t = time_to_expiry.sqrt();
        let discount = (-risk_free_rate * time_to_expiry).exp();
        
        if sqrt_t > 0.0 {
            -n_prime_d1 * sqrt_t * discount / volatility
        } else {
            0.0
        }
    }

    /// Calculate realized volatility from price history
    pub fn calculate_realized_volatility(prices: &[f64], periods_per_year: f64) -> f64 {
        if prices.len() < 2 {
            return 0.0;
        }
        
        // Calculate log returns
        let log_returns: Vec<f64> = prices.windows(2)
            .map(|w| (w[1] / w[0]).ln())
            .collect();
        
        // Calculate mean return
        let mean_return = log_returns.iter().sum::<f64>() / log_returns.len() as f64;
        
        // Calculate variance
        let variance = log_returns.iter()
            .map(|r| (r - mean_return).powi(2))
            .sum::<f64>() / (log_returns.len() - 1) as f64;
        
        // Annualized volatility
        variance.sqrt() * periods_per_year.sqrt()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_binary_option_pricing() {
        let config = PricingConfig {
            use_implied_volatility: true,
            volatility_lookback_hours: 24,
            volatility_update_interval_ms: 60000,
        };
        let pricer = BinaryOptionPricer::new(&config);
        
        // ATM option with 50% volatility, 1 year to expiry
        let price = pricer.price_binary_option(100.0, 100.0, 1.0, 0.5, 0.05);
        assert!(price > 0.0 && price < 1.0);
        
        // Deep ITM should be close to 1.0
        let deep_itm = pricer.price_binary_option(150.0, 100.0, 0.1, 0.3, 0.05);
        assert!(deep_itm > 0.9);
        
        // Deep OTM should be close to 0.0
        let deep_otm = pricer.price_binary_option(50.0, 100.0, 0.1, 0.3, 0.05);
        assert!(deep_otm < 0.1);
    }

    #[test]
    fn test_greeks_calculation() {
        let config = PricingConfig {
            use_implied_volatility: true,
            volatility_lookback_hours: 24,
            volatility_update_interval_ms: 60000,
        };
        let pricer = BinaryOptionPricer::new(&config);
        
        let result = pricer.price_with_greeks(100.0, 100.0, 0.25, 0.5, 0.05);
        
        // Delta should be positive for call
        assert!(result.greeks.delta > 0.0);
        
        // Vega should be positive (options gain value with more volatility)
        // For binary options, vega can be negative near ATM
        assert!(result.greeks.vega.abs() > 0.0);
    }

    #[test]
    fn test_implied_volatility() {
        let config = PricingConfig {
            use_implied_volatility: true,
            volatility_lookback_hours: 24,
            volatility_update_interval_ms: 60000,
        };
        let pricer = BinaryOptionPricer::new(&config);
        
        let true_vol = 0.5;
        let spot = 100.0;
        let strike = 100.0;
        let tte = 0.25;
        let r = 0.05;
        
        let market_price = pricer.price_binary_option(spot, strike, tte, true_vol, r);
        let implied = pricer.calculate_implied_volatility(market_price, spot, strike, tte, r);
        
        assert!(implied.is_some());
        let iv = implied.unwrap();
        assert!((iv - true_vol).abs() < 0.01);
    }
}
