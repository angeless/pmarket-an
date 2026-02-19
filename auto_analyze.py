#!/usr/bin/env python3
"""
Polymarket 自动数据抓取与分析
每5分钟运行一次
"""

import json
import subprocess
from datetime import datetime

def fetch_and_analyze():
    """抓取并分析市场数据"""
    
    # 抓取数据
    print("🌐 抓取 Polymarket 数据...")
    subprocess.run([
        "curl", "-s", 
        "https://gamma-api.polymarket.com/markets?closed=false&archived=false&limit=100",
        "-o", "paper_trading/latest_market_data.json"
    ])
    
    # 加载数据
    with open('paper_trading/latest_market_data.json') as f:
        data = json.load(f)
    
    print(f"✅ 获取 {len(data)} 个市场\n")
    
    # 处理数据
    markets = []
    for m in data:
        try:
            vol_str = m.get('volume', '0')
            vol = float(vol_str) if vol_str and vol_str != 'None' else 0
            
            liq_str = m.get('liquidity', '0')
            liq = float(liq_str) if liq_str and liq_str != 'None' else 0
            
            if vol > 100000:
                # 解析 outcomes (可能是 JSON 字符串)
                outcomes_str = m.get('outcomes', '[]')
                if isinstance(outcomes_str, str):
                    outcomes = json.loads(outcomes_str) if outcomes_str else []
                else:
                    outcomes = outcomes_str
                
                # 解析 outcomePrices (可能是 JSON 字符串)
                prices_str = m.get('outcomePrices', '[]')
                prices = []
                if isinstance(prices_str, str):
                    try:
                        price_list = json.loads(prices_str) if prices_str else []
                        for p in price_list:
                            try:
                                prices.append(float(p))
                            except:
                                prices.append(0)
                    except:
                        prices = [0, 0]
                else:
                    prices = [float(p) if p else 0 for p in prices_str]
                
                markets.append({
                    'question': m.get('question', 'Unknown'),
                    'slug': m.get('slug', ''),
                    'volume': vol,
                    'liquidity': liq,
                    'outcomes': outcomes,
                    'prices': prices,
                    'category': m.get('category', 'Other')
                })
        except:
            pass
    
    # 排序
    markets.sort(key=lambda x: x['volume'], reverse=True)
    
    print(f"📊 高交易量市场 (\u003e$100k): {len(markets)} 个\n")
    print("=" * 70)
    
    # 分析机会
    opportunities = []
    
    for i, m in enumerate(markets[:15], 1):
        print(f"\n{i}. {m['question'][:60]}...")
        print(f"   💰 Volume: ${m['volume']:,.0f} | Liquidity: ${m['liquidity']:,.0f}")
        
        # 显示价格
        if m['outcomes'] and m['prices']:
            for outcome, price in zip(m['outcomes'][:2], m['prices'][:2]):
                if price > 0:
                    print(f"   📊 {outcome}: ${price:.2f}")
        
        # 分析机会
        if len(m['prices']) >= 2:
            p1, p2 = m['prices'][0], m['prices'][1]
            if p1 + p2 < 0.98 and p1 > 0 and p2 > 0:
                profit = 1 - (p1 + p2)
                print(f"   ⚡ 套利机会: +{profit*100:.1f}% 空间")
                opportunities.append({
                    'market': m['question'],
                    'type': 'ARBITRAGE',
                    'prices': [p1, p2],
                    'profit_potential': profit
                })
            elif abs(p1 - 0.5) > 0.2:
                direction = "YES" if p1 > 0.5 else "NO"
                print(f"   📈 趋势机会: {direction} 强势 ({p1:.2f})")
                opportunities.append({
                    'market': m['question'],
                    'type': 'TREND',
                    'direction': direction,
                    'price': p1
                })
    
    print("\n" + "=" * 70)
    print(f"\n💡 发现 {len(opportunities)} 个交易机会\n")
    
    # 保存分析结果
    result = {
        'timestamp': datetime.now().isoformat(),
        'total_markets': len(data),
        'high_volume_markets': len(markets),
        'opportunities': opportunities,
        'top_markets': markets[:10]
    }
    
    with open('paper_trading/market_analysis.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"✅ 数据已保存")
    print(f"   - paper_trading/latest_market_data.json")
    print(f"   - paper_trading/market_analysis.json")
    
    # 生成交易想法
    if opportunities:
        print("\n🎯 交易建议:")
        for opp in opportunities[:3]:
            if opp['type'] == 'ARBITRAGE':
                print(f"\n   套利: {opp['market'][:40]}...")
                print(f"   操作: 同时买入 YES + NO")
                print(f"   预期收益: {opp['profit_potential']*100:.1f}%")
            else:
                print(f"\n   趋势: {opp['market'][:40]}...")
                print(f"   操作: BUY {opp['direction']} @ {opp['price']:.2f}")
    
    return opportunities

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 Polymarket 自动分析")
    print("=" * 70)
    print()
    fetch_and_analyze()
    print("\n" + "=" * 70)
    print("✅ 分析完成")
    print("=" * 70)
