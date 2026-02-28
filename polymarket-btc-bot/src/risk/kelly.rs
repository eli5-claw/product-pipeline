/// Kelly Criterion implementation for optimal position sizing
/// 
/// The Kelly Criterion determines the optimal fraction of capital to bet
/// given the probability of winning and the payoff odds.
/// 
/// Formula: f* = (bp - q) / b
/// where:
/// - f* = optimal fraction of capital to bet
/// - b = net odds received on the bet (decimal odds - 1)
/// - p = probability of winning
/// - q = probability of losing = 1 - p
pub struct KellyCriterion {
    /// Fractional Kelly multiplier (e.g., 0.25 for "quarter Kelly")
    /// Used to reduce volatility at the cost of expected growth
    fractional_kelly: f64,
}

impl KellyCriterion {
    /// Create a new Kelly Criterion calculator
    /// 
    /// # Arguments
    /// * `fractional_kelly` - Multiplier to apply to Kelly fraction (typically 0.1 to 0.5)
    pub fn new(fractional_kelly: f64) -> Self {
        Self {
            fractional_kelly: fractional_kelly.clamp(0.01, 1.0),
        }
    }
    
    /// Calculate the Kelly fraction for a binary outcome bet
    /// 
    /// # Arguments
    /// * `edge` - Expected value / edge (fair_price - market_price)
    /// * `market_price` - Current market price (probability implied by odds)
    /// 
    /// # Returns
    /// Optimal fraction of bankroll to bet (0 to 1)
    pub fn calculate_fraction(
        &self,
        edge: f64,
        market_price: f64,
    ) -> f64 {
        if edge <= 0.0 || market_price <= 0.0 || market_price >= 1.0 {
            return 0.0;
        }
        
        // Convert market price to implied probability
        let q = market_price; // Probability of losing (market's view)
        let p = q + edge;     // Probability of winning (our view)
        
        // Ensure probabilities are valid
        if p <= 0.0 || p >= 1.0 {
            return 0.0;
        }
        
        // Calculate odds
        // If market price is 0.55, odds are (1 - 0.55) / 0.55 = 0.818
        let b = (1.0 - market_price) / market_price;
        
        // Full Kelly formula: f* = (bp - q) / b
        let full_kelly = (b * p - q) / b;
        
        // Apply fractional Kelly
        let kelly_fraction = full_kelly * self.fractional_kelly;
        
        // Clamp to valid range
        kelly_fraction.clamp(0.0, 1.0)
    }
    
    /// Calculate Kelly fraction from win probability and payoff odds
    /// 
    /// # Arguments
    /// * `win_probability` - Our estimated probability of winning (0 to 1)
    /// * `decimal_odds` - Decimal odds (e.g., 2.0 for even money)
    pub fn calculate_from_odds(
        &self,
        win_probability: f64,
        decimal_odds: f64,
    ) -> f64 {
        if win_probability <= 0.0 || win_probability >= 1.0 || decimal_odds <= 1.0 {
            return 0.0;
        }
        
        let b = decimal_odds - 1.0; // Net odds
        let p = win_probability;
        let q = 1.0 - p;
        
        // Full Kelly: f* = (bp - q) / b
        let full_kelly = (b * p - q) / b;
        
        // Apply fractional Kelly
        full_kelly.clamp(0.0, 1.0) * self.fractional_kelly
    }
    
    /// Calculate expected growth rate for a given bet size
    /// 
    /// G(f) = p * log(1 + bf) + q * log(1 - f)
    /// where f is the fraction of bankroll bet
    pub fn expected_growth_rate(
        &self,
        win_probability: f64,
        decimal_odds: f64,
        bet_fraction: f64,
    ) -> f64 {
        if bet_fraction <= 0.0 || bet_fraction >= 1.0 {
            return 0.0;
        }
        
        let b = decimal_odds - 1.0;
        let p = win_probability;
        let q = 1.0 - p;
        
        p * (1.0 + b * bet_fraction).ln() + q * (1.0 - bet_fraction).ln()
    }
    
    /// Calculate the certainty equivalent return
    /// This is the guaranteed return that would be equivalent to the risky bet
    pub fn certainty_equivalent(
        &self,
        win_probability: f64,
        decimal_odds: f64,
        bet_fraction: f64,
        risk_aversion: f64,
    ) -> f64 {
        let growth_rate = self.expected_growth_rate(win_probability, decimal_odds, bet_fraction);
        
        // For log utility (Kelly), certainty equivalent is exp(G) - 1
        // With risk aversion, we adjust the effective growth rate
        growth_rate.exp().powf(1.0 / risk_aversion) - 1.0
    }
    
    /// Calculate maximum drawdown probability given Kelly fraction
    /// 
    /// Based on the approximation: P(drawdown > D) ≈ exp(-2 * G * ln(D) / V)
    /// where G is growth rate and V is variance of growth
    pub fn drawdown_probability(
        &self,
        win_probability: f64,
        decimal_odds: f64,
        bet_fraction: f64,
        drawdown_threshold: f64,
    ) -> f64 {
        if drawdown_threshold <= 0.0 || drawdown_threshold >= 1.0 {
            return 0.0;
        }
        
        let b = decimal_odds - 1.0;
        let p = win_probability;
        let q = 1.0 - p;
        let f = bet_fraction;
        
        // Expected growth per bet
        let g = p * (1.0 + b * f).ln() + q * (1.0 - f).ln();
        
        // Variance of growth per bet
        let e_growth_sq = p * (1.0 + b * f).ln().powi(2) + q * (1.0 - f).ln().powi(2);
        let v = e_growth_sq - g.powi(2);
        
        if v <= 0.0 {
            return 0.0;
        }
        
        // Probability of exceeding drawdown threshold
        (-2.0 * g * drawdown_threshold.ln() / v).exp()
    }
    
    /// Get the fractional Kelly multiplier
    pub fn fractional_kelly(&self) -> f64 {
        self.fractional_kelly
    }
}

impl Default for KellyCriterion {
    fn default() -> Self {
        Self::new(0.25) // Conservative quarter-Kelly by default
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_kelly_fair_bet() {
        let kelly = KellyCriterion::new(1.0); // Full Kelly
        
        // Fair coin flip with 2:1 payout
        // p = 0.5, b = 1.0
        // f* = (1.0 * 0.5 - 0.5) / 1.0 = 0.0
        let fraction = kelly.calculate_from_odds(0.5, 2.0);
        assert!((fraction - 0.0).abs() < 1e-10, "Fair bet should have Kelly = 0");
    }
    
    #[test]
    fn test_kelly_profitable_bet() {
        let kelly = KellyCriterion::new(1.0); // Full Kelly
        
        // 60% chance of winning with 2:1 payout
        // p = 0.6, b = 1.0
        // f* = (1.0 * 0.6 - 0.4) / 1.0 = 0.2
        let fraction = kelly.calculate_from_odds(0.6, 2.0);
        assert!((fraction - 0.2).abs() < 1e-10, "Profitable bet Kelly should be 0.2");
    }
    
    #[test]
    fn test_fractional_kelly() {
        let kelly = KellyCriterion::new(0.5); // Half Kelly
        
        // 60% chance of winning with 2:1 payout
        // Full Kelly = 0.2, Half Kelly = 0.1
        let fraction = kelly.calculate_from_odds(0.6, 2.0);
        assert!((fraction - 0.1).abs() < 1e-10, "Half Kelly should be 0.1");
    }
    
    #[test]
    fn test_kelly_with_edge() {
        let kelly = KellyCriterion::new(1.0);
        
        // Market price = 0.55 (implies 55% probability)
        // Our fair price = 0.60 (we think 60% probability)
        // Edge = 0.05
        let fraction = kelly.calculate_fraction(0.05, 0.55);
        
        // Should be positive
        assert!(fraction > 0.0, "Should have positive Kelly fraction with edge");
        assert!(fraction < 1.0, "Kelly fraction should be less than 1");
    }
    
    #[test]
    fn test_no_edge_no_bet() {
        let kelly = KellyCriterion::new(1.0);
        
        // No edge
        let fraction = kelly.calculate_fraction(0.0, 0.55);
        assert_eq!(fraction, 0.0, "No edge should result in zero Kelly fraction");
        
        // Negative edge
        let fraction = kelly.calculate_fraction(-0.05, 0.55);
        assert_eq!(fraction, 0.0, "Negative edge should result in zero Kelly fraction");
    }
    
    #[test]
    fn test_expected_growth_rate() {
        let kelly = KellyCriterion::new(1.0);
        
        // 60% win probability, 2:1 odds
        let growth = kelly.expected_growth_rate(0.6, 2.0, 0.2); // Full Kelly bet
        
        // Growth should be positive
        assert!(growth > 0.0, "Expected growth should be positive for optimal bet");
        
        // Over-betting should reduce growth
        let growth_over = kelly.expected_growth_rate(0.6, 2.0, 0.5);
        assert!(growth_over < growth, "Over-betting should reduce expected growth");
    }
    
    #[test]
    fn test_drawdown_probability() {
        let kelly = KellyCriterion::new(1.0);
        
        // 60% win probability, 2:1 odds, full Kelly
        let prob = kelly.drawdown_probability(0.6, 2.0, 0.2, 0.5); // 50% drawdown
        
        // Probability should be between 0 and 1
        assert!(prob >= 0.0 && prob <= 1.0, "Drawdown probability should be valid");
    }
}
