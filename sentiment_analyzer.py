#!/usr/bin/env python3
"""
情绪量化分析工具
分析社交媒体情绪，发现过度反应机会
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional

class SentimentAnalyzer:
    """情绪分析器"""
    
    def __init__(self):
        # 情感词典（简化版）
        self.positive_words = [
            'bullish', 'pump', 'moon', 'rocket', 'gain', 'profit', 'win',
            '看涨', '涨', '牛', '赚钱', '赢', '利好', '突破', '爆发',
            'good', 'great', 'excellent', 'amazing', 'awesome', 'strong'
        ]
        
        self.negative_words = [
            'bearish', 'dump', 'crash', 'fall', 'loss', 'lose', 'bear',
            '看跌', '跌', '熊', '亏损', '输', '利空', '崩盘', '暴跌',
            'bad', 'terrible', 'awful', 'weak', 'crash', 'dip'
        ]
        
        self.threshold = 0.6  # 情绪极值阈值
    
    def analyze_text_sentiment(self, text: str) -> float:
        """分析单条文本情绪"""
        text_lower = text.lower()
        
        pos_count = sum(1 for word in self.positive_words if word in text_lower)
        neg_count = sum(1 for word in self.negative_words if word in text_lower)
        
        total = pos_count + neg_count
        if total == 0:
            return 0.0  # 中性
        
        # 标准化到 -1 到 +1
        sentiment = (pos_count - neg_count) / max(total, 1)
        return max(-1, min(1, sentiment))
    
    def analyze_batch(self, texts: List[str]) -> Dict:
        """批量分析文本"""
        if not texts:
            return {'score': 0, 'distribution': {'positive': 0, 'neutral': 0, 'negative': 0}}
        
        scores = [self.analyze_text_sentiment(t) for t in texts]
        
        positive = sum(1 for s in scores if s > 0.2)
        negative = sum(1 for s in scores if s < -0.2)
        neutral = len(scores) - positive - negative
        
        avg_score = sum(scores) / len(scores)
        
        return {
            'score': avg_score,
            'distribution': {
                'positive': positive / len(scores),
                'neutral': neutral / len(scores),
                'negative': negative / len(scores)
            },
            'total_texts': len(texts)
        }
    
    def detect_overreaction(self, market_name: str, sentiment: float, price: float) -> Optional[Dict]:
        """检测过度反应"""
        # 情绪-价格偏离度
        # 价格 0.5 对应情绪 0，价格 1.0 对应情绪 +1，价格 0 对应情绪 -1
        expected_sentiment = (price - 0.5) * 2
        deviation = sentiment - expected_sentiment
        
        if abs(deviation) > 0.3:  # 偏离度 > 30%
            if deviation > 0:
                signal = "SELL"  # 情绪过度乐观，卖出
                reason = "情绪过度乐观，价格可能被高估"
            else:
                signal = "BUY"  # 情绪过度悲观，买入
                reason = "情绪过度悲观，价格可能被低估"
            
            return {
                'market': market_name,
                'sentiment': sentiment,
                'price': price,
                'expected_sentiment': expected_sentiment,
                'deviation': deviation,
                'signal': signal,
                'reason': reason,
                'confidence': abs(deviation),
                'timestamp': datetime.now().isoformat()
            }
        
        return None
    
    def mock_fetch_tweets(self, keyword: str, count: int = 100) -> List[str]:
        """模拟获取推文（实际需要Twitter API）"""
        # 这里模拟一些推文数据
        mock_tweets = {
            'trump': [
                "Trump is going to win! Bullish on this prediction",
                "No way Trump loses, market is wrong",
                "I'm bearish on Trump, too much controversy",
                "Trump pump incoming! 🚀",
                "People are sleeping on Trump's chances",
            ],
            'bitcoin': [
                "BTC is pumping! To the moon!",
                "Bearish on Bitcoin right now",
                "Bitcoin looking strong, bullish",
                "Crypto crash incoming, be careful",
                "Moon mission started for BTC",
            ],
            'default': [
                "This market is going up!",
                "Not sure about this one",
                "Definitely going to happen",
                "No chance this happens",
                "Market is wrong here",
            ]
        }
        
        return mock_tweets.get(keyword.lower(), mock_tweets['default']) * (count // 5)
    
    def analyze_market_sentiment(self, market_name: str, keyword: str, price: float) -> Dict:
        """分析特定市场的情绪"""
        print(f"🔍 分析 {market_name} 情绪...")
        
        # 获取推文
        tweets = self.mock_fetch_tweets(keyword, 50)
        
        # 分析情绪
        analysis = self.analyze_batch(tweets)
        
        # 检测过度反应
        overreaction = self.detect_overreaction(market_name, analysis['score'], price)
        
        result = {
            'market': market_name,
            'keyword': keyword,
            'price': price,
            'sentiment_analysis': analysis,
            'overreaction': overreaction,
            'sample_tweets': tweets[:3]  # 示例推文
        }
        
        return result
    
    def generate_signal_report(self, results: List[Dict]) -> str:
        """生成交易信号报告"""
        report = f"""# 📊 情绪量化交易信号报告

**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}

---

## 🚨 过度反应交易信号

"""
        
        signals = [r for r in results if r['overreaction']]
        
        if signals:
            for i, sig in enumerate(signals, 1):
                opp = sig['overreaction']
                report += f"""### {i}. {opp['market']}
- **当前价格:** {opp['price']:.2f}
- **情绪指数:** {opp['sentiment']:.2f} (范围: -1到+1)
- **预期情绪:** {opp['expected_sentiment']:.2f}
- **偏离度:** {opp['deviation']:.2f}
- **交易信号:** **{opp['signal']}**
- **置信度:** {opp['confidence']*100:.0f}%
- **理由:** {opp['reason']}

**情绪分布:**
- 乐观: {sig['sentiment_analysis']['distribution']['positive']*100:.0f}%
- 中性: {sig['sentiment_analysis']['distribution']['neutral']*100:.0f}%
- 悲观: {sig['sentiment_analysis']['distribution']['negative']*100:.0f}%

---

"""
        else:
            report += "当前无过度反应信号，市场情绪与价格匹配。\n\n"
        
        report += f"""## 📈 情绪监控说明

### 情绪指数解读
- **+0.6 ~ +1.0**: 极度乐观 → 考虑卖出
- **+0.2 ~ +0.6**: 乐观
- **-0.2 ~ +0.2**: 中性
- **-0.6 ~ -0.2**: 悲观
- **-1.0 ~ -0.6**: 极度悲观 → 考虑买入

### 交易逻辑
当情绪与价格出现偏离时：
- 情绪 > 价格反映 → 市场过度乐观 → **卖出**
- 情绪 < 价格反映 → 市场过度悲观 → **买入**

---

*报告由 SentimentAnalyzer 自动生成*
"""
        
        return report
    
    def run_demo(self):
        """运行演示"""
        print("=" * 60)
        print("📊 情绪量化分析工具")
        print("=" * 60)
        print()
        
        # 分析几个市场
        markets = [
            ('Trump 2026', 'trump', 0.58),
            ('Bitcoin $1M', 'bitcoin', 0.48),
            ('OKC Thunder', 'okc', 0.35),
        ]
        
        results = []
        for name, keyword, price in markets:
            result = self.analyze_market_sentiment(name, keyword, price)
            results.append(result)
            
            print(f"\n{name}:")
            print(f"  情绪指数: {result['sentiment_analysis']['score']:.2f}")
            print(f"  分布: 乐观{result['sentiment_analysis']['distribution']['positive']*100:.0f}% / "
                  f"中性{result['sentiment_analysis']['distribution']['neutral']*100:.0f}% / "
                  f"悲观{result['sentiment_analysis']['distribution']['negative']*100:.0f}%")
            
            if result['overreaction']:
                opp = result['overreaction']
                print(f"  🚨 信号: {opp['signal']} - {opp['reason']}")
            else:
                print(f"  ✅ 情绪与价格匹配")
        
        # 生成报告
        report = self.generate_signal_report(results)
        
        # 保存
        filename = f"sentiment_report_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n💾 报告已保存: {filename}")
        print("\n" + "=" * 60)
        print("提示: 接入Twitter API后可获取真实数据")
        print("=" * 60)


def main():
    """主入口"""
    analyzer = SentimentAnalyzer()
    analyzer.run_demo()


if __name__ == "__main__":
    main()
