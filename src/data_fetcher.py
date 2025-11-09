import yfinance as yf
import akshare as ak

def fetch_stock_data(symbol, period):
    try:
        # 尝试使用yfinance获取国际股票数据
        ticker = yf.Ticker(symbol)
        if ticker.history(period=period).empty:
            raise ValueError("No data found")
        return ticker.history(period=period).reset_index()
    
    except Exception as e:
        print(f"Error fetching from yfinance: {str(e)}")
        
        try:
            # 尝试使用AkShare获取A股数据
            if symbol.startswith('6'):
                symbol_ak = f"sh{symbol}"
            else:
                symbol_ak = f"sz{symbol}"
                
            df = ak.stock_zh_a_hist(
                symbol=symbol_ak,
                period="daily",
                start_date=datetime.now().strftime("%Y%m%d"),
                end_date=datetime.now().strftime("%Y%m%d"),
                adjust=""
            )
            return df.rename(columns={
                '日期': 'Date',
                '开盘': 'Open',
                '最高': 'High',
                '最低': 'Low',
                '收盘': 'Close',
                '成交量': 'Volume'
            }).sort_values('Date')
            
        except Exception as e:
            print(f"Error fetching from akshare: {str(e)}")
            return None
