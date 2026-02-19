#!/usr/bin/env python3
"""
Polymarket 真实交易客户端
支持：下单、查看订单、获取余额、取消订单
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional

CONFIG_FILE = "paper_trading/polymarket_config.json"

class PolymarketTrader:
    """Polymarket 交易客户端"""
    
    def __init__(self):
        self.client = None
        self.config = None
        self._load_config()
        self._init_client()
    
    def _load_config(self):
        """加载配置"""
        if not os.path.exists(CONFIG_FILE):
            raise Exception("配置文件不存在，请先运行 setup_trading.py setup")
        
        with open(CONFIG_FILE, "r") as f:
            self.config = json.load(f)
        
        if not self.config.get("api_credentials"):
            raise Exception("没有 API 凭证，请先运行 setup_trading.py creds")
    
    def _init_client(self):
        """初始化客户端"""
        try:
            from py_clob_client.client import ClobClient, ApiCreds
            
            creds = self.config["api_credentials"]
            
            self.client = ClobClient(
                host=self.config["host"],
                chain_id=self.config["chain_id"],
                key=self.config["private_key"],
                creds=ApiCreds(
                    api_key=creds["api_key"],
                    api_secret=creds["secret"],
                    api_passphrase=creds["passphrase"]
                ),
                signature_type=1,  # POLY_PROXY
                funder=self.config["funder_address"]
            )
            
        except ImportError:
            raise Exception("请先安装 py-clob-client: pip install py-clob-client")
    
    def get_balance(self) -> Dict:
        """获取余额"""
        try:
            balance = self.client.get_balance()
            return balance
        except Exception as e:
            return {"error": str(e)}
    
    def place_order(self, token_id: str, side: str, price: float, size: float) -> Dict:
        """
        下单
        
        Args:
            token_id: 代币 ID（从市场数据获取）
            side: "BUY" 或 "SELL"
            price: 价格 (0-1)
            size: 数量（美元）
        """
        try:
            order = self.client.create_and_post_order(
                {
                    "token_id": token_id,
                    "price": price,
                    "size": size,
                    "side": side
                },
                {
                    "tick_size": "0.01",
                    "neg_risk": False
                }
            )
            
            # 记录交易
            self._record_trade({
                "action": "PLACE_ORDER",
                "token_id": token_id,
                "side": side,
                "price": price,
                "size": size,
                "order_id": order.get("orderID"),
                "timestamp": datetime.now().isoformat()
            })
            
            return order
            
        except Exception as e:
            return {"error": str(e)}
    
    def get_open_orders(self) -> list:
        """获取未成交订单"""
        try:
            orders = self.client.get_open_orders()
            return orders
        except Exception as e:
            return [{"error": str(e)}]
    
    def cancel_order(self, order_id: str) -> Dict:
        """取消订单"""
        try:
            result = self.client.cancel_order(order_id)
            
            self._record_trade({
                "action": "CANCEL_ORDER",
                "order_id": order_id,
                "timestamp": datetime.now().isoformat()
            })
            
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def cancel_all_orders(self) -> Dict:
        """取消所有订单"""
        try:
            result = self.client.cancel_all_orders()
            
            self._record_trade({
                "action": "CANCEL_ALL_ORDERS",
                "timestamp": datetime.now().isoformat()
            })
            
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def get_market_orderbook(self, token_id: str) -> Dict:
        """获取市场订单簿"""
        try:
            book = self.client.get_order_book(token_id)
            return book
        except Exception as e:
            return {"error": str(e)}
    
    def _record_trade(self, trade_info: Dict):
        """记录交易"""
        log_file = "paper_trading/real_trades.json"
        
        trades = []
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                trades = json.load(f)
        
        trades.append(trade_info)
        
        with open(log_file, "w") as f:
            json.dump(trades, f, indent=2)


def main():
    """命令行入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("=" * 60)
        print("🔥 Polymarket 真实交易客户端")
        print("=" * 60)
        print()
        print("用法:")
        print("  python3 live_trader.py balance          # 查看余额")
        print("  python3 live_trader.py orders           # 查看未成交订单")
        print("  python3 live_trader.py buy TOKEN PRICE SIZE   # 买入")
        print("  python3 live_trader.py sell TOKEN PRICE SIZE  # 卖出")
        print("  python3 live_trader.py cancel ORDER_ID  # 取消订单")
        print("  python3 live_trader.py cancel-all       # 取消所有订单")
        print()
        print("⚠️  注意：这些操作涉及真实资金！")
        print()
        return
    
    command = sys.argv[1]
    
    try:
        trader = PolymarketTrader()
        
        if command == "balance":
            print("查询余额...")
            balance = trader.get_balance()
            print(json.dumps(balance, indent=2))
        
        elif command == "orders":
            print("查询未成交订单...")
            orders = trader.get_open_orders()
            print(json.dumps(orders, indent=2))
        
        elif command == "buy":
            if len(sys.argv) < 5:
                print("用法: python3 live_trader.py buy TOKEN_ID PRICE SIZE")
                return
            token_id = sys.argv[2]
            price = float(sys.argv[3])
            size = float(sys.argv[4])
            
            print(f"⚠️  即将下单买入:")
            print(f"   Token: {token_id[:20]}...")
            print(f"   价格: {price}")
            print(f"   金额: ${size}")
            confirm = input("确认执行? (yes/no): ")
            
            if confirm.lower() == "yes":
                result = trader.place_order(token_id, "BUY", price, size)
                print(json.dumps(result, indent=2))
            else:
                print("已取消")
        
        elif command == "sell":
            if len(sys.argv) < 5:
                print("用法: python3 live_trader.py sell TOKEN_ID PRICE SIZE")
                return
            token_id = sys.argv[2]
            price = float(sys.argv[3])
            size = float(sys.argv[4])
            
            print(f"⚠️  即将下单卖出:")
            print(f"   Token: {token_id[:20]}...")
            print(f"   价格: {price}")
            print(f"   金额: ${size}")
            confirm = input("确认执行? (yes/no): ")
            
            if confirm.lower() == "yes":
                result = trader.place_order(token_id, "SELL", price, size)
                print(json.dumps(result, indent=2))
            else:
                print("已取消")
        
        elif command == "cancel":
            if len(sys.argv) < 3:
                print("用法: python3 live_trader.py cancel ORDER_ID")
                return
            order_id = sys.argv[2]
            result = trader.cancel_order(order_id)
            print(json.dumps(result, indent=2))
        
        elif command == "cancel-all":
            confirm = input("确认取消所有订单? (yes/no): ")
            if confirm.lower() == "yes":
                result = trader.cancel_all_orders()
                print(json.dumps(result, indent=2))
            else:
                print("已取消")
        
        else:
            print(f"未知命令: {command}")
    
    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == "__main__":
    main()
