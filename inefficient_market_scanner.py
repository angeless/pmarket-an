#!/usr/bin/env python3
"""
Kalshi 低效市场捡漏扫描器
寻找低交易量、高价差的市场机会
"""

import json
import requests
from datetime import datetime
from typing import Dict, List, Optional

class InefficientMarketScanner:
    """低效市场扫描器"""
    
    def __init__(self):
        self.min_spread = 0.02  # 最小价差 2%
        self.max_volume = 100000  # 最大日交易量 $100k
        self.min_days = 30  # 最少30天到期
        
    def fetch_polymarket_markets(self) -> List[Dict]:
        """获取 Polymarket 市场数据"""
        try:
            url = "https://gamma-api.polymarket.com/markets?closed=false&archived=false&limit=200"
            response = requests.get(url, timeout=30)
            data = response.json()
            
            markets = []
            for m in data:
                try:
                    vol = float(m.get('volume') or 0)
                    liq = float(m.get('liquidity') or 0)
                    
                    # 解析价格
                    prices_str = m.get('outcomePrices', '[]')
                    prices = json.loads(prices_str) if isinstance(prices_str, str) else prices_str
                    
                    if len(prices) >= 2:
                        p1, p2 = float(prices[0]), float(prices[1])
                        spread = abs(p1 - p2)
                        
                        markets.append({
                            'name': m.get('question', 'Unknown'),
                            'slug': m.get('slug', ''),
                            'volume': vol,
                            'liquidity': liq,
                            'yes_price': p1,
                            'no_price': p2,
                            'spread': spread,
                            'end_date': m.get('endDate', ''),
                            'category': m.get('category', 'Other')
                        })
                except:
                    continue
            
            return markets
        except Exception as e:
            print(f"获取市场数据失败: {e}")
            return []
    
    def identify_inefficient(self, markets: List[Dict]) -> List[Dict]:
        """识别低效市场"""
        opportunities = []
        
        for m in markets:
            score = 0
            reasons = []
            
            # 1. 低交易量
            if m['volume'] < self.max_volume:
                score += 2
                reasons.append(f"低交易量 (${m['volume']:,.0f})")
            
            # 2. 高价差
            if m['spread'] > self.min_spread:
                score += 3
                reasons.append(f"高价差 ({m['spread']*100:.1f}%)")
            
            # 3. 价格适中（有波动空间）
            if 0.20 <= m['yes_price'] <= 0.80:
                score += 1
                reasons.append(f"价格适中 ({m['yes_price']:.2f})")
            
            # 4. 特定类别（更容易捡漏）
            if m['category'] in ['Sports', 'Politics', 'Crypto']:
                score += 1
                reasons.append(f"活跃类别 ({m['category']})")
            
            if score >= 4:  # 总分够高
                opportunities.append({
                    **m,
                    'score': score,
                    'reasons': reasons,
                    'strategy': self._suggest_strategy(m)
                })
        
        # 按评分排序
        return sorted(opportunities, key=lambda x: x['score'], reverse=True)
    
    def _suggest_strategy(self, market: Dict) -> str:
        """建议策略"""
        if market['volume'] < 50000 and market['spread'] > 0.03:
            return "流动性提供: 挂单赚价差"
        elif market['yes_price'] < 0.30:
            return "价值低估: 买入YES等待反弹"
        elif market['no_price'] < 0.30:
            return "价值低估: 买入NO等待反弹"
        else:
            return "观望: 等待更明确信号"
    
    def generate_report(self, opportunities: List[Dict]) -> str:
        """生成捡漏报告"""
        report = f"""# 🔍 Kalshi/Polymarket 低效市场捡漏报告

**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}  
**扫描市场数:** 200+  
**发现机会:** {len(opportunities)} 个

---

## 🎯 高价值捡漏机会

"""
        
        for i, opp in enumerate(opportunities[:10], 1):
            report += f"""### {i}. {opp['name'][:60]}...
- **类别:** {opp['category']}
- **交易量:** ${opp['volume']:,.0f}
- **流动性:** ${opp['liquidity']:,.0f}
- **YES价格:** {opp['yes_price']:.2f}
- **NO价格:** {opp['no_price']:.2f}
- **价差:** {opp['spread']*100:.1f}%
- **评分:** {opp['score']}/7
- **原因:** {', '.join(opp['reasons'])}
- **建议策略:** {opp['strategy']}

"""
        
        report += f"""---

## 💡 捡漏策略说明

### 1. 流动性提供 (Maker)
在价差 > 3% 的市场双边挂单，赚取中间差价。
- 风险: 可能只成交一边
- 收益: 价差的一半

### 2. 价值低估买入
当价格 < 0.30 时，可能存在过度悲观定价。
- 风险: 判断错误
- 收益: 可能翻倍

### 3. 时间价值
长期市场（30天+）价格往往被低估。
- 风险: 资金占用
- 收益: 时间衰减收益

---

*报告由 InefficientMarketScanner 自动生成*
"""
        
        return report
    
    def run(self):
        """运行扫描"""
        print("=" * 60)
        print("🔍 低效市场捡漏扫描器")
        print("=" * 60)
        print()
        
        print("📊 获取市场数据...")
        markets = self.fetch_polymarket_markets()
        print(f"✅ 获取 {len(markets)} 个市场")
        print()
        
        print("🔍 识别低效市场...")
        opportunities = self.identify_inefficient(markets)
        print(f"✅ 发现 {len(opportunities)} 个机会")
        print()
        
        if opportunities:
            report = self.generate_report(opportunities)
            
            # 保存报告
            filename = f"inefficient_markets_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(report)
            print(f"💾 报告已保存: {filename}")
        else:
            print("⏳ 当前无低效市场机会")
        
        return opportunities


def main():
    """主入口"""
    scanner = InefficientMarketScanner()
    scanner.run()


if __name__ == "__main__":
    main()
