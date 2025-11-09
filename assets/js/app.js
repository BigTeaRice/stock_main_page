document.addEventListener('DOMContentLoaded', async () => {
    // 加载报告列表
    const reports = await fetchReports();
    renderReportList(reports);
    
    // 绑定点击事件
    document.querySelectorAll('.report-link').forEach(link => {
        link.addEventListener('click', async (e) => {
            e.preventDefault();
            const symbol = link.dataset.symbol;
            await showReport(symbol);
        });
    });
});

async function fetchReports() {
    const response = await fetch('/reports.json');
    return response.json().reports;
}

function renderReportList(reports) {
    const list = document.getElementById('report-list');
    list.innerHTML = '';
    
    reports.forEach(report => {
        const li = document.createElement('li');
        const link = document.createElement('a');
        link.href = `/reports/${report.filename}`;
        link.textContent = `${report.symbol} (${report.period})`;
        link.dataset.symbol = report.symbol;
        li.appendChild(link);
        list.appendChild(li);
    });
}

async function showReport(symbol) {
    const reportPath = `/reports/${symbol}_report_latest.html`;
    const chartPath = `/charts/${symbol}_latest.png`;
    
    // 动态加载内容
    document.getElementById('report-content').innerHTML = '<div class="loading">Loading...</div>';
    document.getElementById('chart-container').innerHTML = '';
    
    try {
        const reportHtml = await fetch(reportPath).then(res => res.text());
        document.getElementById('report-content').innerHTML = reportHtml;
    } catch (error) {
        showError('Failed to load report');
    }
}

function showError(message) {
    alert(message);
}
