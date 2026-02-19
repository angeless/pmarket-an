#!/usr/bin/env python3
"""
模拟投资每日交易计划
本金 $100，一周高频交易
"""

from paper_trading_system import PaperTradingSystem
from datetime import datetime
import json

# 启动模拟投资系统
system = PaperTradingSystem(initial_capital=100.0)

print("""
🚀 Polymarket 模拟投资系统启动
================================

💰 初始本金: $100 USD
📅 交易周期: 7天
🎯 目标: 高频寻找赚钱机会

================================

本周重点监控事件:
1. 美联储利率决议 (如果在这周内)
2. 每日加密货币短期涨跌
3. 体育/政治事件

交易规则:
- 单笔交易不超过本金的 30% ($30)
- 每日最多 5 笔交易
- 止损线: -15%
- 盈利提取: 每日结算时提取 50% 利润

记录要求:
- 买入时必须记录理由和截图
- 卖出时必须记录理由和截图
- 每日生成交易报告

================================

使用命令:
from paper_trading_system import PaperTradingSystem
system = PaperTradingSystem(initial_capital=100.0)

# 买入示例
system.buy(
    market="Bitcoin Up or Down - Feb 19",
    side="YES",
    price=0.52,
    amount=30.0,
    reason="技术指标显示上涨趋势，社交媒体情绪看涨",
    screenshot="buy_btc_20260219_103000.png"
)

# 卖出示例  
system.sell(
    market="Bitcoin Up or Down - Feb 19",
    side="YES",
    exit_price=0.58,
    reason="达到目标收益 11.5%，止盈离场",
    screenshot="sell_btc_20260219_143000.png"
)

# 更新价格
system.update_prices({
    "Bitcoin Up or Down - Feb 19": 0.55,
    "Ethereum Up or Down - Feb 19": 0.48
})

# 生成日报
report = system.generate_daily_report()
print(report)

# 查看组合
summary = system.get_portfolio_summary()
print(json.dumps(summary, indent=2))
""")

# 初始化今日交易计划
today_plan = {
    "date": datetime.now().strftime("%Y-%m-%d"),
    "target_trades": 3,
    "max_risk_per_trade": 30.0,
    "focus_markets": [
        "加密货币短期涨跌",
        "体育事件",
        "政治事件"
    ],
    "strategy": "寻找情绪-价格偏离 >10% 的机会",
    "notes": ""
}

# 保存今日计划
with open("paper_trading/today_plan.json", "w") as f:
    json.dump(today_plan, f, indent=2)

print(f"\n✅ 今日交易计划已保存: paper_trading/today_plan.json")
print(f"📅 日期: {today_plan['date']}")
print(f"🎯 目标交易数: {today_plan['target_trades']}")
print(f"💰 单笔最大风险: ${today_plan['max_risk_per_trade']}")
