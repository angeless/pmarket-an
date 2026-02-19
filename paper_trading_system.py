#!/usr/bin/env python3
"""
Polymarket 模拟投资系统（含手续费）
本金: $100 USD
周期: 7天高频交易
记录所有买卖操作和收益
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class Trade:
    """交易记录（含手续费）"""
    trade_id: str
    timestamp: str
    market: str
    action: str  # BUY or SELL
    side: str    # YES or NO
    price: float
    amount: float  # 投入金额
    shares: float  # 购买份额
    fee: float     # 手续费
    net_amount: float  # 扣除手续费后的净额
    reason: str
    screenshot: str = ""
    
@dataclass
class Position:
    """持仓记录"""
    market: str
    side: str
    entry_price: float
    shares: float
    invested: float
    entry_fee: float  # 买入时手续费
    current_price: float = 0.0
    pnl: float = 0.0
    pnl_pct: float = 0.0
    status: str = "OPEN"  # OPEN or CLOSED

class PaperTradingSystem:
    """模拟投资系统（含真实手续费）"""
    
    # Polymarket 手续费结构
    MAKER_FEE = 0.0      # Maker 0%
    TAKER_FEE = 0.01     # Taker 1% (保守估计，实际0.5-2%)
    
    def __init__(self, initial_capital: float = 100.0):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions: List[Position] = []
        self.trades: List[Trade] = []
        self.daily_records: List[Dict] = []
        self.start_date = datetime.now()
        self.trade_counter = 0
        self.total_fees = 0.0  # 累计手续费
        
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
            "total_fees": 0.0,  # 累计手续费
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
        print(f"💸 手续费: Maker {self.MAKER_FEE*100}%, Taker {self.TAKER_FEE*100}%")
    
    def _generate_trade_id(self) -> str:
        """生成交易ID"""
        self.trade_counter += 1
        return f"TRADE_{self.start_date.strftime('%Y%m%d')}_{self.trade_counter:03d}"
    
    def _calculate_fee(self, amount: float, is_maker: bool = False) -> float:
        """计算手续费"""
        if is_maker:
            return amount * self.MAKER_FEE
        else:
            return amount * self.TAKER_FEE
    
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
            reason: str, screenshot: str = "", is_maker: bool = False) -> Optional[Trade]:
        """买入操作（含手续费）"""
        
        # 计算手续费
        fee = self._calculate_fee(amount, is_maker)
        total_cost = amount + fee
        
        if total_cost > self.cash:
            print(f"❌ 资金不足: 需要 ${total_cost:.2f} (含手续费 ${fee:.2f}), 可用 ${self.cash:.2f}")
            return None
        
        # 计算购买份额（手续费从金额中扣除，份额相应减少）
        net_amount = amount - fee
        shares = net_amount / price
        
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
            fee=fee,
            net_amount=net_amount,
            reason=reason,
            screenshot=screenshot
        )
        
        # 更新现金
        self.cash -= total_cost
        self.total_fees += fee
        
        # 创建持仓
        position = Position(
            market=market,
            side=side,
            entry_price=price,
            shares=shares,
            invested=net_amount,  # 实际投资金额（扣除手续费）
            entry_fee=fee,
            current_price=price
        )
        
        self.positions.append(position)
        self.trades.append(trade)
        
        # 更新投资组合
        self.portfolio["current_cash"] = self.cash
        self.portfolio["total_invested"] += net_amount
        self.portfolio["total_fees"] = self.total_fees
        self.portfolio["total_trades"] += 1
        self.portfolio["open_positions"] = len([p for p in self.positions if p.status == "OPEN"])
        
        self._save_portfolio()
        self._save_trade(trade)
        
        fee_type = "Maker" if is_maker else "Taker"
        print(f"✅ 买入成功: {trade.trade_id}")
        print(f"   市场: {market}")
        print(f"   方向: {side} @ {price}")
        print(f"   投入: ${amount:.2f} - 手续费(${fee:.2f}, {fee_type}) = ${net_amount:.2f}")
        print(f"   获得: {shares:.4f} 份")
        print(f"   剩余现金: ${self.cash:.2f}")
        
        return trade
    
    def sell(self, market: str, side: str, exit_price: float, 
             reason: str, screenshot: str = "", is_maker: bool = False) -> Optional[Trade]:
        """卖出操作（含手续费）"""
        
        # 查找对应持仓
        position = None
        for p in self.positions:
            if p.market == market and p.side == side and p.status == "OPEN":
                position = p
                break
        
        if not position:
            print(f"❌ 未找到持仓: {market} {side}")
            return None
        
        # 计算卖出金额
        gross_amount = position.shares * exit_price
        
        # 计算手续费
        fee = self._calculate_fee(gross_amount, is_maker)
        net_amount = gross_amount - fee
        
        # 计算收益（扣除两边手续费）
        total_fees = position.entry_fee + fee
        pnl = net_amount - position.invested
        pnl_pct = (pnl / position.invested) * 100 if position.invested > 0 else 0
        
        # 创建交易记录
        trade = Trade(
            trade_id=self._generate_trade_id(),
            timestamp=datetime.now().isoformat(),
            market=market,
            action="SELL",
            side=side,
            price=exit_price,
            amount=gross_amount,
            shares=position.shares,
            fee=fee,
            net_amount=net_amount,
            reason=reason,
            screenshot=screenshot
        )
        
        # 更新现金
        self.cash += net_amount
        self.total_fees += fee
        
        # 更新持仓状态
        position.current_price = exit_price
        position.pnl = pnl
        position.pnl_pct = pnl_pct
        position.status = "CLOSED"
        
        self.trades.append(trade)
        
        # 更新投资组合
        self.portfolio["current_cash"] = self.cash
        self.portfolio["total_fees"] = self.total_fees
        self.portfolio["total_pnl"] += pnl
        self.portfolio["total_trades"] += 1
        self.portfolio["closed_positions"] += 1
        self.portfolio["open_positions"] = len([p for p in self.positions if p.status == "OPEN"])
        
        # 计算总收益率
        total_value = self.cash + sum([p.shares * p.current_price for p in self.positions if p.status == "OPEN"])
        self.portfolio["total_pnl_pct"] = ((total_value - self.initial_capital) / self.initial_capital) * 100
        
        self._save_portfolio()
        self._save_trade(trade)
        
        fee_type = "Maker" if is_maker else "Taker"
        print(f"✅ 卖出成功: {trade.trade_id}")
        print(f"   市场: {market}")
        print(f"   方向: {side} @ {exit_price}")
        print(f"   毛收入: ${gross_amount:.2f} - 手续费(${fee:.2f}, {fee_type}) = ${net_amount:.2f}")
        print(f"   总手续费: ${total_fees:.2f}")
        print(f"   盈亏: ${pnl:+.2f} ({pnl_pct:+.2f}%)")
        print(f"   当前现金: ${self.cash:.2f}")
        
        return trade
    
    def update_prices(self, prices: Dict[str, float]):
        """更新市场价格"""
        for position in self.positions:
            if position.status == "OPEN" and position.market in prices:
                position.current_price = prices[position.market]
                current_value = position.shares * position.current_price
                position.pnl = current_value - position.invested
                position.pnl_pct = (position.pnl / position.invested) * 100 if position.invested > 0 else 0
        
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
            "total_fees": self.total_fees,
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
**累计手续费:** ${summary['total_fees']:.2f}  
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
                report += f"""| 市场 | 方向 | 入场价 | 当前价 | 份额 | 投入 | 盈亏 | 手续费 |
|------|------|--------|--------|------|------|------|--------|
| {p.market[:40]}... | {p.side} | {p.entry_price} | {p.current_price} | {p.shares:.4f} | ${p.invested:.2f} | ${p.pnl:+.2f} ({p.pnl_pct:+.1f}%) | ${p.entry_fee:.2f} |

"""
        
        report += f"""---

## 📈 今日交易

"""
        
        today = datetime.now().strftime('%Y-%m-%d')
        today_trades = [t for t in self.trades if t.timestamp.startswith(today)]
        
        if today_trades:
            for t in today_trades:
                report += f"- **{t.action}** {t.market} {t.side} @ {t.price}\n"
                report += f"  - 金额: ${t.amount:.2f}, 手续费: ${t.fee:.2f}, 净额: ${t.net_amount:.2f}\n"
                report += f"  - 理由: {t.reason}\n"
                if t.screenshot:
                    report += f"  - 截图: {t.screenshot}\n"
                report += "\n"
        else:
            report += "今日暂无交易\n"
        
        report += f"""
---

## 💸 手续费明细

累计手续费: ${summary['total_fees']:.2f}

**手续费说明:**
- Maker Fee: {self.MAKER_FEE*100}% (提供流动性)
- Taker Fee: {self.TAKER_FEE*100}% (吃单)
- 当前假设所有交易均为 Taker (保守估计)

---

*模拟投资系统 - Deki Agent*  
*含真实手续费计算*
"""
        
        # 保存报告
        filename = f"paper_trading/daily_reports/report_{datetime.now().strftime('%Y%m%d')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        
        return report


def main():
    """测试入口"""
    print("=" * 60)
    print("🚀 Polymarket 模拟投资系统（含手续费）")
    print("=" * 60)
    print()
    
    system = PaperTradingSystem(initial_capital=100.0)
    
    # 示例交易（含手续费）
    print("\n📈 执行示例交易（含1%手续费）：\n")
    
    trade1 = system.buy(
        market="Bitcoin Up or Down - Feb 19",
        side="YES",
        price=0.52,
        amount=30.0,
        reason="技术指标看涨",
        is_maker=False  # Taker，1%手续费
    )
    
    if trade1:
        print(f"\n实际投资: ${trade1.net_amount:.2f} (扣除手续费)")
        print(f"手续费: ${trade1.fee:.2f}")
    
    print("\n" + "=" * 60)
    print("✅ 系统测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
