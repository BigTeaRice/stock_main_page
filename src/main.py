import os
from datetime import datetime
from data_fetcher import fetch_stock_data
from analyzer import StockAnalyzer
from visualizer import generate_report, save_chart

# 配置参数
SYMBOLS = ['AAPL', '000001.SZ', 'TSLA']  # 监控的股票列表
PERIOD = '1mo'                           # 数据周期
OUTPUT_DIR = 'charts'                    # 图表输出目录

def main():
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 获取当前时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 分析每支股票
    for symbol in SYMBOLS:
        print(f"Processing {symbol}...")
        
        # 获取数据
        data = fetch_stock_data(symbol, PERIOD)
        if not data:
            print(f"Failed to fetch data for {symbol}")
            continue
            
        # 运行分析
        analyzer = StockAnalyzer(data)
        report = analyzer.generate_report()
        
        # 生成图表
        chart_path = f"{OUTPUT_DIR}/{symbol}_{timestamp}.png"
        save_chart(analyzer.chart_data, chart_path)
        
        # 生成报告
        report_path = f"reports/{symbol}_report_{timestamp}.md"
        generate_report(report, chart_path, report_path)
        
    print("Analysis completed!")

if __name__ == "__main__":
    main()
