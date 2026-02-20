#!/usr/bin/env python3
"""
跨平台套利监控系统
实时监控 Kalshi 和 Polymarket 价格差异
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional

class CrossPlatformArbitrageMonitor:
    """跨平台套利监控器"""
    
    def __init__(self, threshold: float = 0.03):
        self.threshold = threshold  # 3% 触发线
        self.opportunities = []
        self.monitored_markets = [
            # 同时在两个平台的市场
            {"name": "Trump 2026 Policy", "kalshi_symbol": "TRUMP-2026", "poly_slug": "trump-policy-2026"},
            {"name": "FOMC Rate Decision", "kalshi_symbol": "FOMC-MAR", "poly_slug": "fed-rate-march"},
            {"name": "Bitcoin ETF", "kalshi_symbol": "BTC-ETF", "poly_slug": "bitcoin-etf"},
        ]
    
    def fetch_kalshi_price(self, symbol: str) -> Optional[float]:
        """获取 Kalshi 价格（模拟，实际需要API）"""
        # TODO: 接入 Kalshi API
        # 目前返回模拟数据
        mock_prices = {
            "TRUMP-2026": 0.58,
            "FOMC-MAR": 0.65,
            "BTC-ETF": 0.72,
        }
        return mock_prices.get(symbol)
    
    def fetch_polymarket_price(self, slug: str) -> Optional[float]:
        """获取 Polymarket 价格"""
        try:
            import requests
            url = f"https://gamma-api.polymarket.com/markets?slug={slug}"
            response = requests.get(url, timeout=10)
            data = response.json()
            if data and len(data) > 0:
                prices_str = data[0].get('outcomePrices', '[]')
                prices = json.loads(prices_str) if isinstance(prices_str, str) else prices_str
                if prices and len(prices) > 0:
                    return float(prices[0])
        except Exception as e:
            print(f"获取Polymarket价格失败: {e}")
        return None
    
    def check_arbitrage(self, market: Dict) -> Optional[Dict]:
        """检查单个市场的套利机会"""
        kalshi_price = self.fetch_kalshi_price(market['kalshi_symbol'])
        poly_price = self.fetch_polymarket_price(market['poly_slug'])
        
        if kalshi_price is None or poly_price is None:
            return None
        
        diff = abs(kalshi_price - poly_price)
        diff_pct = diff / min(kalshi_price, poly_price)
        
        if diff_pct > self.threshold:
            return {
                'market': market['name'],
                'kalshi_price': kalshi_price,
                'poly_price': poly_price,
                'diff': diff,
                'diff_pct': diff_pct,
                'buy_platform': 'Kalshi' if kalshi_price < poly_price else 'Polymarket',
                'sell_platform': 'Polymarket' if kalshi_price < poly_price else 'Kalshi',
                'buy_price': min(kalshi_price, poly_price),
                'sell_price': max(kalshi_price, poly_price),
                'expected_profit': diff - 0.015,  # 扣除1.5%双边手续费
                'timestamp': datetime.now().isoformat()
            }
        return None
    
    def scan_all(self) -> List[Dict]:
        """扫描所有监控的市场"""
        opportunities = []
        print(f"🔍 扫描 {len(self.monitored_markets)} 个市场...")
        
        for market in self.monitored_markets:
            opp = self.check_arbitrage(market)
            if opp:
                opportunities.append(opp)
                print(f"✅ 发现套利机会: {opp['market']}")
                print(f"   Kalshi: {opp['kalshi_price']}, Polymarket: {opp['poly_price']}")
                print(f"   价差: {opp['diff_pct']*100:.2f}%, 预期利润: {opp['expected_profit']*100:.2f}%")
        
        return opportunities
    
    def save_opportunities(self, opportunities: List[Dict]):
        """保存机会到文件"""
        filename = f"arbitrage_opps_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(filename, 'w') as f:
            json.dump(opportunities, f, indent=2)
        print(f"💾 已保存到 {filename}")
    
    def run_continuous(self, interval: int = 300):
        """持续运行监控"""
        print("🚀 跨平台套利监控启动")
        print(f"⏱️  检查间隔: {interval}秒")
        print(f"📊 触发阈值: {self.threshold*100}%")
        print()
        
        while True:
            opportunities = self.scan_all()
            if opportunities:
                self.save_opportunities(opportunities)
            else:
                print(f"{datetime.now().strftime('%H:%M')} - 暂无套利机会")
            
            time.sleep(interval)


def main():
    """主入口"""
    monitor = CrossPlatformArbitrageMonitor(threshold=0.03)
    
    # 单次扫描测试
    print("=" * 60)
    print("🔥 跨平台套利监控测试")
    print("=" * 60)
    print()
    
    opportunities = monitor.scan_all()
    
    if opportunities:
        print(f"\n✅ 共发现 {len(opportunities)} 个套利机会")
        monitor.save_opportunities(opportunities)
    else:
        print("\n⏳ 当前无套利机会")
    
    print()
    print("=" * 60)
    print("提示: 接入Kalshi API后可实现实时监控")
    print("运行: monitor.run_continuous() 开始持续监控")
    print("=" * 60)


if __name__ == "__main__":
    main()
