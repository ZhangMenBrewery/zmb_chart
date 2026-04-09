/**
 * Chart Renderer - Plotly.js 客戶端渲染庫
 * 用於優化圖表載入速度
 */

// 圖表配置預設值
const CHART_CONFIG = {
    responsive: true,
    displayModeBar: true,
    modeBarButtonsToRemove: ['lasso2d', 'select2d'],
    displaylogo: false,
    responsive: true
};

// 時間範圍配置
const TIME_RANGES = {
    '1d': { days: 1, label: '1 天' },
    '1w': { days: 7, label: '1 週' },
    '1m': { days: 30, label: '1 個月' },
    '3m': { days: 90, label: '3 個月' },
    '6m': { days: 180, label: '6 個月' }
};

// 資料載入範圍（保留完整歷史資料供按鈕切換）
const DEFAULT_DAYS = 180;

/**
 * 根據資料的最後一筆時間戳，計算初始顯示的 1 天範圍
 * 資料庫時間為台灣時間 naive datetime，字串操作保持一致
 */
function getInitialOneDayRange(timestamps) {
    if (!timestamps || timestamps.length === 0) return undefined;
    // 用資料最後一筆時間作為結束點，避免圖表右側出現空白
    const lastDate = new Date(timestamps[timestamps.length - 1].slice(0, 19) + 'Z');
    if (isNaN(lastDate.getTime())) return undefined;
    const startDate = new Date(lastDate);
    startDate.setDate(startDate.getDate() - 1);
    return [startDate.toISOString(), lastDate.toISOString()];
}

/**
 * 創建 Plotly 圖表
 * @param {string} elementId - 圖表容器 ID
 * @param {Object} data - 圖表數據
 * @param {Object} layout - 圖表佈局配置
 */
function createChart(elementId, data, layout) {
    const config = {
        ...CHART_CONFIG,
        ...layout.config || {}
    };
    
    // 提取計算 Y 軸範圍的共用函數
    const getVisibleYRange = (plotData, xRange) => {
        if (!xRange || !xRange[0] || !xRange[1]) return null;
        
        const parseDateFallback = (d) => {
            if (!d) return NaN;
            if (typeof d === 'string') {
                return new Date(d.replace(' ', 'T')).getTime();
            }
            return new Date(d).getTime();
        };

        const x0 = parseDateFallback(xRange[0]);
        const x1 = parseDateFallback(xRange[1]);
        
        if (isNaN(x0) || isNaN(x1)) return null;

        let yMin = Infinity;
        let yMax = -Infinity;

        plotData.forEach(trace => {
            if (trace.visible === 'legendonly' || trace.visible === false) return;
            if (!trace.x || !trace.y) return;
            
            // 加入緩存以避免在拖動 rangeslider 時大量重複解析日期造成卡頓
            if (!trace._xTime) {
                trace._xTime = trace.x.map(d => parseDateFallback(d));
            }
            
            for (let i = 0; i < trace._xTime.length; i++) {
                const t = trace._xTime[i];
                if (t >= x0 && t <= x1) {
                    const y = trace.y[i];
                    if (y !== null && y !== undefined && !isNaN(y)) {
                        if (y < yMin) yMin = y;
                        if (y > yMax) yMax = y;
                    }
                }
            }
        });

        if (yMin !== Infinity && yMax !== -Infinity) {
            const margin = (yMax - yMin) * 0.05;
            // 處理常數直線的情況，避免 margin 為 0 導致錯誤
            const actualMargin = margin === 0 ? 1 : margin;
            return [yMin - actualMargin, yMax + actualMargin];
        }
        return null;
    };
    
    // 初次載入時，針對初始的 X 軸顯示範圍來計算 Y 軸尺度
    if (layout.xaxis && layout.xaxis.range) {
        const initialYRange = getVisibleYRange(data, layout.xaxis.range);
        if (initialYRange) {
            layout.yaxis = layout.yaxis || {};
            layout.yaxis.range = initialYRange;
            layout.yaxis.autorange = false;
        }
    }

    Plotly.newPlot(elementId, data, layout, config).then(function(plotElement) {
        let autoscaleTimeout = null;
        
        const autoscaleY = () => {
            if (!plotElement.layout.xaxis || !plotElement.layout.xaxis.range) return;
            const newYRange = getVisibleYRange(plotElement.data, plotElement.layout.xaxis.range);
            
            if (newYRange) {
                const currentYRange = plotElement.layout.yaxis ? plotElement.layout.yaxis.range : null;
                if (currentYRange && 
                    Math.abs(currentYRange[0] - newYRange[0]) < 1e-6 && 
                    Math.abs(currentYRange[1] - newYRange[1]) < 1e-6) {
                    return;
                }
                // 使用 Plotly.relayout 更新 Y 軸
                Plotly.relayout(plotElement, { 'yaxis.range': newYRange, 'yaxis.autorange': false });
            }
        };

        const debouncedAutoscaleY = () => {
            if (autoscaleTimeout) clearTimeout(autoscaleTimeout);
            autoscaleTimeout = setTimeout(autoscaleY, 150);
        };

        // 監控 X 軸變化（如：縮放、拖動 Slider、點擊範圍按鈕）
        plotElement.on('plotly_relayout', function(eventData) {
            // 如果使用者手動調整了 Y 軸，則不自動覆蓋，尊重其操作
            if (eventData['yaxis.range[0]'] !== undefined || 
                eventData['yaxis.range'] !== undefined || 
                eventData['yaxis.autorange'] !== undefined) {
                return;
            }
            
            const hasXChange = eventData['xaxis.range[0]'] !== undefined || 
                               eventData['xaxis.range'] !== undefined || 
                               eventData['xaxis.autorange'] === true;

            if (hasXChange) {
                // 使用 debounce 避免拖動過程中連續觸發重繪導致卡頓
                debouncedAutoscaleY();
            }
        });

        // 監控圖例點擊開啟/關閉線條，重新調整 Y 軸
        plotElement.on('plotly_restyle', function() {
            debouncedAutoscaleY();
        });
    });
}

/**
 * 獲取熱水罐圖表數據
 */
async function fetchHotwaterData(days = 1) {
    const response = await fetch(`/api/hotwater/?days=${days}`);
    return await response.json();
}

/**
 * 獲取糖化鍋圖表數據
 */
async function fetchMashlauterData(days = 1) {
    const response = await fetch(`/api/mashlauter/?days=${days}`);
    return await response.json();
}

/**
 * 獲取煮沸鍋圖表數據
 */
async function fetchWortkettleData(days = 1) {
    const response = await fetch(`/api/wortkettle/?days=${days}`);
    return await response.json();
}

/**
 * 獲取冰水罐圖表數據
 */
async function fetchIcewaterData(days = 1) {
    const response = await fetch(`/api/icewater/?days=${days}`);
    return await response.json();
}

/**
 * 獲取冷媒罐圖表數據
 */
async function fetchGlycolData(tank = '1', days = 1) {
    const response = await fetch(`/api/glycol/?tank=${tank}&days=${days}`);
    return await response.json();
}

/**
 * 獲取發酵罐圖表數據
 */
async function fetchFvData(fvNumber, days = 1) {
    const response = await fetch(`/api/fv/?fv=${fvNumber}&days=${days}`);
    return await response.json();
}

/**
 * 渲染熱水罐圖表
 */
async function renderHotwaterChart(containerId, days = DEFAULT_DAYS) {
    try {
        const data = await fetchHotwaterData(days);
        
        const traces = [
            {
                name: '溫度',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.temperature,
                line: { color: '#FF6B6B' }
            },
            {
                name: '加熱',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.setpoint.map((v, i) => v * data.valve[i]),
                line: { color: '#FFA500' }
            },
            {
                name: '設定溫度',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.setpoint,
                visible: 'legendonly',
                line: { color: '#4ECDC4' }
            },
            {
                name: '蒸氣閥',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.valve,
                visible: 'legendonly',
                line: { color: '#95E1D3' }
            },
            {
                name: '體積',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.volume,
                visible: 'legendonly',
                line: { color: '#F38181' }
            },
            {
                name: '熱水泵',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.pump,
                visible: 'legendonly',
                line: { color: '#AA96DA' }
            }
        ];
        
        const layout = {
            title: '熱水罐監控',
            xaxis: {
                range: getInitialOneDayRange(data.timestamps),
                autorange: false,
                rangeselector: {
                    buttons: [
                        { count: 1, label: '1d', step: 'day', stepmode: 'backward' },
                        { count: 7, label: '1w', step: 'day', stepmode: 'backward' },
                        { count: 30, label: '1m', step: 'day', stepmode: 'backward' },
                        { count: 90, label: '3m', step: 'day', stepmode: 'backward' },
                        { count: 180, label: '6m', step: 'day', stepmode: 'backward' },
                        { step: 'all' }
                    ]
                },
                rangeslider: { visible: true },
                type: 'date'
            },
            yaxis: { autorange: true },
            showlegend: true,
            legend: { x: 0, y: 1 }
        };
        
        createChart(containerId, traces, layout);
    } catch (error) {
        console.error('Error loading hotwater chart:', error);
    }
}

/**
 * 渲染糖化鍋圖表
 */
async function renderMashlauterChart(containerId, days = DEFAULT_DAYS) {
    try {
        const data = await fetchMashlauterData(days);
        
        const traces = [
            {
                name: '溫度',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.temperature,
                line: { color: '#FF6B6B' }
            },
            {
                name: '加熱',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.setpoint.map((v, i) => v * data.valve[i]),
                line: { color: '#FFA500' }
            },
            {
                name: '糖化泵',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.pumpspeed.map((v, i) => v * data.pump[i]),
                visible: 'legendonly',
                line: { color: '#4ECDC4' }
            },
            {
                name: '攪拌',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.agitatorspeed.map((v, i) => v * data.agitator[i]),
                visible: 'legendonly',
                line: { color: '#95E1D3' }
            },
            {
                name: '流量',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.flowmeter,
                visible: 'legendonly',
                line: { color: '#F38181' }
            }
        ];
        
        const layout = {
            title: '糖化鍋監控',
            xaxis: {
                range: getInitialOneDayRange(data.timestamps),
                autorange: false,
                rangeselector: {
                    buttons: [
                        { count: 1, label: '1d', step: 'day', stepmode: 'backward' },
                        { count: 7, label: '1w', step: 'day', stepmode: 'backward' },
                        { count: 30, label: '1m', step: 'day', stepmode: 'backward' },
                        { count: 90, label: '3m', step: 'day', stepmode: 'backward' },
                        { count: 180, label: '6m', step: 'day', stepmode: 'backward' },
                        { step: 'all' }
                    ]
                },
                rangeslider: { visible: true },
                type: 'date'
            },
            yaxis: { autorange: true },
            showlegend: true
        };
        
        createChart(containerId, traces, layout);
    } catch (error) {
        console.error('Error loading mashlauter chart:', error);
    }
}

/**
 * 渲染煮沸鍋圖表
 */
async function renderWortkettleChart(containerId, days = DEFAULT_DAYS) {
    try {
        const data = await fetchWortkettleData(days);
        
        const traces = [
            {
                name: '溫度',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.temperature,
                line: { color: '#FF6B6B' }
            },
            {
                name: '上部加熱',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.setpoint.map((v, i) => v * data.valve1[i]),
                line: { color: '#FFA500' }
            },
            {
                name: '下部加熱',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.setpoint.map((v, i) => v * data.valve2[i]),
                line: { color: '#FFD93D' }
            },
            {
                name: '麥芽泵',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.pumpspeed.map((v, i) => v * data.pump[i]),
                visible: 'legendonly',
                line: { color: '#4ECDC4' }
            },
            {
                name: '煙囪溫度',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.chimneytemperature,
                visible: 'legendonly',
                line: { color: '#95E1D3' }
            },
            {
                name: '流速',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.flowmeter,
                visible: 'legendonly',
                line: { color: '#F38181' }
            },
            {
                name: '流量',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.flowvolume,
                visible: 'legendonly',
                line: { color: '#AA96DA' }
            }
        ];
        
        const layout = {
            title: '煮沸鍋監控',
            xaxis: {
                range: getInitialOneDayRange(data.timestamps),
                autorange: false,
                rangeselector: {
                    buttons: [
                        { count: 1, label: '1d', step: 'day', stepmode: 'backward' },
                        { count: 7, label: '1w', step: 'day', stepmode: 'backward' },
                        { count: 30, label: '1m', step: 'day', stepmode: 'backward' },
                        { count: 90, label: '3m', step: 'day', stepmode: 'backward' },
                        { count: 180, label: '6m', step: 'day', stepmode: 'backward' },
                        { step: 'all' }
                    ]
                },
                rangeslider: { visible: true },
                type: 'date'
            },
            yaxis: { autorange: true },
            showlegend: true
        };
        
        createChart(containerId, traces, layout);
    } catch (error) {
        console.error('Error loading wortkettle chart:', error);
    }
}

/**
 * 渲染冰水罐圖表
 */
async function renderIcewaterChart(containerId, days = DEFAULT_DAYS) {
    try {
        const data = await fetchIcewaterData(days);
        
        const traces = [
            {
                name: '體積',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.volume,
                line: { color: '#4ECDC4' }
            },
            {
                name: '馬達',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.pump,
                visible: 'legendonly',
                line: { color: '#FF6B6B' }
            }
        ];
        
        const layout = {
            title: '冰水罐監控',
            xaxis: {
                range: getInitialOneDayRange(data.timestamps),
                autorange: false,
                rangeselector: {
                    buttons: [
                        { count: 1, label: '1d', step: 'day', stepmode: 'backward' },
                        { count: 7, label: '1w', step: 'day', stepmode: 'backward' },
                        { count: 30, label: '1m', step: 'day', stepmode: 'backward' },
                        { count: 90, label: '3m', step: 'day', stepmode: 'backward' },
                        { count: 180, label: '6m', step: 'day', stepmode: 'backward' },
                        { step: 'all' }
                    ]
                },
                rangeslider: { visible: true },
                type: 'date'
            },
            yaxis: { autorange: true },
            showlegend: true
        };
        
        createChart(containerId, traces, layout);
    } catch (error) {
        console.error('Error loading icewater chart:', error);
    }
}

/**
 * 渲染冷媒罐圖表
 */
async function renderGlycolChart(containerId, tank = '1', days = DEFAULT_DAYS) {
    try {
        const data = await fetchGlycolData(tank, days);
        const coolerKey = tank === '1' ? 'cooler1' : 'cooler2';
        
        const traces = [
            {
                name: '溫度',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.temperature,
                line: { color: '#4ECDC4' }
            },
            {
                name: '設定溫度',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.setpoint,
                line: { color: '#95E1D3' }
            },
            {
                name: `製冷機${tank}`,
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data[coolerKey].map((v, i) => v * data.setpoint[i]),
                visible: 'legendonly',
                line: { color: '#FF6B6B' }
            },
            {
                name: '馬達',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.pump,
                visible: 'legendonly',
                line: { color: '#FFA500' }
            }
        ];
        
        const layout = {
            title: `冷媒罐 ${tank} 監控`,
            xaxis: {
                range: getInitialOneDayRange(data.timestamps),
                autorange: false,
                rangeselector: {
                    buttons: [
                        { count: 1, label: '1d', step: 'day', stepmode: 'backward' },
                        { count: 7, label: '1w', step: 'day', stepmode: 'backward' },
                        { count: 30, label: '1m', step: 'day', stepmode: 'backward' },
                        { count: 90, label: '3m', step: 'day', stepmode: 'backward' },
                        { count: 180, label: '6m', step: 'day', stepmode: 'backward' },
                        { step: 'all' }
                    ]
                },
                rangeslider: { visible: true },
                type: 'date'
            },
            yaxis: { autorange: true },
            showlegend: true
        };
        
        createChart(containerId, traces, layout);
    } catch (error) {
        console.error('Error loading glycol chart:', error);
    }
}

/**
 * 渲染發酵罐圖表
 */
async function renderFvChart(containerId, fvNumber, days = DEFAULT_DAYS) {
    try {
        // 如果 fvNumber 是字符串，轉換為數字
        if (typeof fvNumber === 'string') {
            fvNumber = parseInt(fvNumber);
        }
        const data = await fetchFvData(fvNumber, days);
        
        const traces = [
            {
                name: '溫度',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.temperature,
                line: { color: '#FF6B6B' }
            },
            {
                name: '設定溫度',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.setpoint,
                line: { color: '#4ECDC4' }
            },
            {
                name: '上電磁閥',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.setpoint.map((v, i) => v * data.valve1[i]),
                visible: 'legendonly',
                line: { color: '#FFA500' }
            },
            {
                name: '下電磁閥',
                type: 'scatter',
                mode: 'lines',
                x: data.timestamps,
                y: data.setpoint.map((v, i) => v * data.valve2[i]),
                visible: 'legendonly',
                line: { color: '#FFD93D' }
            }
        ];
        
        // FV17 以上有額外數據
        if (fvNumber >= 17) {
            traces.push(
                {
                    name: '壓力',
                    type: 'scatter',
                    mode: 'lines',
                    x: data.timestamps,
                    y: data.psi,
                    line: { color: '#95E1D3' }
                },
                {
                    name: '設定壓力',
                    type: 'scatter',
                    mode: 'lines',
                    x: data.timestamps,
                    y: data.psi_sp,
                    visible: 'legendonly',
                    line: { color: '#AA96DA' }
                },
                {
                    name: 'CO2 體積',
                    type: 'scatter',
                    mode: 'lines',
                    x: data.timestamps,
                    y: data.co2vol,
                    visible: 'legendonly',
                    line: { color: '#F38181' }
                },
                {
                    name: '設定 CO2 體積',
                    type: 'scatter',
                    mode: 'lines',
                    x: data.timestamps,
                    y: data.co2vol_sp,
                    visible: 'legendonly',
                    line: { color: '#6C5CE7' }
                },
                {
                    name: '洩壓閥',
                    type: 'scatter',
                    mode: 'lines',
                    x: data.timestamps,
                    y: data.psi_sp.map((v, i) => v * data.valve3[i]),
                    visible: 'legendonly',
                    line: { color: '#A8E6CF' }
                }
            );
        }
        
        const layout = {
            title: `發酵罐 ${fvNumber} 監控`,
            xaxis: {
                range: getInitialOneDayRange(data.timestamps),
                autorange: false,
                rangeselector: {
                    buttons: [
                        { count: 1, label: '1d', step: 'day', stepmode: 'backward' },
                        { count: 7, label: '1w', step: 'day', stepmode: 'backward' },
                        { count: 30, label: '1m', step: 'day', stepmode: 'backward' },
                        { count: 90, label: '3m', step: 'day', stepmode: 'backward' },
                        { count: 180, label: '6m', step: 'day', stepmode: 'backward' },
                        { step: 'all' }
                    ]
                },
                rangeslider: { visible: true },
                type: 'date'
            },
            yaxis: { autorange: true },
            showlegend: true
        };
        
        createChart(containerId, traces, layout);
    } catch (error) {
        console.error(`Error loading FV${fvNumber} chart:`, error);
    }
}

/**
 * 懶加載圖表 - 當圖表進入視圖時才渲染
 */
function setupLazyLoading() {
    const observerOptions = {
        root: null,
        rootMargin: '800px 0px',  // 提前 800px 開始加載，讓更多圖表預先加載
        threshold: 0.0  // 只要有任何交集就觸發
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const chartElement = entry.target;
                const renderFunction = chartElement.dataset.render;
                
                if (renderFunction) {
                    // 執行渲染函數
                    const renderConfig = JSON.parse(chartElement.dataset.config || '{}');
                    
                    // 根據渲染函數名稱決定參數
                    if (renderFunction === 'renderFvChart') {
                        window[renderFunction](chartElement.id, renderConfig.fvNumber, renderConfig.days || 1);
                    } else {
                        window[renderFunction](chartElement.id, renderConfig.days || 1);
                    }
                    
                    // 停止觀察
                    observer.unobserve(chartElement);
                }
            }
        });
    }, observerOptions);
    
    // 觀察所有需要懶加載的圖表容器
    document.querySelectorAll('.chart-container[data-render]').forEach(el => {
        observer.observe(el);
    });
}

// 頁面加載時初始化懶加載
document.addEventListener('DOMContentLoaded', () => {
    setupLazyLoading();
});

// 導出函數供全局使用
window.ChartRenderer = {
    renderHotwaterChart,
    renderMashlauterChart,
    renderWortkettleChart,
    renderIcewaterChart,
    renderGlycolChart,
    renderFvChart,
    setupLazyLoading
};
