#!/usr/bin/env python3
"""
股票分析工具 - GitHub兼容版本
集成yfinance和AkShare API的完整股票分析解决方案
适用于GitHub Actions和静态环境运行
"""

import yfinance as yf
import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class StockAnalyzer:
    """股票分析器主类"""
    
    def __init__(self):
        self.data_source = "yfinance"  # 默认数据源
        self.cache_data = {}  # 数据缓存
        
    def set_data_source(self, source):
        """设置数据源"""
        valid_sources = ["yfinance", "akshare", "simulated"]
        if source in valid_sources:
            self.data_source = source
            return True
        return False
    
    def fetch_stock_data(self, symbol, period="3mo"):
        """获取股票数据"""
        print(f"🔍 从 {self.data_source} 获取 {symbol} 的 {period} 数据...")
        
        try:
            if self.data_source == "yfinance":
                return self._fetch_yfinance_data(symbol, period)
            elif self.data_source == "akshare":
                return self._fetch_akshare_data(symbol, period)
            else:
                return self._generate_simulated_data(symbol, period)
        except Exception as e:
            print(f"❌ 数据获取失败: {e}")
            return None
    
    def _fetch_yfinance_data(self, symbol, period):
        """从yfinance获取国际股票数据"""
        try:
            # 添加常见后缀
            if not any(symbol.endswith(suffix) for suffix in ['.SI', '.HK', '.TW', '.SS', '.SZ']):
                symbol_clean = symbol
            else:
                symbol_clean = symbol
            
            ticker = yf.Ticker(symbol_clean)
            hist = ticker.history(period=period)
            
            if hist.empty:
                # 尝试常见后缀
                for suffix in ['.SI', '.HK']:
                    try:
                        ticker = yf.Ticker(symbol + suffix)
                        hist = ticker.history(period=period)
                        if not hist.empty:
                            symbol += suffix
                            break
                    except:
                        continue
            
            if hist.empty:
                raise ValueError("未找到股票数据")
            
            # 处理数据格式
            hist = hist.reset_index()
            hist['Date'] = pd.to_datetime(hist['Date'])
            hist = hist.rename(columns={
                'Date': 'date',
                'Open': 'open',
                'High': 'high', 
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            })
            
            return {
                'symbol': symbol,
                'data': hist[['date', 'open', 'high', 'low', 'close', 'volume']],
                'info': ticker.info,
                'source': 'yfinance'
            }
            
        except Exception as e:
            print(f"yfinance数据获取失败: {e}")
            return self._generate_simulated_data(symbol, period)
    
    def _fetch_akshare_data(self, symbol, period):
        """从AkShare获取A股数据"""
        try:
            # 处理A股代码格式
            if symbol.startswith('6'):
                symbol_ak = f"sh{symbol}"
            elif symbol.startswith('0') or symbol.startswith('3'):
                symbol_ak = f"sz{symbol}"
            else:
                symbol_ak = symbol
            
            # 计算时间范围
            end_date = datetime.now().strftime('%Y%m%d')
            if period == "1mo":
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            elif period == "3mo":
                start_date = (datetime.now() - timedelta(days=90)).strftime('%Y%m%d')
            elif period == "6mo":
                start_date = (datetime.now() - timedelta(days=180)).strftime('%Y%m%d')
            elif period == "1y":
                start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
            else:
                start_date = (datetime.now() - timedelta(days=90)).strftime('%Y%m%d')
            
            # 获取A股数据
            stock_data = ak.stock_zh_a_hist(symbol=symbol_ak[2:], 
                                          period="daily", 
                                          start_date=start_date, 
                                          end_date=end_date,
                                          adjust="")
            
            if stock_data.empty:
                raise ValueError("AkShare未找到股票数据")
            
            # 处理数据格式
            stock_data = stock_data.rename(columns={
                '日期': 'date',
                '开盘': 'open',
                '最高': 'high',
                '最低': 'low', 
                '收盘': 'close',
                '成交量': 'volume'
            })
            
            stock_data['date'] = pd.to_datetime(stock_data['date'])
            
            return {
                'symbol': symbol,
                'data': stock_data[['date', 'open', 'high', 'low', 'close', 'volume']],
                'info': {'currency': 'CNY', 'exchange': 'SSE/SZSE'},
                'source': 'akshare'
            }
            
        except Exception as e:
            print(f"AkShare数据获取失败: {e}")
            return self._generate_simulated_data(symbol, period)
    
    def _generate_simulated_data(self, symbol, period):
        """生成模拟数据（备用）"""
        print("📊 使用模拟数据...")
        
        # 根据周期确定数据点数
        periods = {
            "1d": 1, "5d": 5, "1mo": 21, "3mo": 63, 
            "6mo": 126, "1y": 252, "2y": 504
        }
        n_points = periods.get(period, 63)
        
        # 生成日期范围
        end_date = datetime.now()
        dates = pd.date_range(end=end_date, periods=n_points, freq='D')
        
        # 生成价格数据
        base_price = 100 + np.random.random() * 50
        returns = np.random.normal(0, 0.02, n_points)
        prices = base_price * np.exp(np.cumsum(returns))
        
        # 生成OHLC数据
        data = []
        for i, date in enumerate(dates):
            close = prices[i]
            open_price = close * (1 + np.random.normal(0, 0.01))
            high = max(open_price, close) * (1 + abs(np.random.normal(0, 0.015)))
            low = min(open_price, close) * (1 - abs(np.random.normal(0, 0.015)))
            volume = np.random.randint(1000000, 10000000)
            
            data.append({
                'date': date,
                'open': max(open_price, 0.01),
                'high': max(high, 0.01),
                'low': max(low, 0.01),
                'close': max(close, 0.01),
                'volume': volume
            })
        
        df = pd.DataFrame(data)
        return {
            'symbol': symbol,
            'data': df,
            'info': {'currency': 'USD', 'exchange': 'SIMULATED'},
            'source': 'simulated'
        }
    
    def calculate_technical_indicators(self, df):
        """计算技术指标"""
        closes = df['close'].values
        highs = df['high'].values
        lows = df['low'].values
        opens = df['open'].values
        
        # 移动平均线
        df['MA5'] = df['close'].rolling(window=5).mean()
        df['MA10'] = df['close'].rolling(window=10).mean()
        df['MA20'] = df['close'].rolling(window=20).mean()
        
        # RSI
        df['RSI'] = self._calculate_rsi(closes, 14)
        
        # MACD
        exp1 = df['close'].ewm(span=12).mean()
        exp2 = df['close'].ewm(span=26).mean()
        df['MACD'] = exp1 - exp2
        df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
        
        # 布林带
        df['BB_Middle'] = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        # 成交量指标
        df['Volume_MA20'] = df['volume'].rolling(window=20).mean()
        
        return df
    
    def _calculate_rsi(self, prices, period=14):
        """计算RSI指标"""
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gains = np.zeros_like(prices)
        avg_losses = np.zeros_like(prices)
        
        # 初始值
        avg_gains[period] = np.mean(gains[:period])
        avg_losses[period] = np.mean(losses[:period])
        
        # 计算RSI
        for i in range(period+1, len(prices)):
            avg_gains[i] = (avg_gains[i-1] * (period-1) + gains[i-1]) / period
            avg_losses[i] = (avg_losses[i-1] * (period-1) + losses[i-1]) / period
        
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))
        rsi[:period] = 50  # 前period个数据设为50
        
        return rsi
    
    def generate_report(self, stock_data, indicators_df):
        """生成分析报告"""
        current_price = stock_data['data']['close'].iloc[-1]
        prev_price = stock_data['data']['close'].iloc[-2] if len(stock_data['data']) > 1 else current_price
        change = current_price - prev_price
        change_pct = (change / prev_price) * 100
        
        report = {
            'symbol': stock_data['symbol'],
            'current_price': current_price,
            'change': change,
            'change_pct': change_pct,
            'volume': stock_data['data']['volume'].iloc[-1],
            'data_points': len(stock_data['data']),
            'source': stock_data['source'],
            'currency': stock_data['info'].get('currency', 'USD'),
            'exchange': stock_data['info'].get('exchange', 'Unknown'),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 技术指标状态
        if not indicators_df.empty:
            latest = indicators_df.iloc[-1]
            report.update({
                'ma5': latest.get('MA5', None),
                'ma10': latest.get('MA10', None),
                'ma20': latest.get('MA20', None),
                'rsi': latest.get('RSI', None),
                'macd': latest.get('MACD', None),
                'bb_upper': latest.get('BB_Upper', None),
                'bb_lower': latest.get('BB_Lower', None)
            })
        
        return report
    
    def plot_stock_chart(self, stock_data, indicators_df, save_path=None):
        """绘制股票图表"""
        plt.style.use('seaborn-v0_8')
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), 
                                      gridspec_kw={'height_ratios': [3, 1]})
        
        df = stock_data['data']
        
        # K线图
        for i in range(len(df)):
            date = df['date'].iloc[i]
            open_p = df['open'].iloc[i]
            high = df['high'].iloc[i]
            low = df['low'].iloc[i]
            close = df['close'].iloc[i]
            
            color = 'red' if close > open_p else 'green'
            ax1.vlines(x=date, ymin=low, ymax=high, color=color, linewidth=1)
            ax1.vlines(x=date, ymin=min(open_p, close), ymax=max(open_p, close), 
                      color=color, linewidth=6)
        
        # 移动平均线
        if 'MA5' in indicators_df.columns:
            ax1.plot(df['date'], indicators_df['MA5'], label='MA5', linewidth=1, alpha=0.8)
        if 'MA20' in indicators_df.columns:
            ax1.plot(df['date'], indicators_df['MA20'], label='MA20', linewidth=1, alpha=0.8)
        
        ax1.set_title(f"{stock_data['symbol']} 股票价格走势", fontsize=14, fontweight='bold')
        ax1.set_ylabel('价格', fontsize=12)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 成交量
        colors = ['green' if df['close'].iloc[i] >= df['open'].iloc[i] else 'red' 
                 for i in range(len(df))]
        ax2.bar(df['date'], df['volume'], color=colors, alpha=0.7)
        ax2.set_ylabel('成交量', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        # 日期格式
        for ax in [ax1, ax2]:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
            ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📈 图表已保存至: {save_path}")
        else:
            plt.show()
        
        return fig

def main():
    """主函数 - 示例用法"""
    analyzer = StockAnalyzer()
    
    # 测试不同数据源
    test_cases = [
        {"symbol": "AAPL", "source": "yfinance", "period": "3mo"},
        {"symbol": "000001", "source": "akshare", "period": "3mo"},
        {"symbol": "TEST", "source": "simulated", "period": "1mo"}
    ]
    
    for i, test in enumerate(test_cases):
        print(f"\n{'='*50}")
        print(f"测试案例 {i+1}: {test['symbol']} ({test['source']})")
        print(f"{'='*50}")
        
        # 设置数据源
        analyzer.set_data_source(test['source'])
        
        # 获取数据
        stock_data = analyzer.fetch_stock_data(test['symbol'], test['period'])
        
        if stock_data is not None:
            # 计算技术指标
            indicators_df = analyzer.calculate_technical_indicators(stock_data['data'])
            
            # 生成报告
            report = analyzer.generate_report(stock_data, indicators_df)
            
            # 打印报告
            print(f"📊 股票代码: {report['symbol']}")
            print(f"💰 当前价格: {report['current_price']:.2f} {report['currency']}")
            print(f"📈 涨跌幅: {report['change_pct']:+.2f}%")
            print(f"📅 数据点数: {report['data_points']}")
            print(f"🌐 数据源: {report['source']}")
            print(f"⏰ 更新时间: {report['timestamp']}")
            
            if report['rsi'] is not None:
                rsi_status = "超买" if report['rsi'] > 70 else "超卖" if report['rsi'] < 30 else "正常"
                print(f"📊 RSI(14): {report['rsi']:.1f} ({rsi_status})")
            
            # 绘制图表（保存为文件）
            chart_path = f"stock_chart_{test['symbol']}_{i+1}.png"
            analyzer.plot_stock_chart(stock_data, indicators_df, chart_path)
            
        print(f"{'='*50}")

if __name__ == "__main__":
    print("🚀 股票分析工具启动...")
    print("📋 功能说明:")
    print("   - 支持 yfinance (国际股票)")
    print("   - 支持 AkShare (A股数据)") 
    print("   - 内置模拟数据引擎")
    print("   - 完整技术指标计算")
    print("   - 自动图表生成")
    print()
    
    main()
    
    print("\n✅ 所有测试完成!")
    print("💡 使用方法:")
    print("   1. 修改测试案例中的股票代码")
    print("   2. 调整数据源 (yfinance/akshare/simulated)")
    print("   3. 设置时间范围 (1mo/3mo/1y等)")
    print("   4. 运行 python stock_analysis_github.py")
