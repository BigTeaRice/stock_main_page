"""
股票分析系统核心包

此包包含数据获取、分析和可视化核心模块
"""

# 导入核心模块（按需启用）
from .data_fetcher import fetch_stock_data
from .analyzer import StockAnalyzer
from .visualizer import generate_chart
from .utils import save_report

# 定义包级常量
PACKAGE_NAME = "stock-analysis"
VERSION = "1.0.0"

# 包初始化逻辑（可选）
def __init_package__():
    print(f"[{PACKAGE_NAME}] v{VERSION} 初始化完成")

# 自动执行初始化
__init_package__()
