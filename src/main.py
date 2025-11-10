"""
主程序 - 简化版本
"""

import argparse
import sys
import os
import logging

# 添加src目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_fetcher import DataFetcher
from analyzer import StockAnalyzer
from visualizer import ChartVisualizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='股票分析系统')
    parser.add_argument('--symbol', nargs='+', help='股票代码')
    parser.add_argument('--days', type=int, default=30, help='分析天数')
    parser.add_argument('--test-mode', action='store_true', help='测试模式')
    
    args = parser.parse_args()
    
    if not args.symbol:
        logger.error("请指定股票代码")
        return 1
    
    # 初始化组件
    fetcher = DataFetcher()
    analyzer = StockAnalyzer()
    visualizer = ChartVisualizer()
    
    # 获取数据
    for symbol in args.symbol:
        logger.info(f"分析 {symbol}")
        
        df = fetcher.get_stock_data(symbol, args.days, args.test_mode)
        if df is not None:
            result = analyzer.technical_analysis(df, symbol)
            chart_path = visualizer.create_stock_chart(df, result, symbol)
            
            logger.info(f"完成 {symbol} 分析: {result.recommendation}")
    
    logger.info("分析完成")
    return 0

if __name__ == "__main__":
    sys.exit(main())
