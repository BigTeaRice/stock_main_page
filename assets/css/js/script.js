// 全局状态：存储报告列表、当前选中的股票符号
let g_reports = [];
let g_currentSymbol = '';

/**
 * 页面初始化：加载数据 → 渲染列表 → 绑定事件
 */
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // 1. 加载报告元数据（由main.py生成的reports.json）
        await loadReportsMetadata();
        // 2. 渲染报告列表到导航栏
        renderReportNav();
        // 3. 绑定股票符号按钮点击事件
        bindSymbolButtons();
        // 4. 默认显示第一个报告和图表
        if (g_reports.length > 0) {
            const defaultReport = g_reports[0];
            showReport(defaultReport);
            showChart(defaultReport.symbol);
            updateActiveStates(defaultReport.symbol);
        }
        // 5. 显示最后更新时间
        updateLastUpdateTime();
    } catch (err) {
        console.error('初始化失败:', err);
        showError('页面加载失败，请刷新重试');
    }
});

/**
 * 加载reports.json：获取所有报告的元数据（符号、标题、时间、路径）
 */
async function loadReportsMetadata() {
    const res = await fetch('reports/reports.json');
    if (!res.ok) throw new Error(`无法加载报告列表（状态码：${res.status}）`);
    g_reports = (await res.json()).reports || [];
}

/**
 * 渲染报告导航栏：将报告列表生成可点击的列表项
 */
function renderReportNav() {
    const navList = document.getElementById('report-nav-list');
    if (!navList) return;

    navList.innerHTML = ''; // 清空现有内容
    g_reports.forEach(report => {
        const li = document.createElement('li');
        li.className = 'report-nav-item';
        li.textContent = report.title;
        li.dataset.symbol = report.symbol;
        // 点击报告项：显示内容和图表
        li.addEventListener('click', () => {
            showReport(report);
            showChart(report.symbol);
            updateActiveStates(report.symbol);
        });
        navList.appendChild(li);
    });
}

/**
 * 绑定股票符号按钮：点击快速切换报告和图表
 */
function bindSymbolButtons() {
    const symbolBtns = document.querySelectorAll('.symbol-btn');
    symbolBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const symbol = btn.dataset.symbol;
            // 查找对应报告
            const targetReport = g_reports.find(r => r.symbol === symbol);
            if (targetReport) {
                showReport(targetReport);
                showChart(symbol);
                updateActiveStates(symbol);
            }
        });
    });
}

/**
 * 显示报告内容：从reports.json获取Markdown路径 → 解析为HTML
 * @param {Object} report - 报告元数据
 */
async function showReport(report) {
    try {
        // 高亮当前报告项
        document.querySelectorAll('.report-nav-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`.report-nav-item[data-symbol="${report.symbol}"]`).classList.add('active');

        // 加载Markdown内容
        const mdRes = await fetch(report.url);
        if (!mdRes.ok) throw new Error(`无法加载报告：${mdRes.status}`);
        const mdContent = await mdRes.text();

        // 解析Markdown为HTML（依赖marked库）
        const htmlContent = marked.parse(mdContent);
        document.getElementById('report-content').innerHTML = htmlContent;
    } catch (err) {
        console.error('显示报告失败:', err);
        showError('加载报告内容失败');
    }
}

/**
 * 显示股票图表：隐藏所有图表 → 显示选中的
 * @param {string} symbol - 股票符号（如AAPL、000001.SZ）
 */
function showChart(symbol) {
    // 隐藏所有图表
    document.querySelectorAll('.chart-item').forEach(item => {
        item.style.display = 'none';
    });
    // 显示当前股票图表
    const chartElem = document.getElementById(`chart-${symbol}`);
    if (chartElem) chartElem.style.display = 'block';
}

/**
 * 更新激活状态：高亮当前选中的报告/按钮
 * @param {string} activeSymbol - 当前激活的股票符号
 */
function updateActiveStates(activeSymbol) {
    // 更新符号按钮状态
    document.querySelectorAll('.symbol-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.symbol === activeSymbol) btn.classList.add('active');
    });
}

/**
 * 更新最后更新时间：显示最近一次报告的时间
 */
function updateLastUpdateTime() {
    if (g_reports.length > 0 && document.getElementById('last-update')) {
        document.getElementById('last-update').textContent = `最后更新：${g_reports[0].timestamp}`;
    }
}

/**
 * 显示错误提示：3秒后自动消失
 * @param {string} msg - 错误信息
 */
function showError(msg) {
    const errorElem = document.getElementById('error-message');
    if (errorElem) {
        errorElem.textContent = msg;
        errorElem.style.display = 'block';
        setTimeout(() => errorElem.style.display = 'none', 3000);
    }
}
