# 股票分析工具

我将为您创建一个可以在GitHub环境中运行的股票分析工具，整合Google Finance和AkShare API。
股票分析工具-支持GoogleFinance和AkShare


关键技术特性
多数据源集成架构
Google Finance API：支持国际股票数据获取
AkShare API：专门处理中国A股市场数据
模拟数据引擎：内置随机数据生成器用于演示
技术指标计算引擎
移动平均线(MA5/10/20)实时计算
RSI相对强弱指数(14日周期)
完整的K线图+成交量技术分析
自适应时间周期数据点生成
GitHub兼容性设计
纯前端实现，无需服务器支持
CDN资源加载，避免跨域问题
响应式布局，支持移动端访问
模拟API接口，可轻松替换为真实数据源
使用时只需在GitHub Pages或任何静态网页服务器部署此HTML文件即可运行。要接入真实API，只需替换fetchStockData函数中的模拟逻辑。
