/**
 * AgriPredict AI Engine - Interactive Dashboard Controller
 * Connects frontend to FastAPI backend decision optimization services.
 */

const API_ANALYZE_ENDPOINT = '/api/analyze';

document.addEventListener('DOMContentLoaded', () => {
    console.log("AgriPredict AI Engine Dashboard initialized.");
    setupFormHandlers();
    setupPresetButtons();
    fetchHealthStatus();
});

/**
 * Health check & status update
 */
async function fetchHealthStatus() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        console.log("Backend status:", data);
    } catch (err) {
        console.warn("Backend status check failed:", err.message);
    }
}

/**
 * Form submission setup
 */
function setupFormHandlers() {
    const form = document.getElementById('farmer-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = collectFormData();
        if (!validateForm(payload)) return;

        await analyzeMarket(payload);
    });
}

/**
 * Quick preset scenario buttons for demo testing
 */
function setupPresetButtons() {
    const btnStore = document.getElementById('preset-store');
    const btnSell = document.getElementById('preset-sell');

    if (btnStore) {
        btnStore.addEventListener('click', () => {
            document.getElementById('crop').value = 'Tomato';
            document.getElementById('variety').value = 'Roma';
            document.getElementById('quantity_kg').value = '5000';
            document.getElementById('expected_harvest_window').value = 'Immediate';
            document.getElementById('local_market').value = 'Nashik Mandi';
            document.getElementById('location').value = 'Nashik Agro Zone';
            document.getElementById('expected_storage_days').value = '14';
            
            // Auto submit
            document.getElementById('analyze-btn').click();
        });
    }

    if (btnSell) {
        btnSell.addEventListener('click', () => {
            document.getElementById('crop').value = 'Potato';
            document.getElementById('variety').value = 'Desi';
            document.getElementById('quantity_kg').value = '10000';
            document.getElementById('expected_harvest_window').value = 'Immediate';
            document.getElementById('local_market').value = 'Agra Wholesale Market';
            document.getElementById('location').value = 'Agra Sector 4';
            document.getElementById('expected_storage_days').value = '14';

            // Auto submit
            document.getElementById('analyze-btn').click();
        });
    }
}

/**
 * Collects form inputs into matching FarmerInput schema object
 */
function collectFormData() {
    return {
        crop: document.getElementById('crop').value,
        variety: document.getElementById('variety').value || 'Standard',
        cultivation_area: parseFloat(document.getElementById('cultivation_area').value) || 1.0,
        expected_harvest_window: document.getElementById('expected_harvest_window').value,
        local_market: document.getElementById('local_market').value || 'Local Mandi',
        location: document.getElementById('location').value || 'Local District',
        quantity_kg: parseFloat(document.getElementById('quantity_kg').value),
        expected_storage_days: parseInt(document.getElementById('expected_storage_days').value, 10) || 14
    };
}

/**
 * Validates farmer input parameters
 */
function validateForm(payload) {
    hideError();

    if (!payload.crop) {
        showError("Please select a valid crop type.");
        return false;
    }
    if (isNaN(payload.quantity_kg) || payload.quantity_kg <= 0) {
        showError("Available quantity (quantity_kg) must be greater than zero.");
        return false;
    }
    if (payload.expected_storage_days < 14 || payload.expected_storage_days > 30) {
        showError("Storage duration target must be between 14 and 30 days.");
        return false;
    }

    return true;
}

/**
 * Executes POST /api/analyze request to FastAPI backend
 */
async function analyzeMarket(payload) {
    showLoading(true);
    hideError();

    try {
        const response = await fetch(API_ANALYZE_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: 'Analysis failed' }));
            throw new Error(errorData.detail || `Server returned status ${response.status}`);
        }

        const data = await response.json();
        console.log("Analysis API Response:", data);

        renderDashboardResults(data);
    } catch (error) {
        console.error("API Analysis Error:", error);
        showError(`Analysis failed: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

/**
 * Renders all dashboard sections from backend response payload
 */
function renderDashboardResults(data) {
    // Hide initial state banner
    const initialState = document.getElementById('initial-state');
    if (initialState) initialState.classList.add('hidden');

    // Show results container
    const resultsContainer = document.getElementById('results-container');
    if (resultsContainer) resultsContainer.classList.remove('hidden');

    // Render individual components
    renderRecommendation(data.recommendation, data.arbitrage);
    renderMarketSnapshot(data.market_data, data.farmer_input);
    renderForecast(data.forecast);
    renderArbitrage(data.arbitrage, data.recommendation);
    renderStorage(data.recommended_storage);
    renderBuyers(data.top_buyers);
    renderReasons(data.recommendation);
    renderSummary(data);

    // Scroll to results banner smoothly
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Render Visually Dominant Recommendation Card (STORE & HOLD vs SELL IMMEDIATELY)
 */
function renderRecommendation(rec, arb) {
    const sec = document.getElementById('recommendation-section');
    if (!sec) return;

    const isStore = rec.action === 'STORE & HOLD';
    const bannerClass = isStore ? 'rec-banner-store' : 'rec-banner-sell';
    const actionBadge = isStore ? '📦 STORE & HOLD' : '⚡ SELL IMMEDIATELY';
    const netAdvantageFormatted = rec.economic_difference >= 0 
        ? `+₹${rec.economic_difference.toLocaleString()}`
        : `-₹${Math.abs(rec.economic_difference).toLocaleString()}`;
    const confidencePct = Math.round((rec.confidence || 0.85) * 100);

    sec.innerHTML = `
        <div class="recommendation-banner ${bannerClass}">
            <div class="rec-header-block">
                <div class="rec-action-badge">${actionBadge}</div>
                <div class="rec-subhead">Confidence Index: <strong>${confidencePct}%</strong> | Optimal Horizon: <strong>${arb.optimal_storage_days || 14} Days</strong></div>
            </div>
            <div class="rec-metrics-block">
                <span class="rec-advantage-lbl">Projected Net Financial Advantage</span>
                <span class="rec-advantage-val">${netAdvantageFormatted}</span>
                <span class="rec-breakeven-tag">Break-even Spot Price: ₹${rec.break_even_price.toFixed(2)}/kg</span>
            </div>
        </div>
    `;
}

/**
 * Render Current Market Snapshot Grid
 */
function renderMarketSnapshot(market, input) {
    document.getElementById('snap-price').textContent = `₹${market.current_price.toFixed(2)}/${market.unit || 'kg'}`;
    document.getElementById('snap-market').textContent = market.location || 'Local Mandi';
    document.getElementById('snap-volume').textContent = `${market.arrival_volume_tons.toFixed(1)} Tons`;
    document.getElementById('snap-trend').textContent = formatTrendLabel(market.trend);
    document.getElementById('snap-qty').textContent = `${input.quantity_kg.toLocaleString()} kg`;
    document.getElementById('snap-crop').textContent = `${input.crop} (${input.variety || 'Standard'})`;
}

/**
 * Render Price Forecast Section & SVG Line Chart
 */
function renderForecast(forecast) {
    document.getElementById('forecast-horizon-badge').textContent = `${forecast.forecast_horizon_days}-Day Horizon`;
    document.getElementById('forecast-confidence-badge').textContent = `${Math.round(forecast.confidence * 100)}% Confidence`;

    document.getElementById('fc-current').textContent = `₹${forecast.current_price.toFixed(2)}/kg`;
    document.getElementById('fc-projected').textContent = `₹${forecast.projected_price.toFixed(2)}/kg`;
    document.getElementById('fc-peak').textContent = `₹${forecast.peak_price.toFixed(2)}/kg (Day ${forecast.peak_day})`;

    const growthPct = ((forecast.projected_price - forecast.current_price) / forecast.current_price) * 100;
    const growthElem = document.getElementById('fc-growth');
    growthElem.textContent = `${growthPct >= 0 ? '+' : ''}${growthPct.toFixed(1)}%`;
    growthElem.className = `meta-value ${growthPct >= 0 ? 'text-green' : 'text-danger'}`;

    // Render Reasons
    const reasonsBox = document.getElementById('forecast-reasons-box');
    if (reasonsBox && forecast.reasons) {
        reasonsBox.innerHTML = `
            <ul>
                ${forecast.reasons.map(r => `<li>💡 ${escapeHtml(r)}</li>`).join('')}
            </ul>
        `;
    }

    // Render SVG Chart
    renderSVGChart(forecast.daily_forecast, forecast.forecast_horizon_days);
}

/**
 * Generates dynamic, responsive SVG Line Chart for daily price forecast
 */
function renderSVGChart(dailyForecast, horizonDays) {
    const container = document.getElementById('svg-chart-container');
    if (!container || !dailyForecast || dailyForecast.length === 0) return;

    const width = 800;
    const height = 240;
    const padding = { top: 25, right: 35, bottom: 35, left: 50 };

    const prices = dailyForecast.map(d => d.price);
    const minPrice = Math.floor(Math.min(...prices) * 0.95);
    const maxPrice = Math.ceil(Math.max(...prices) * 1.05);

    const getX = (index) => padding.left + (index / (dailyForecast.length - 1)) * (width - padding.left - padding.right);
    const getY = (price) => height - padding.bottom - ((price - minPrice) / (maxPrice - minPrice)) * (height - padding.top - padding.bottom);

    // Build line path points
    const points = dailyForecast.map((d, i) => `${getX(i)},${getY(d.price)}`).join(' ');
    
    // Area fill path
    const areaPoints = `${getX(0)},${height - padding.bottom} ${points} ${getX(dailyForecast.length - 1)},${height - padding.bottom}`;

    // Grid lines & Y axis ticks
    const yTicks = 4;
    let gridLinesSvg = '';
    for (let i = 0; i <= yTicks; i++) {
        const p = minPrice + (i / yTicks) * (maxPrice - minPrice);
        const y = getY(p);
        gridLinesSvg += `
            <line x1="${padding.left}" y1="${y}" x2="${width - padding.right}" y2="${y}" stroke="#273554" stroke-dasharray="3,3" />
            <text x="${padding.left - 10}" y="${y + 4}" fill="#94a3b8" font-size="11" text-anchor="end">₹${p.toFixed(1)}</text>
        `;
    }

    // X axis ticks
    let xTicksSvg = '';
    dailyForecast.forEach((d, i) => {
        if (i === 0 || i === Math.floor(dailyForecast.length / 2) || i === dailyForecast.length - 1) {
            const x = getX(i);
            xTicksSvg += `
                <text x="${x}" y="${height - 10}" fill="#94a3b8" font-size="11" text-anchor="middle">Day ${d.day}</text>
            `;
        }
    });

    // Data points dots
    let dotsSvg = '';
    dailyForecast.forEach((d, i) => {
        const x = getX(i);
        const y = getY(d.price);
        dotsSvg += `
            <circle cx="${x}" cy="${y}" r="4" fill="#10b981" stroke="#0b1329" stroke-width="2">
                <title>Day ${d.day}: ₹${d.price.toFixed(2)}/kg</title>
            </circle>
        `;
    });

    const svgMarkup = `
        <svg viewBox="0 0 ${width} ${height}" preserveAspectRatio="none">
            <defs>
                <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#10b981" stop-opacity="0.35" />
                    <stop offset="100%" stop-color="#10b981" stop-opacity="0.0" />
                </linearGradient>
            </defs>
            
            ${gridLinesSvg}
            ${xTicksSvg}
            
            <polygon points="${areaPoints}" fill="url(#chartGradient)" />
            <polyline points="${points}" fill="none" stroke="#10b981" stroke-width="3" stroke-linecap="round" />
            ${dotsSvg}
        </svg>
    `;

    container.innerHTML = svgMarkup;
}

/**
 * Render Arbitrage Financial Breakdown
 */
function renderArbitrage(arb, rec) {
    document.getElementById('arb-days-badge').textContent = `${arb.optimal_storage_days} Days Storage`;
    document.getElementById('arb-immediate').textContent = `₹${rec.current_sale_value.toLocaleString()}`;
    document.getElementById('arb-future').textContent = `₹${(arb.gross_future_value * arb.optimal_storage_days).toLocaleString()}`;
    document.getElementById('arb-spoilage').textContent = `-₹${rec.spoilage_loss.toLocaleString()}`;
    document.getElementById('arb-spoilage-rate').textContent = `Perishability rate: ${(arb.spoilage_rate * 100).toFixed(1)}%`;
    document.getElementById('arb-costs').textContent = `-₹${(rec.storage_cost + rec.transit_cost).toLocaleString()}`;
    document.getElementById('arb-costs-sub').textContent = `Storage: ₹${rec.storage_cost.toLocaleString()} | Freight: ₹${rec.transit_cost.toLocaleString()}`;

    const netElem = document.getElementById('arb-net-diff');
    const isPositive = rec.economic_difference >= 0;
    netElem.textContent = `${isPositive ? '+' : ''}₹${rec.economic_difference.toLocaleString()}`;
    netElem.className = `adv-value ${isPositive ? 'text-green' : 'text-danger'}`;

    document.getElementById('arb-break-even').textContent = `Break-even Spot Price Threshold: ₹${arb.break_even_future_price.toFixed(2)}/kg`;
}

/**
 * Render Recommended Storage Facility Section
 */
function renderStorage(facility) {
    const container = document.getElementById('storage-details');
    if (!container) return;

    if (!facility) {
        container.innerHTML = `<p class="text-muted">No nearby cold-storage facility required or available.</p>`;
        return;
    }

    container.innerHTML = `
        <div class="storage-title-row">
            <span class="facility-name">${escapeHtml(facility.name)}</span>
            <span class="facility-dist">📍 ${facility.distance_km.toFixed(1)} km away</span>
        </div>
        <div class="facility-info-grid">
            <div class="info-item">
                <span class="info-lbl">Location</span>
                <span class="info-val">${escapeHtml(facility.location || 'Agro Zone')}</span>
            </div>
            <div class="info-item">
                <span class="info-lbl">Daily Storage Rate</span>
                <span class="info-val">₹${facility.daily_cost_per_kg}/kg/day</span>
            </div>
            <div class="info-item">
                <span class="info-lbl">Available Capacity</span>
                <span class="info-val">${facility.available_capacity_kg.toLocaleString()} kg</span>
            </div>
            <div class="info-item">
                <span class="info-lbl">Facility Rating</span>
                <span class="info-val">⭐ ${facility.rating} / 5.0</span>
            </div>
            <div class="info-item">
                <span class="info-lbl">Est. Storage Fee</span>
                <span class="info-val text-accent">₹${facility.total_storage_cost.toLocaleString()}</span>
            </div>
            <div class="info-item">
                <span class="info-lbl">Est. Freight Transit</span>
                <span class="info-val text-accent">₹${facility.estimated_transit_cost.toLocaleString()}</span>
            </div>
        </div>
    `;
}

/**
 * Render Ranked Buyers Section
 */
function renderBuyers(buyers) {
    const container = document.getElementById('buyers-list-container');
    if (!container) return;

    if (!buyers || buyers.length === 0) {
        container.innerHTML = `<p class="text-muted">No buyers matching current criteria.</p>`;
        return;
    }

    container.innerHTML = buyers.map((b, idx) => `
        <div class="buyer-card">
            <div class="buyer-rank">#${idx + 1}</div>
            <div class="buyer-main">
                <span class="buyer-name">${escapeHtml(b.company_name)}</span>
                <span class="buyer-sub">${escapeHtml(b.buyer_type)} | Offered Price: <strong>₹${b.offered_price_per_kg.toFixed(2)}/kg</strong> | Distance: <strong>${b.distance_km} km</strong></span>
                <div class="buyer-reasons-tags">
                    ${(b.match_reasons || []).map(r => `<span class="tag-reason">${escapeHtml(r)}</span>`).join('')}
                </div>
            </div>
            <div class="buyer-score-block">
                <span class="score-num">${b.match_score.toFixed(1)} <small>/ 100</small></span>
                <div class="score-bar-track">
                    <div class="score-bar-fill" style="width: ${Math.min(100, b.match_score)}%;"></div>
                </div>
            </div>
        </div>
    `).join('');
}

/**
 * Render Why This Recommendation (Explainability & Risks)
 */
function renderReasons(rec) {
    const reasonsList = document.getElementById('reasons-list');
    const risksList = document.getElementById('risks-list');

    if (reasonsList && rec.reasons) {
        reasonsList.innerHTML = rec.reasons.map(r => `<li>${escapeHtml(r)}</li>`).join('');
    }

    if (risksList && rec.risks) {
        risksList.innerHTML = rec.risks.map(r => `<li>${escapeHtml(r)}</li>`).join('');
    }
}

/**
 * Render Executive Summary Table
 */
function renderSummary(data) {
    const inp = data.farmer_input;
    const mkt = data.market_data;
    const fc = data.forecast;
    const rec = data.recommendation;
    const st = data.recommended_storage;
    const by = data.top_buyers && data.top_buyers[0];

    document.getElementById('sum-crop').textContent = `${inp.crop} (${inp.quantity_kg.toLocaleString()} kg)`;
    document.getElementById('sum-prices').textContent = `₹${mkt.current_price.toFixed(2)} → ₹${fc.projected_price.toFixed(2)} / kg`;
    
    const actionElem = document.getElementById('sum-action');
    actionElem.innerHTML = `<strong class="${rec.action === 'STORE & HOLD' ? 'text-green' : 'text-danger'}">${rec.action}</strong>`;
    
    const advElem = document.getElementById('sum-adv');
    const isPos = rec.economic_difference >= 0;
    advElem.textContent = `${isPos ? '+' : ''}₹${rec.economic_difference.toLocaleString()}`;
    advElem.className = `font-bold ${isPos ? 'text-green' : 'text-danger'}`;

    document.getElementById('sum-storage').textContent = st ? `${st.name} (${st.distance_km} km)` : 'Direct Mandi Delivery';
    document.getElementById('sum-buyer').textContent = by ? `${by.company_name} (Score: ${by.match_score.toFixed(1)}/100)` : 'Regional Wholesale Mandi';
}

/**
 * Helper: Show/Hide Loading UI State
 */
function showLoading(isLoading) {
    const btn = document.getElementById('analyze-btn');
    const loadingCard = document.getElementById('loading-card');

    if (btn) {
        btn.disabled = isLoading;
        btn.innerHTML = isLoading 
            ? `<span class="btn-icon">⏳</span> ANALYZING MARKET...` 
            : `<span class="btn-icon">⚡</span> GET AI RECOMMENDATION`;
    }

    if (loadingCard) {
        if (isLoading) {
            loadingCard.classList.remove('hidden');
            const initialState = document.getElementById('initial-state');
            if (initialState) initialState.classList.add('hidden');
        } else {
            loadingCard.classList.add('hidden');
        }
    }
}

/**
 * Helper: Show Error Banner
 */
function showError(message) {
    const errBanner = document.getElementById('error-banner');
    const errMsg = document.getElementById('error-message');
    if (errBanner && errMsg) {
        errMsg.textContent = message;
        errBanner.classList.remove('hidden');
    }
}

/**
 * Helper: Hide Error Banner
 */
function hideError() {
    const errBanner = document.getElementById('error-banner');
    if (errBanner) errBanner.classList.add('hidden');
}

/**
 * Utility: Format trend label
 */
function formatTrendLabel(trend) {
    if (!trend) return 'Stable';
    return trend.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

/**
 * Utility: HTML Escape
 */
function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
