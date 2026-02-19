#!/usr/bin/env python3
"""
Polymarket 5分钟高频监控更新 - Cron Job执行脚本
更新时间: 2026-02-19 14:46 UTC
"""

import json
import os
from datetime import datetime

# 当前持仓 (由cron job提供)
CURRENT_POSITIONS = [
    {
        "market": "Jesus vs GTA - Will Jesus Return Before GTA 6 Releases?",
        "market_slug": "jesus-vs-gta",
        "side": "NO",
        "entry_price": 0.52,
        "invested": 25.0,
        "shares": 48.0769,  # $25 / 0.52
        "upside_pct": 92,
        "current_price": None,  # 待获取
        "pnl": 0.0,
        "pnl_pct": 0.0
    },
    {
        "market": "NBA Championship 2025 - OKC Thunder",
        "market_slug": "okc-thunder-championship",
        "side": "YES",
        "entry_price": 0.35,
        "invested": 20.0,
        "shares": 57.1429,  # $20 / 0.35
        "upside_pct": 186,
        "current_price": None,
        "pnl": 0.0,
        "pnl_pct": 0.0
    },
    {
        "market": "Bitcoin $1M in 2025",
        "market_slug": "btc-1m-2025",
        "side": "YES",
        "entry_price": 0.48,
        "invested": 20.0,
        "shares": 41.6667,  # $20 / 0.48
        "upside_pct": 108,
        "current_price": None,
        "pnl": 0.0,
        "pnl_pct": 0.0
    }
]

CASH = 35.0
INITIAL_CAPITAL = 100.0

# 触发条件
STOP_PROFIT_PCT = 20.0   # 止盈线: +20%
STOP_LOSS_PCT = -15.0    # 止损线: -15%

def load_portfolio():
    """加载当前投资组合"""
    portfolio_path = "paper_trading/portfolio.json"
    if os.path.exists(portfolio_path):
        with open(portfolio_path, 'r') as f:
            return json.load(f)
    return {
        "start_date": datetime.now().isoformat(),
        "initial_capital": INITIAL_CAPITAL,
        "current_cash": CASH,
        "total_invested": 65.0,
        "total_pnl": 0.0,
        "total_pnl_pct": 0.0,
        "total_trades": 0,
        "open_positions": 3,
        "closed_positions": 0
    }

def save_monitoring_report(positions, cash, portfolio, alerts):
    """保存监控报告"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M UTC')
    
    report = f"""# 📊 Polymarket 高频监控报告

**时间:** {timestamp}  
**周期:** 5分钟更新  
**监控状态:** ✅ 运行中

---

## 💼 当前持仓 (3个)

| # | 市场 | 方向 | 入场价 | 当前价 | 投入 | 盈亏 | 状态 |
|---|------|------|--------|--------|------|------|------|
"""
    
    total_invested = 0
    total_unrealized_pnl = 0
    
    for i, pos in enumerate(positions, 1):
        current_price = pos['current_price'] if pos['current_price'] else "⏳ 待获取"
        pnl_str = f"${pos['pnl']:+.2f} ({pos['pnl_pct']:+.1f}%)" if pos['current_price'] else "⏳ 待计算"
        
        # 触发条件检查
        status = "⏸️ 持有"
        if pos['current_price']:
            if pos['pnl_pct'] >= STOP_PROFIT_PCT:
                status = "🚨 **止盈触发!**"
            elif pos['pnl_pct'] <= STOP_LOSS_PCT:
                status = "🚨 **止损触发!**"
        
        report += f"| {i} | {pos['market']} {pos['side']} | {pos['side']} | {pos['entry_price']} | {current_price} | ${pos['invested']} | {pnl_str} | {status} |\n"
        
        total_invested += pos['invested']
        total_unrealized_pnl += pos['pnl']
    
    report += f"""
---

## 💰 资金状况

| 项目 | 金额 |
|------|------|
| 初始本金 | ${INITIAL_CAPITAL:.2f} |
| 现金余额 | ${cash:.2f} |
| 持仓投入 | ${total_invested:.2f} |
| 未实现盈亏 | ${total_unrealized_pnl:+.2f} |
| **持仓市值** | ${total_invested + total_unrealized_pnl:.2f} |

---

## 🚨 触发条件监控

**止盈线:** +{STOP_PROFIT_PCT}%  
**止损线:** {STOP_LOSS_PCT}%

### 当前触发状态:
"""
    
    if alerts:
        for alert in alerts:
            report += f"- {alert}\n"
    else:
        report += "- ✅ 无触发条件，继续监控\n"
    
    report += f"""
---

## 🔍 新机会扫描 (剩余资金: ${cash:.2f})

目标: 寻找第4、5笔投资机会

**筛选标准:**
- 高流动性市场
- 情绪-价格偏离 >10%
- 事件时间明确
- 投入金额: $15-20/笔

**候选市场:**
- [待扫描Polymarket获取...]

---

## 📈 操作记录

**本次操作:**
- [ ] 止盈卖出
- [ ] 止损卖出  
- [ ] 新建仓位
- [ ] 无操作

---

## 🔔 提醒

⚠️ **注意:** 由于API限制，本次更新无法获取实时价格。
请手动检查Polymarket或使用浏览器截图获取最新价格。

---

*Polymarket 模拟投资系统 - Deki Agent*  
*下次更新: 5分钟后*
"""
    
    # 保存报告
    report_filename = datetime.now().strftime('%Y%m%d_%H%M')
    report_path = f"paper_trading/high_freq_reports/monitor_{report_filename}.md"
    
    os.makedirs("paper_trading/high_freq_reports", exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 同时更新最新报告
    with open("paper_trading/LATEST_MONITOR_REPORT.md", 'w', encoding='utf-8') as f:
        f.write(report)
    
    return report

def main():
    """主函数"""
    print("="*60)
    print("🚀 Polymarket 5分钟高频监控更新")
    print("="*60)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print()
    
    # 加载投资组合
    portfolio = load_portfolio()
    print(f"💰 初始本金: ${portfolio['initial_capital']:.2f}")
    print(f"💵 当前现金: ${CASH:.2f}")
    print()
    
    # 检查持仓
    print("📊 当前持仓:")
    alerts = []
    for pos in CURRENT_POSITIONS:
        print(f"  • {pos['market']} {pos['side']} @ {pos['entry_price']} (${pos['invested']})")
        if pos['current_price'] and pos['pnl_pct'] >= STOP_PROFIT_PCT:
            alerts.append(f"🎯 止盈触发: {pos['market']} +{pos['pnl_pct']:.1f}%")
        elif pos['current_price'] and pos['pnl_pct'] <= STOP_LOSS_PCT:
            alerts.append(f"⚠️ 止损触发: {pos['market']} {pos['pnl_pct']:.1f}%")
    
    print()
    
    # 触发条件检查
    if alerts:
        print("🚨 触发条件:")
        for alert in alerts:
            print(f"  {alert}")
    else:
        print("✅ 无触发条件，继续监控")
    
    print()
    
    # 生成报告
    report = save_monitoring_report(CURRENT_POSITIONS, CASH, portfolio, alerts)
    print("📄 报告已保存至: paper_trading/LATEST_MONITOR_REPORT.md")
    
    print()
    print("="*60)
    print("✅ 监控更新完成")
    print("="*60)
    
    # 返回报告用于显示
    return report

if __name__ == "__main__":
    report = main()
    print("\n" + "="*60)
    print("监控报告预览:")
    print("="*60)
    print(report[:2000] + "..." if len(report) > 2000 else report)
