use axum::{
    extract::{Path, Query, State},
    http::StatusCode,
    response::{Html, IntoResponse, Json},
    routing::{get, post},
    Router,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use tokio::sync::RwLock;
use tracing::{info, warn};
use chrono::{DateTime, Utc};

/// Dashboard state shared across handlers
#[derive(Clone)]
pub struct DashboardState {
    pub bot_config: Arc<RwLock<BotConfig>>,
    pub trade_history: Arc<RwLock<Vec<TradeRecord>>>,
    pub performance_metrics: Arc<RwLock<PerformanceMetrics>>,
    pub current_price: Arc<RwLock<Option<f64>>>,
    pub bot_status: Arc<RwLock<BotStatus>>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BotConfig {
    pub enabled: bool,
    pub min_edge_threshold: f64,
    pub kelly_fraction: f64,
    pub max_position_size: f64,
    pub max_daily_loss: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TradeRecord {
    pub id: String,
    pub timestamp: DateTime<Utc>,
    pub market_id: String,
    pub side: String,
    pub size: f64,
    pub price: f64,
    pub expected_value: f64,
    pub edge: f64,
    pub pnl: Option<f64>,
    pub status: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct PerformanceMetrics {
    pub total_trades: u64,
    pub winning_trades: u64,
    pub losing_trades: u64,
    pub total_pnl: f64,
    pub daily_pnl: f64,
    pub win_rate: f64,
    pub avg_trade_size: f64,
    pub max_drawdown: f64,
    pub sharpe_ratio: f64,
    pub current_balance: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BotStatus {
    pub running: bool,
    pub last_price_update: Option<DateTime<Utc>>,
    pub last_trade_time: Option<DateTime<Utc>>,
    pub open_positions: usize,
    pub errors_count: u64,
    pub uptime_seconds: u64,
}

impl DashboardState {
    pub fn new() -> Self {
        Self {
            bot_config: Arc::new(RwLock::new(BotConfig {
                enabled: true,
                min_edge_threshold: 0.02,
                kelly_fraction: 0.25,
                max_position_size: 1000.0,
                max_daily_loss: 5000.0,
            })),
            trade_history: Arc::new(RwLock::new(Vec::new())),
            performance_metrics: Arc::new(RwLock::new(PerformanceMetrics::default())),
            current_price: Arc::new(RwLock::new(None)),
            bot_status: Arc::new(RwLock::new(BotStatus {
                running: true,
                last_price_update: None,
                last_trade_time: None,
                open_positions: 0,
                errors_count: 0,
                uptime_seconds: 0,
            })),
        }
    }
}

/// Create the dashboard router
pub fn create_router(state: DashboardState) -> Router {
    Router::new()
        .route("/", get(index_handler))
        .route("/dashboard", get(dashboard_handler))
        .route("/api/status", get(get_status))
        .route("/api/metrics", get(get_metrics))
        .route("/api/trades", get(get_trades))
        .route("/api/config", get(get_config).post(update_config))
        .route("/api/price", get(get_price))
        .route("/api/bot/:action", post(bot_control))
        .route("/static/*path", get(static_handler))
        .with_state(state)
}

/// Main dashboard HTML
async fn index_handler() -> Html<&'static str> {
    Html(DASHBOARD_HTML)
}

async fn dashboard_handler() -> Html<&'static str> {
    Html(DASHBOARD_HTML)
}

/// Get bot status
async fn get_status(
    State(state): State<DashboardState>,
) -> Json<BotStatus> {
    let status = state.bot_status.read().await.clone();
    Json(status)
}

/// Get performance metrics
async fn get_metrics(
    State(state): State<DashboardState>,
) -> Json<PerformanceMetrics> {
    let metrics = state.performance_metrics.read().await.clone();
    Json(metrics)
}

/// Get trade history with pagination
#[derive(Deserialize)]
struct TradeQuery {
    limit: Option<usize>,
    offset: Option<usize>,
}

async fn get_trades(
    State(state): State<DashboardState>,
    Query(params): Query<TradeQuery>,
) -> Json<Vec<TradeRecord>> {
    let trades = state.trade_history.read().await;
    let limit = params.limit.unwrap_or(50);
    let offset = params.offset.unwrap_or(0);
    
    let result: Vec<TradeRecord> = trades
        .iter()
        .rev()
        .skip(offset)
        .take(limit)
        .cloned()
        .collect();
    
    Json(result)
}

/// Get current configuration
async fn get_config(
    State(state): State<DashboardState>,
) -> Json<BotConfig> {
    let config = state.bot_config.read().await.clone();
    Json(config)
}

/// Update configuration
async fn update_config(
    State(state): State<DashboardState>,
    Json(new_config): Json<BotConfig>,
) -> impl IntoResponse {
    let mut config = state.bot_config.write().await;
    *config = new_config;
    info!("Bot configuration updated");
    (StatusCode::OK, "Configuration updated")
}

/// Get current BTC price
async fn get_price(
    State(state): State<DashboardState>,
) -> Json<serde_json::Value> {
    let price = *state.current_price.read().await;
    Json(serde_json::json!({
        "price": price,
        "timestamp": Utc::now()
    }))
}

/// Bot control actions (start, stop, pause)
async fn bot_control(
    State(state): State<DashboardState>,
    Path(action): Path<String>,
) -> impl IntoResponse {
    let mut status = state.bot_status.write().await;
    
    match action.as_str() {
        "start" => {
            status.running = true;
            info!("Bot started via dashboard");
            (StatusCode::OK, "Bot started")
        }
        "stop" => {
            status.running = false;
            info!("Bot stopped via dashboard");
            (StatusCode::OK, "Bot stopped")
        }
        "pause" => {
            status.running = false;
            info!("Bot paused via dashboard");
            (StatusCode::OK, "Bot paused")
        }
        _ => (StatusCode::BAD_REQUEST, "Unknown action"),
    }
}

/// Static file handler
async fn static_handler(Path(path): Path<String>) -> impl IntoResponse {
    match path.as_str() {
        "css/style.css" => (
            [("Content-Type", "text/css")],
            CSS_STYLE
        ),
        "js/dashboard.js" => (
            [("Content-Type", "application/javascript")],
            JS_DASHBOARD
        ),
        _ => (
            [("Content-Type", "text/plain")],
            "Not found"
        ),
    }
}

const DASHBOARD_HTML: &str = r#"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Polymarket BTC Bot Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 Polymarket BTC Bot</h1>
            <div class="status-indicator" id="bot-status">
                <span class="status-dot"></span>
                <span id="status-text">Connecting...</span>
            </div>
        </header>

        <div class="grid">
            <!-- Performance Metrics -->
            <div class="card metrics-card">
                <h2>📊 Performance</h2>
                <div class="metrics-grid">
                    <div class="metric">
                        <label>Total P&L</label>
                        <span id="total-pnl" class="value">$0.00</span>
                    </div>
                    <div class="metric">
                        <label>Daily P&L</label>
                        <span id="daily-pnl" class="value">$0.00</span>
                    </div>
                    <div class="metric">
                        <label>Win Rate</label>
                        <span id="win-rate" class="value">0%</span>
                    </div>
                    <div class="metric">
                        <label>Total Trades</label>
                        <span id="total-trades" class="value">0</span>
                    </div>
                    <div class="metric">
                        <label>Max Drawdown</label>
                        <span id="max-drawdown" class="value">0%</span>
                    </div>
                    <div class="metric">
                        <label>Balance</label>
                        <span id="balance" class="value">$0.00</span>
                    </div>
                </div>
            </div>

            <!-- Current Price -->
            <div class="card price-card">
                <h2>💰 BTC Price</h2>
                <div class="price-display">
                    <span id="btc-price">--</span>
                    <span id="price-change"></span>
                </div>
                <div id="price-timestamp">--</div>
            </div>

            <!-- Bot Controls -->
            <div class="card controls-card">
                <h2>🎮 Controls</h2>
                <div class="control-buttons">
                    <button id="btn-start" class="btn btn-success">▶ Start</button>
                    <button id="btn-pause" class="btn btn-warning">⏸ Pause</button>
                    <button id="btn-stop" class="btn btn-danger">⏹ Stop</button>
                </div>
            </div>

            <!-- Configuration -->
            <div class="card config-card">
                <h2>⚙️ Configuration</h2>
                <form id="config-form">
                    <div class="form-group">
                        <label>Min Edge Threshold</label>
                        <input type="number" id="min-edge" step="0.001" value="0.02">
                    </div>
                    <div class="form-group">
                        <label>Kelly Fraction</label>
                        <input type="number" id="kelly-fraction" step="0.05" min="0" max="1" value="0.25">
                    </div>
                    <div class="form-group">
                        <label>Max Position Size ($)</label>
                        <input type="number" id="max-position" step="100" value="1000">
                    </div>
                    <div class="form-group">
                        <label>Max Daily Loss ($)</label>
                        <input type="number" id="max-daily-loss" step="100" value="5000">
                    </div>
                    <button type="submit" class="btn btn-primary">💾 Save Config</button>
                </form>
            </div>

            <!-- P&L Chart -->
            <div class="card chart-card">
                <h2>📈 P&L History</h2>
                <canvas id="pnl-chart"></canvas>
            </div>

            <!-- Trade History -->
            <div class="card trades-card">
                <h2>📜 Recent Trades</h2>
                <div class="trades-container">
                    <table id="trades-table">
                        <thead>
                            <tr>
                                <th>Time</th>
                                <th>Market</th>
                                <th>Side</th>
                                <th>Size</th>
                                <th>Price</th>
                                <th>Edge</th>
                                <th>P&L</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody id="trades-body">
                            <tr><td colspan="8" class="empty">No trades yet</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script src="/static/js/dashboard.js"></script>
</body>
</html>
"#;

const CSS_STYLE: &str = r#"
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --bg-primary: #0a0e27;
    --bg-secondary: #151b3d;
    --bg-card: #1a2040;
    --text-primary: #ffffff;
    --text-secondary: #8b92a8;
    --accent-green: #00d084;
    --accent-red: #ff4757;
    --accent-blue: #3742fa;
    --accent-yellow: #ffa502;
    --border-color: #2d3561;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.6;
}

.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
}

header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding: 20px;
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 1px solid var(--border-color);
}

h1 {
    font-size: 28px;
    font-weight: 700;
}

.status-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: var(--bg-card);
    border-radius: 20px;
}

.status-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--accent-yellow);
    animation: pulse 2s infinite;
}

.status-dot.running {
    background: var(--accent-green);
}

.status-dot.stopped {
    background: var(--accent-red);
    animation: none;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 20px;
}

.card {
    background: var(--bg-card);
    border-radius: 12px;
    padding: 20px;
    border: 1px solid var(--border-color);
}

.card h2 {
    font-size: 18px;
    margin-bottom: 15px;
    color: var(--text-secondary);
}

.metrics-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
}

.metric {
    display: flex;
    flex-direction: column;
    padding: 15px;
    background: var(--bg-secondary);
    border-radius: 8px;
}

.metric label {
    font-size: 12px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric .value {
    font-size: 24px;
    font-weight: 700;
    margin-top: 5px;
}

.metric .value.positive {
    color: var(--accent-green);
}

.metric .value.negative {
    color: var(--accent-red);
}

.price-display {
    font-size: 48px;
    font-weight: 700;
    text-align: center;
    margin: 20px 0;
}

.price-display .positive {
    color: var(--accent-green);
}

.price-display .negative {
    color: var(--accent-red);
}

#price-timestamp {
    text-align: center;
    color: var(--text-secondary);
    font-size: 14px;
}

.control-buttons {
    display: flex;
    gap: 10px;
}

.btn {
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    flex: 1;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.btn-success {
    background: var(--accent-green);
    color: white;
}

.btn-warning {
    background: var(--accent-yellow);
    color: black;
}

.btn-danger {
    background: var(--accent-red);
    color: white;
}

.btn-primary {
    background: var(--accent-blue);
    color: white;
}

.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    color: var(--text-secondary);
    font-size: 14px;
}

.form-group input {
    width: 100%;
    padding: 10px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    color: var(--text-primary);
    font-size: 14px;
}

.form-group input:focus {
    outline: none;
    border-color: var(--accent-blue);
}

.chart-card {
    grid-column: span 2;
}

.trades-card {
    grid-column: span 2;
}

.trades-container {
    max-height: 400px;
    overflow-y: auto;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th, td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid var(--border-color);
}

th {
    color: var(--text-secondary);
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
}

tbody tr:hover {
    background: var(--bg-secondary);
}

.side-yes {
    color: var(--accent-green);
}

.side-no {
    color: var(--accent-red);
}

.pnl-positive {
    color: var(--accent-green);
}

.pnl-negative {
    color: var(--accent-red);
}

.empty {
    text-align: center;
    color: var(--text-secondary);
    padding: 40px;
}

@media (max-width: 768px) {
    .grid {
        grid-template-columns: 1fr;
    }
    
    .chart-card,
    .trades-card {
        grid-column: span 1;
    }
    
    .metrics-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    
    header {
        flex-direction: column;
        gap: 15px;
    }
}
"#;

const JS_DASHBOARD: &str = r#"
// Dashboard state
let pnlChart = null;
let trades = [];
let pnlHistory = [];

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    initChart();
    startDataUpdates();
    setupEventListeners();
});

// Initialize P&L Chart
function initChart() {
    const ctx = document.getElementById('pnl-chart').getContext('2d');
    
    pnlChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Cumulative P&L',
                data: [],
                borderColor: '#00d084',
                backgroundColor: 'rgba(0, 208, 132, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    display: false
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#8b92a8',
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

// Start periodic data updates
function startDataUpdates() {
    // Update every 2 seconds
    setInterval(updateDashboard, 2000);
    updateDashboard(); // Initial update
}

// Update all dashboard data
async function updateDashboard() {
    try {
        await Promise.all([
            updateStatus(),
            updateMetrics(),
            updatePrice(),
            updateTrades()
        ]);
    } catch (error) {
        console.error('Dashboard update error:', error);
    }
}

// Update bot status
async function updateStatus() {
    try {
        const response = await fetch('/api/status');
        const status = await response.json();
        
        const statusDot = document.querySelector('.status-dot');
        const statusText = document.getElementById('status-text');
        
        if (status.running) {
            statusDot.className = 'status-dot running';
            statusText.textContent = 'Running';
        } else {
            statusDot.className = 'status-dot stopped';
            statusText.textContent = 'Stopped';
        }
    } catch (error) {
        console.error('Status update error:', error);
    }
}

// Update performance metrics
async function updateMetrics() {
    try {
        const response = await fetch('/api/metrics');
        const metrics = await response.json();
        
        updateMetric('total-pnl', metrics.total_pnl, '$');
        updateMetric('daily-pnl', metrics.daily_pnl, '$');
        updateMetric('win-rate', metrics.win_rate * 100, '', '%');
        updateMetric('total-trades', metrics.total_trades, '');
        updateMetric('max-drawdown', metrics.max_drawdown * 100, '', '%');
        updateMetric('balance', metrics.current_balance, '$');
        
        // Update P&L chart
        if (metrics.total_pnl !== undefined) {
            updatePnlChart(metrics.total_pnl);
        }
    } catch (error) {
        console.error('Metrics update error:', error);
    }
}

// Update a single metric display
function updateMetric(id, value, prefix = '', suffix = '') {
    const element = document.getElementById(id);
    if (!element) return;
    
    const numValue = typeof value === 'number' ? value : 0;
    element.textContent = prefix + numValue.toFixed(2) + suffix;
    
    // Add color class based on value
    element.classList.remove('positive', 'negative');
    if (numValue > 0) element.classList.add('positive');
    if (numValue < 0) element.classList.add('negative');
}

// Update BTC price
async function updatePrice() {
    try {
        const response = await fetch('/api/price');
        const data = await response.json();
        
        if (data.price) {
            const priceElement = document.getElementById('btc-price');
            const timestampElement = document.getElementById('price-timestamp');
            
            priceElement.textContent = '$' + data.price.toLocaleString('en-US', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
            
            if (data.timestamp) {
                const date = new Date(data.timestamp);
                timestampElement.textContent = 'Updated: ' + date.toLocaleTimeString();
            }
        }
    } catch (error) {
        console.error('Price update error:', error);
    }
}

// Update trades table
async function updateTrades() {
    try {
        const response = await fetch('/api/trades?limit=20');
        const newTrades = await response.json();
        
        if (JSON.stringify(newTrades) !== JSON.stringify(trades)) {
            trades = newTrades;
            renderTrades();
        }
    } catch (error) {
        console.error('Trades update error:', error);
    }
}

// Render trades table
function renderTrades() {
    const tbody = document.getElementById('trades-body');
    
    if (trades.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="empty">No trades yet</td></tr>';
        return;
    }
    
    tbody.innerHTML = trades.map(trade => {
        const date = new Date(trade.timestamp);
        const timeStr = date.toLocaleTimeString();
        const sideClass = trade.side === 'Yes' ? 'side-yes' : 'side-no';
        const pnlClass = trade.pnl > 0 ? 'pnl-positive' : trade.pnl < 0 ? 'pnl-negative' : '';
        const pnlStr = trade.pnl !== undefined ? '$' + trade.pnl.toFixed(2) : '--';
        
        return `
            <tr>
                <td>${timeStr}</td>
                <td>${trade.market_id.substring(0, 8)}...</td>
                <td class="${sideClass}">${trade.side}</td>
                <td>$${trade.size.toFixed(2)}</td>
                <td>${(trade.price * 100).toFixed(1)}¢</td>
                <td>${(trade.edge * 100).toFixed(2)}%</td>
                <td class="${pnlClass}">${pnlStr}</td>
                <td>${trade.status}</td>
            </tr>
        `;
    }).join('');
}

// Update P&L chart
function updatePnlChart(totalPnl) {
    const now = new Date();
    const timeLabel = now.toLocaleTimeString();
    
    pnlHistory.push({ time: timeLabel, value: totalPnl });
    
    // Keep last 50 data points
    if (pnlHistory.length > 50) {
        pnlHistory.shift();
    }
    
    pnlChart.data.labels = pnlHistory.map(h => h.time);
    pnlChart.data.datasets[0].data = pnlHistory.map(h => h.value);
    pnlChart.update('none');
}

// Setup event listeners
function setupEventListeners() {
    // Control buttons
    document.getElementById('btn-start').addEventListener('click', () => controlBot('start'));
    document.getElementById('btn-pause').addEventListener('click', () => controlBot('pause'));
    document.getElementById('btn-stop').addEventListener('click', () => controlBot('stop'));
    
    // Config form
    document.getElementById('config-form').addEventListener('submit', saveConfig);
    
    // Load initial config
    loadConfig();
}

// Bot control (start/stop/pause)
async function controlBot(action) {
    try {
        const response = await fetch(`/api/bot/${action}`, { method: 'POST' });
        if (response.ok) {
            showNotification(`Bot ${action}ed successfully`);
        } else {
            showNotification(`Failed to ${action} bot`, 'error');
        }
    } catch (error) {
        showNotification(`Error: ${error.message}`, 'error');
    }
}

// Load configuration
async function loadConfig() {
    try {
        const response = await fetch('/api/config');
        const config = await response.json();
        
        document.getElementById('min-edge').value = config.min_edge_threshold;
        document.getElementById('kelly-fraction').value = config.kelly_fraction;
        document.getElementById('max-position').value = config.max_position_size;
        document.getElementById('max-daily-loss').value = config.max_daily_loss;
    } catch (error) {
        console.error('Config load error:', error);
    }
}

// Save configuration
async function saveConfig(e) {
    e.preventDefault();
    
    const config = {
        enabled: true,
        min_edge_threshold: parseFloat(document.getElementById('min-edge').value),
        kelly_fraction: parseFloat(document.getElementById('kelly-fraction').value),
        max_position_size: parseFloat(document.getElementById('max-position').value),
        max_daily_loss: parseFloat(document.getElementById('max-daily-loss').value)
    };
    
    try {
        const response = await fetch('/api/config', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        });
        
        if (response.ok) {
            showNotification('Configuration saved successfully');
        } else {
            showNotification('Failed to save configuration', 'error');
        }
    } catch (error) {
        showNotification(`Error: ${error.message}`, 'error');
    }
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        background: ${type === 'success' ? '#00d084' : '#ff4757'};
        color: white;
        border-radius: 8px;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}
"#;
