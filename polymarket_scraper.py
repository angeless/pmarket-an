"""
Polymarket Data Scraper (Gamma API)
Polymarket 数据抓取模块 - 基于 Gamma API
"""

import requests
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PolymarketScraper:
    """Polymarket 数据抓取器"""
    
    BASE_URL = "https://gamma-api.polymarket.com"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "PolymarketScraper/1.0"
        })
        self.scraped_data = []
    
    def get_markets(self, limit: int = 100, closed: bool = False) -> List[Dict]:
        """获取市场列表"""
        try:
            params = {
                "closed": str(closed).lower(),
                "archived": "false",
                "order": "volume",
                "sort": "desc",
                "limit": limit,
                "offset": 0
            }
            response = self.session.get(
                f"{self.BASE_URL}/markets",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"获取市场列表失败: {e}")
            return []
    
    def get_market_details(self, market_id: str) -> Optional[Dict]:
        """获取市场详情"""
        try:
            response = self.session.get(
                f"{self.BASE_URL}/markets/{market_id}",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"获取市场详情失败 {market_id}: {e}")
            return None
    
    def scrape_active_markets(self, count: int = 20) -> List[Dict]:
        """抓取活跃市场数据"""
        logger.info(f"获取 {count} 个活跃市场...")
        markets = self.get_markets(limit=count*2, closed=False)
        
        # 筛选活跃市场
        active_markets = [
            m for m in markets 
            if m.get("active", True) and not m.get("closed", False)
        ][:count]
        
        results = []
        for i, market in enumerate(active_markets):
            market_id = market.get("id")
            slug = market.get("slug", "unknown")
            
            logger.info(f"[{i+1}/{len(active_markets)}] 抓取 {slug}...")
            
            # 获取完整详情
            details = self.get_market_details(str(market_id))
            if details:
                result = {
                    "market_id": market_id,
                    "slug": slug,
                    "question": details.get("question"),
                    "description": details.get("description", "")[:200],
                    "category": details.get("category"),
                    "volume": details.get("volume", 0),
                    "liquidity": details.get("liquidity", 0),
                    "outcomes": details.get("outcomes", []),
                    "prices": self._extract_prices(details),
                    "end_date": details.get("endDate"),
                    "resolution_source": details.get("resolutionSource"),
                    "scraped_at": datetime.now().isoformat()
                }
                results.append(result)
                self.scraped_data.append(result)
            
            time.sleep(0.3)  # 避免速率限制
        
        return results
    
    def _extract_prices(self, market: Dict) -> Dict:
        """提取市场价格信息"""
        outcomes = market.get("outcomes", [])
        prices = {}
        
        if outcomes and isinstance(outcomes[0], dict):
            # outcomes 是字典列表
            for outcome in outcomes:
                name = outcome.get("name", "unknown")
                price = outcome.get("price", 0)
                prices[name] = price
        elif outcomes:
            # outcomes 是字符串列表，需要结合其他字段
            for i, name in enumerate(outcomes):
                # 尝试从 outcomePrices 获取价格
                outcome_prices = market.get("outcomePrices", [])
                if i < len(outcome_prices):
                    try:
                        price = float(outcome_prices[i])
                    except:
                        price = 0
                else:
                    price = 0
                prices[name] = price
        
        return prices
    
    def find_arbitrage_candidates(self, max_price_diff: float = 0.05) -> List[Dict]:
        """寻找套利候选 (价格偏离较大的市场)"""
        candidates = []
        
        for data in self.scraped_data:
            prices = data.get("prices", {})
            if len(prices) >= 2:
                price_values = list(prices.values())
                total = sum(price_values)
                
                # 如果总价偏离 1.0 超过阈值，可能是套利机会
                if abs(total - 1.0) > max_price_diff:
                    candidates.append({
                        "market_id": data["market_id"],
                        "question": data["question"],
                        "prices": prices,
                        "price_sum": total,
                        "deviation": abs(total - 1.0)
                    })
        
        return sorted(candidates, key=lambda x: x["deviation"], reverse=True)
    
    def analyze_volume_opportunities(self, min_volume: float = 100000) -> List[Dict]:
        """分析高交易量机会"""
        opportunities = []
        
        for data in self.scraped_data:
            volume = data.get("volume", 0)
            try:
                vol = float(volume) if volume else 0
            except:
                vol = 0
            
            if vol >= min_volume:
                opportunities.append({
                    "market_id": data["market_id"],
                    "question": data["question"],
                    "volume": vol,
                    "prices": data.get("prices"),
                    "liquidity": data.get("liquidity")
                })
        
        return sorted(opportunities, key=lambda x: x["volume"], reverse=True)
    
    def export_to_json(self, filepath: str = None) -> str:
        """导出数据到 JSON"""
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"polymarket_data_{timestamp}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"数据已导出到: {filepath}")
        return filepath


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Polymarket 数据抓取工具')
    parser.add_argument('--markets', '-n', type=int, default=20, help='抓取市场数量')
    parser.add_argument('--min-volume', '-v', type=float, default=100000, help='最小交易量')
    parser.add_argument('--output', '-o', type=str, help='输出文件路径')
    
    args = parser.parse_args()
    
    print("🚀 启动 Polymarket 数据抓取...")
    print(f"   目标: {args.markets} 个活跃市场")
    print()
    
    scraper = PolymarketScraper()
    
    # 抓取数据
    results = scraper.scrape_active_markets(count=args.markets)
    
    # 分析高交易量机会
    vol_opps = scraper.analyze_volume_opportunities(min_volume=args.min_volume)
    
    print(f"\n✅ 抓取完成: {len(results)} 个市场")
    
    if vol_opps:
        print(f"\n💰 高交易量市场 (≥${args.min_volume:,.0f}):")
        for opp in vol_opps[:5]:
            print(f"   • {opp['question'][:50]}...")
            print(f"     交易量: ${opp['volume']:,.0f} | 流动性: ${float(opp['liquidity'] or 0):,.0f}")
    else:
        print(f"\n📊 未发现高交易量市场 (≥${args.min_volume:,.0f})")
    
    # 导出数据
    output_file = scraper.export_to_json(args.output)
    print(f"\n💾 数据已保存: {output_file}")
    
    # 打印市场摘要
    print("\n📋 市场摘要:")
    for i, r in enumerate(results[:5], 1):
        prices = r.get('prices', {})
        price_str = ', '.join([f"{k}={v}" for k, v in list(prices.items())[:2]])
        print(f"   {i}. {r['question'][:45]}...")
        print(f"      价格: {price_str}")


if __name__ == "__main__":
    main()
