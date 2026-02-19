#!/usr/bin/env python3
"""
快速记录交易工具
用于手动输入交易数据
"""

import sys
import json
from datetime import datetime
from paper_trading_system import PaperTradingSystem

def record_buy():
    """记录买入"""
    print("\n📝 记录买入交易")
    print("-" * 40)
    
    system = PaperTradingSystem(initial_capital=100.0)
    
    # 从命令行参数或交互式输入
    if len(sys.argv) >= 6:
        market = sys.argv[2]
        side = sys.argv[3]
        price = float(sys.argv[4])
        amount = float(sys.argv[5])
        reason = sys.argv[6] if len(sys.argv) > 6 else "手动记录"
        screenshot = sys.argv[7] if len(sys.argv) > 7 else ""
    else:
        market = input("市场名称: ")
        side = input("方向 (YES/NO): ")
        price = float(input("价格 (0-1): "))
        amount = float(input("金额 ($): "))
        reason = input("交易理由: ")
        screenshot = input("截图文件名 (可选): ")
    
    trade = system.buy(market, side, price, amount, reason, screenshot)
    
    if trade:
        print(f"\n✅ 买入记录成功: {trade.trade_id}")
        
        # 显示当前状态
        summary = system.get_portfolio_summary()
        print(f"\n当前状态:")
        print(f"  现金: ${summary['current_cash']:.2f}")
        print(f"  持仓: {summary['open_positions']} 个")
        print(f"  总市值: ${summary['total_value']:.2f}")

def record_sell():
    """记录卖出"""
    print("\n📝 记录卖出交易")
    print("-" * 40)
    
    system = PaperTradingSystem(initial_capital=100.0)
    
    if len(sys.argv) >= 6:
        market = sys.argv[2]
        side = sys.argv[3]
        exit_price = float(sys.argv[4])
        reason = sys.argv[5]
        screenshot = sys.argv[6] if len(sys.argv) > 6 else ""
    else:
        market = input("市场名称: ")
        side = input("方向 (YES/NO): ")
        exit_price = float(input("卖出价格 (0-1): "))
        reason = input("卖出理由: ")
        screenshot = input("截图文件名 (可选): ")
    
    trade = system.sell(market, side, exit_price, reason, screenshot)
    
    if trade:
        print(f"\n✅ 卖出记录成功: {trade.trade_id}")
        
        # 显示当前状态
        summary = system.get_portfolio_summary()
        print(f"\n当前状态:")
        print(f"  现金: ${summary['current_cash']:.2f}")
        print(f"  持仓: {summary['open_positions']} 个")
        print(f"  总盈亏: ${summary['total_pnl']:+.2f} ({summary['total_pnl_pct']:+.2f}%)")

def show_status():
    """显示当前状态"""
    system = PaperTradingSystem(initial_capital=100.0)
    summary = system.get_portfolio_summary()
    
    print("\n📊 投资组合状态")
    print("-" * 40)
    print(f"初始本金: ${summary['initial_capital']:.2f}")
    print(f"当前现金: ${summary['current_cash']:.2f}")
    print(f"持仓市值: ${summary['positions_value']:.2f}")
    print(f"总市值: ${summary['total_value']:.2f}")
    print(f"总盈亏: ${summary['total_pnl']:+.2f} ({summary['total_pnl_pct']:+.2f}%)")
    print(f"交易天数: {summary['days_trading']}")
    print(f"持仓数量: {summary['open_positions']}")
    print(f"已平仓: {summary['closed_positions']}")
    print(f"总交易: {summary['total_trades']}")

def generate_report():
    """生成日报"""
    system = PaperTradingSystem(initial_capital=100.0)
    report = system.generate_daily_report()
    print(report)

def main():
    if len(sys.argv) < 2:
        print("""
📊 Polymarket 模拟投资记录工具

用法:
  python3 quick_trade.py buy [市场] [方向] [价格] [金额] [理由] [截图]
  python3 quick_trade.py sell [市场] [方向] [价格] [理由] [截图]
  python3 quick_trade.py status
  python3 quick_trade.py report

示例:
  python3 quick_trade.py buy "BTC Up" YES 0.52 30 "看涨趋势" "screenshot1.png"
  python3 quick_trade.py sell "BTC Up" YES 0.58 "止盈" "screenshot2.png"
        """)
        return
    
    command = sys.argv[1]
    
    if command == "buy":
        record_buy()
    elif command == "sell":
        record_sell()
    elif command == "status":
        show_status()
    elif command == "report":
        generate_report()
    else:
        print(f"未知命令: {command}")
        print("可用命令: buy, sell, status, report")

if __name__ == "__main__":
    main()
