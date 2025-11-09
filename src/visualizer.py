import plotly.graph_objects as go
from plotly.subplots import make_subplots

def generate_chart(chart_data, filename):
    # 创建组合图表
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        specs=[[{"secondary_y": True}], [{"secondary_y": False}]]
    )
    
    # 添加K线图
    fig.add_trace(
        go.Candlestick(
            x=chart_data['Date'],
            open=chart_data['Open'],
            high=chart_data['High'],
            low=chart_data['Low'],
            close=chart_data['Close'],
            name='Price'
        ),
        row=1, col=1
    )
    
    # 添加移动平均线
    fig.add_trace(
        go.Scatter(
            x=chart_data['Date'],
            y=chart_data['MA5'],
            mode='lines',
            name='MA5',
            line=dict(color='blue', width=1)
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=chart_data['Date'],
            y=chart_data['MA10'],
            mode='lines',
            name='MA10',
            line=dict(color='orange', width=1)
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=chart_data['Date'],
            y=chart_data['MA20'],
            mode='lines',
            name='MA20',
            line=dict(color='green', width=1)
        ),
        row=1, col=1
    )
    
    # 添加成交量柱状图
    fig.add_trace(
        go.Bar(
            x=chart_data['Date'],
            y=chart_data['Volume'],
            name='Volume',
            marker_color='rgba(255, 165, 0, 0.5)',
            yaxis='y2'
        ),
        row=2, col=1
    )
    
    # 添加RSI指标
    fig.add_trace(
        go.Scatter(
            x=chart_data['Date'],
            y=chart_data['RSI'],
            mode='lines',
            name='RSI',
            line=dict(color='red', width=1),
            yaxis='y3'
        ),
        row=2, col=1
    )
    
    # 添加MACD指标
    fig.add_trace(
        go.Scatter(
            x=chart_data['Date'],
            y=chart_data['MACD'],
            mode='lines',
            name='MACD',
            line=dict(color='purple', width=1),
            yaxis='y4'
        ),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=chart_data['Date'],
            y=chart_data['MACD_Signal'],
            mode='lines',
            name='Signal Line',
            line=dict(color='blue', width=1),
            yaxis='y4'
        ),
        row=2, col=1
    )
    
    # 布局设置
    fig.update_layout(
        title_text=f"{self.symbol} Stock Analysis",
        xaxis_rangeslider_visible=False,
        height=800,
        width=1200,
        template='plotly_dark'
    )
    
    # 保存图表
    fig.write_image(filename, format='png', scale=2)
