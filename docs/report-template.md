# 股票分析报告 - {{ symbol }}

## 摘要
- **当前价格**: {{ current_price }} {{ currency }}
- **涨跌幅**: {{ change_pct }}%
- **成交量**: {{ volume }}
- **RSI**: {{ rsi }}
- **MACD**: {{ macd_diff }}

## 价格走势


## 技术指标
| 指标       | 值       | 状态       |
|------------|----------|------------|
| MA5        | {{ ma5 }}|            |
| MA10       | {{ ma10 }}|            |
| MA20       | {{ ma20 }}|            |
| RSI        | {{ rsi }}| {{ rsi_status }} |
| MACD       | {{ macd_diff }} |            |

## 数据统计
- 数据周期: {{ period }}
- 数据点数: {{ data_points }}
- 更新时间: {{ timestamp }}
