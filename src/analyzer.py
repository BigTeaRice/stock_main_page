import pandas as pd
import talib as ta

class StockAnalyzer:
    def __init__(self, symbol, data):
        self.symbol = symbol
        self.data = data
        self.chart_data = self.prepare_chart_data()
        
    def prepare_chart_data(self):
        # 计算技术指标
        closes = self.data['Close'].values
        highs = self.data['High'].values
        lows = self.data['Low'].values
        opens = self.data['Open'].values
        
        # 移动平均线
        ma5 = ta.SMA(closes, timeperiod=5)
        ma10 = ta.SMA(closes, timeperiod=10)
        ma20 = ta.SMA(closes, timeperiod=20)
        
        # RSI
        rsi = ta.RSI(closes, timeperiod=14)
        
        # MACD
        macd, macdsignal, macdhist = ta.MACD(closes, fastperiod=12, slowperiod=26, signalperiod=9)
        
        # 布林带
        upper, middle, lower = ta.BBANDS(closes, timeperiod=20)
        
        # 合并数据
        chart_data = self.data.copy()
        chart_data['MA5'] = ma5
        chart_data['MA10'] = ma10
        chart_data['MA20'] = ma20
        chart_data['RSI'] = rsi
        chart_data['MACD'] = macd
        chart_data['MACD_Signal'] = macdsignal
        chart_data['BB_Upper'] = upper
        chart_data['BB_Lower'] = lower
        
        return chart_data
    
    def generate_report(self):
        # 生成关键指标摘要
        summary = {
            'symbol': self.symbol,
            'current_price': self.data['Close'].iloc[-1],
            'change_pct': (self.data['Close'].iloc[-1] - self.data['Close'].iloc[0]) / self.data['Close'].iloc[0] * 100,
            'volume': self.data['Volume'].iloc[-1],
            'rsi': self.chart_data['RSI'].iloc[-1],
            'macd_diff': self.chart_data['MACD'].iloc[-1] - self.chart_data['MACD_Signal'].iloc[-1]
        }
        
        return summary
