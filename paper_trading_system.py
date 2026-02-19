#!/usr/bin/env python3
"""
Polymarket 模拟投资系统
本金: $100 USD
周期: 7天高频交易
记录所有买卖操作和收益
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class Trade:
    """交易记录"""
    trade_id: str
    timestamp: str
    market: str
    action: str  # BUY or SELL
    side: str    # YES or NO
    price: float
    amount: float  # 投入金额
    shares: float  # 购买份额
    reason: str    # 交易理由
    screenshot: str = ""  # 截图文件名
    
@dataclass
class Position:
    """持仓记录"""
    market: str
    side: str
    entry_price: float
    shares: float
    invested: float
    current_price: float = 0.0
    pnl: float = 0.0
    pnl_pct: float = 0.0
    status: str = "OPEN"  # OPEN or CLOSED

class PaperTradingSystem:
    """模拟投资系统"""
    
    def __init__(self, initial_capital: float = 100.0):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions: List[Position] = []
        self.trades: List[Trade] = []
        self.daily_records: List[Dict] = []
        self.start_date = datetime.now()
        self.trade_counter = 0
        
        # 创建记录目录
        os.makedirs("paper_trading/trades", exist_ok=True)
        os.makedirs("paper_trading/screenshots", exist_ok=True)
        os.makedirs("paper_trading/daily_reports", exist_ok=True)
        
        # 初始化投资组合
        self.portfolio = {
            "start_date": self.start_date.isoformat(),
            "initial_capital": initial_capital,
            "current_cash": initial_capital,
            "total_invested": 0.0,
            "total_pnl": 0.0,
            "total_pnl_pct": 0.0,
            "total_trades": 0,
            "open_positions": 0,
            "closed_positions": 0
        }
        
        self._save_portfolio()
        print(f"🚀 模拟投资系统启动")
        print(f"💰 初始本金: ${initial_capital}")
        print(f"📅 开始日期: {self.start_date.strftime('%Y-%m-%d')}")
    
    def _generate_trade_id(self) -> str:
        """生成交易ID"""
        self.trade_counter += 1
        return f"TRADE_{self.start_date.strftime('%Y%m%d')}_{self.trade_counter:03d}"
    
    def _save_portfolio(self):
        """保存投资组合状态"""
        with open("paper_trading/portfolio.json", "w", encoding="utf-8") as f:
            json.dump(self.portfolio, f, ensure_ascii=False, indent=2)
    
    def _save_trade(self, trade: Trade):
        """保存交易记录"""
        filename = f"paper_trading/trades/{trade.trade_id}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(asdict(trade), f, ensure_ascii=False, indent=2)
    
    def buy(self, market: str, side: str, price: float, amount: float, 
            reason: str, screenshot: str = "") -> Optional[Trade]:
        """买入操作"""
        
        if amount > self.cash:
            print(f"❌ 资金不足: 需要 ${amount}, 可用 ${self.cash}")
            return None
        
        # 计算购买份额
        shares = amount / price
        
        # 创建交易记录
        trade = Trade(
            trade_id=self._generate_trade_id(),
            timestamp=datetime.now().isoformat(),
            market=market,
            action="BUY",
            side=side,
            price=price,
            amount=amount,
            shares=shares,
            reason=reason,
            screenshot=screenshot
        )
        
        # 更新现金
        self.cash -= amount
        
        # 创建持仓
        position = Position(
            market=market,
            side=side,
            entry_price=price,
            shares=shares,
            invested=amount,
            current_price=price
        )
        
        self.positions.append(position)
        self.trades.append(trade)
        
        # 更新投资组合
        self.portfolio["current_cash"] = self.cash
        self.portfolio["total_invested"] += amount
        self.portfolio["total_trades"] += 1
        self.portfolio["open_positions"] = len([p for p in self.positions if p.status == "OPEN"])
        
        self._save_portfolio()
        self._save_trade(trade)
        
        print(f"✅ 买入成功: {trade.trade_id}")
        print(f"   市场: {market}")
        print(f"   方向: {side} @ {price}")
        print(f"   投入: ${amount} -> {shares:.4f} 份")
        print(f"   理由: {reason}")
        print(f"   剩余现金: ${self.cash:.2f}")
        
        return trade
    
    def sell(self, market: str, side: str, exit_price: float, 
             reason: str, screenshot: str = "") -> Optional[Trade]:
        """卖出操作"""
        
        # 查找对应持仓
        position = None
        for p in self.positions:
            if p.market == market and p.side == side and p.status == "OPEN":
                position = p
                break
        
        if not position:
            print(f"❌ 未找到持仓: {market} {side}")
            return None
        
        # 计算收益
        exit_amount = position.shares * exit_price
        pnl = exit_amount - position.invested
        pnl_pct = (pnl / position.invested) * 100
        
        # 创建交易记录
        trade = Trade(
            trade_id=self._generate_trade_id(),
            timestamp=datetime.now().isoformat(),
            market=market,
            action="SELL",
            side=side,
            price=exit_price,
            amount=exit_amount,
            shares=position.shares,
            reason=reason,
            screenshot=screenshot
        )
        
        # 更新现金
        self.cash += exit_amount
        
        # 更新持仓状态
        position.current_price = exit_price
        position.pnl = pnl
        position.pnl_pct = pnl_pct
        position.status = "CLOSED"
        
        self.trades.append(trade)
        
        # 更新投资组合
        self.portfolio["current_cash"] = self.cash
        self.portfolio["total_pnl"] += pnl
        self.portfolio["total_trades"] += 1
        self.portfolio["closed_positions"] += 1
        self.portfolio["open_positions"] = len([p for p in self.positions if p.status == "OPEN"])
        
        # 计算总收益率
        total_value = self.cash + sum([p.shares * p.current_price for p in self.positions if p.status == "OPEN"])
        self.portfolio["total_pnl_pct"] = ((total_value - self.initial_capital) / self.initial_capital) * 100
        
        self._save_portfolio()
        self._save_trade(trade)
        
        print(f"✅ 卖出成功: {trade.trade_id}")
        print(f"   市场: {market}")
        print(f"   方向: {side} @ {exit_price}")
        print(f"   收回: ${exit_amount:.2f}")
        print(f"   盈亏: ${pnl:.2f} ({pnl_pct:+.2f}%)")
        print(f"   理由: {reason}")
        print(f"   当前现金: ${self.cash:.2f}")
        
        return trade
    
    def update_prices(self, prices: Dict[str, float]):
        """更新市场价格"""
        for position in self.positions:
            if position.status == "OPEN" and position.market in prices:
                position.current_price = prices[position.market]
                current_value = position.shares * position.current_price
                position.pnl = current_value - position.invested
                position.pnl_pct = (position.pnl / position.invested) * 100
        
        self._save_portfolio()
    
    def get_portfolio_summary(self) -> Dict:
        """获取投资组合摘要"""
        open_positions = [p for p in self.positions if p.status == "OPEN"]
        
        total_value = self.cash
        unrealized_pnl = 0.0
        
        for p in open_positions:
            current_value = p.shares * p.current_price
            total_value += current_value
            unrealized_pnl += p.pnl
        
        return {
            "timestamp": datetime.now().isoformat(),
            "days_trading": (datetime.now() - self.start_date).days,
            "initial_capital": self.initial_capital,
            "current_cash": self.cash,
            "positions_value": total_value - self.cash,
            "total_value": total_value,
            "total_pnl": total_value - self.initial_capital,
            "total_pnl_pct": ((total_value - self.initial_capital) / self.initial_capital) * 100,
            "open_positions": len(open_positions),
            "closed_positions": self.portfolio["closed_positions"],
            "total_trades": len(self.trades),
            "unrealized_pnl": unrealized_pnl
        }
    
    def generate_daily_report(self) -> str:
        """生成每日报告"""
        summary = self.get_portfolio_summary()
        
        report = f"""# 📊 模拟投资日报 - Day {summary['days_trading']}

**日期:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}  
**初始本金:** ${summary['initial_capital']:.2f}  
**当前总值:** ${summary['total_value']:.2f}  
**总盈亏:** ${summary['total_pnl']:+.2f} ({summary['total_pnl_pct']:+.2f}%)  
**现金余额:** ${summary['current_cash']:.2f}

---

## 💼 持仓情况

**未实现盈亏:** ${summary['unrealized_pnl']:+.2f}  
**持仓数量:** {summary['open_positions']}  
**已平仓:** {summary['closed_positions']}  
**总交易次数:** {summary['total_trades']}

### 当前持仓

"""
        
        for p in self.positions:
            if p.status == "OPEN":
                report += f"""| 市场 | 方向 | 入场价 | 当前价 | 份额 | 投入 | 盈亏 |
|------|------|--------|--------|------|------|------|
| {p.market} | {p.side} | {p.entry_price} | {p.current_price} | {p.shares:.4f} | ${p.invested:.2f} | ${p.pnl:+.2f} ({p.pnl_pct:+.1f}%) |

"""
        
        report += f"""---

## 📈 今日交易

"""
        
        today = datetime.now().strftime('%Y-%m-%d')
        today_trades = [t for t in self.trades if t.timestamp.startswith(today)]
        
        if today_trades:
            for t in today_trades:
                report += f"- **{t.action}** {t.market} {t.side} @ {t.price}\n"
                report += f"  - 金额: ${t.amount:.2f}, 份额: {t.shares:.4f}\n"
                report += f"  - 理由: {t.reason}\n"
                if t.screenshot:
                    report += f"  - 截图: {t.screenshot}\n"
                report += "\n"
        else:
            report += "今日暂无交易\n"
        
        report += f"""
---

## 🎯 交易记录

查看详细交易记录: `paper_trading/trades/`

---

*模拟投资系统 - Deki Agent*
"""
        
        # 保存报告
        filename = f"paper_trading/daily_reports/report_{datetime.now().strftime('%Y%m%d')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        
        return report
    
    def generate_final_report(self) -> str:
        """生成最终报告"""
        summary = self.get_portfolio_summary()
        
        report = f"""# 🏆 模拟投资最终报告

## 📊 总体表现

| 指标 | 数值 |
|------|------|
| 初始本金 | ${summary['initial_capital']:.2f} |
| 最终总值 | ${summary['total_value']:.2f} |
| **总盈亏** | **${summary['total_pnl']:+.2f}** |
| **收益率** | **{summary['total_pnl_pct']:+.2f}%** |
| 交易天数 | {summary['days_trading']} 天 |
| 总交易次数 | {summary['total_trades']} |
| 胜率 | [需计算] |

---

## 💰 资金曲线

[资金曲线图 - 需手动生成]

---

## 📋 所有交易记录

"""
        
        for t in self.trades:
            report += f"""### {t.trade_id}
- **时间:** {t.timestamp}
- **操作:** {t.action} {t.market} {t.side}
- **价格:** {t.price}
- **金额:** ${t.amount:.2f}
- **理由:** {t.reason}
- **截图:** {t.screenshot if t.screenshot else "无"}

"""
        
        report += f"""---

## 📈 策略分析

### 盈利策略
[总结哪些策略有效]

### 亏损分析
[分析亏损原因]

### 改进建议
[提出优化方案]

---

*模拟投资系统 - Deki Agent*  
*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}*
"""
        
        # 保存报告
        filename = "paper_trading/FINAL_REPORT.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        
        return report


def main():
    """测试入口"""
    system = PaperTradingSystem(initial_capital=100.0)
    
    print("\n" + "="*50)
    print("模拟投资系统已启动")
    print("="*50 + "\n")
    
    # 显示帮助
    print("使用说明:")
    print("1. 买入: system.buy(market, side, price, amount, reason, screenshot)")
    print("2. 卖出: system.sell(market, side, exit_price, reason, screenshot)")
    print("3. 更新价格: system.update_prices({'market': price})")
    print("4. 生成日报: system.generate_daily_report()")
    print("5. 查看组合: system.get_portfolio_summary()")
    print("\n所有记录保存在 paper_trading/ 目录")


if __name__ == "__main__":
    main()
