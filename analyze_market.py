#!/usr/bin/env python3
"""
Polymarket 市场数据分析
自动分析交易机会
"""

import json
from datetime import datetime
from typing import List, Dict

def analyze_markets():
    """分析市场数据"""
    try:
        with open('paper_trading/latest_market_data.json', 'r') as f:
            data = json.load(f)
    except:
        print("❌ 无法加载市场数据")
        return []
    
    # 处理数据
    markets = []
    for m in data:
        try:
            # 处理字符串类型的 volume
            vol_str = m.get('volume', '0')
            vol = float(vol_str) if vol_str else 0
            
            liq_str = m.get('liquidity', '0')
            liq = float(liq_str) if liq_str else 0
            
            if vol > 100000:  # 只分析高交易量市场
                markets.append({
                    'question': m.get('question', 'Unknown'),
                    'slug': m.get('slug', ''),
                    'volume': vol,
                    'liquidity': liq,
                    'outcomes': m.get('outcomes', []),
                    'prices': [float(p) if p else 0 for p in m.get('outcomePrices', [])],
                    'category': m.get('category', 'Other'),
                    'end_date': m.get('endDate', '')
                })
        except Exception as e:
            pass
    
    # 按交易量排序
    markets.sort(key=lambda x: x['volume'], reverse=True)
    
    print(f"✅ 分析 {len(markets)} 个高交易量市场 (\u003e$100k)\n")
    print("=" * 60)
    
    # 显示 TOP 10
    opportunities = []
    for i, m in enumerate(markets[:10], 1):
        print(f"\n{i}. {m['question'][:55]}...")
        print(f"   💰 Volume: ${m['volume']:,.0f} | Liquidity: ${m['liquidity']:,.0f}")
        
        # 显示价格
        if m['outcomes'] and m['prices']:
            for j, (outcome, price) in enumerate(zip(m['outcomes'][:2], m['prices'][:2])):
                if price > 0:
                    print(f"   📊 {outcome}: ${price:.2f}")
        
        # 简单分析
        if m['prices'] and len(m['prices']) >= 2:
            try:
                p1, p2 = m['prices'][0], m['prices'][1]
                if p1 + p2 < 0.98:
                    print(f"   ⚡ 套利机会: 价格总和 {p1+p2:.3f} < 1.0")
                    opportunities.append({
                        'market': m['question'],
                        'type': 'ARBITRAGE',
                        'prices': m['prices'],
                        'profit': 1 - (p1 + p2)
                    })
                elif abs(p1 - 0.5) > 0.15:
                    trend = "看涨" if p1 > 0.5 else "看跌"
                    print(f"   📈 趋势: {trend} ({p1:.2f})")
                    opportunities.append({
                        'market': m['question'],
                        'type': 'TREND',
                        'direction': 'YES' if p1 > 0.5 else 'NO',
                        'price': p1
                    })
            except:
                pass
    
    print("\n" + "=" * 60)
    print(f"\n💡 发现 {len(opportunities)} 个潜在机会")
    
    # 保存分析结果
    result = {
        'timestamp': datetime.now().isoformat(),
        'total_markets_analyzed': len(markets),
        'opportunities': opportunities
    }
    
    with open('paper_trading/market_analysis.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"✅ 分析结果已保存: paper_trading/market_analysis.json")
    
    return opportunities

if __name__ == "__main__":
    analyze_markets()
