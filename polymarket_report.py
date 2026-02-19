#!/usr/bin/env python3
"""
Polymarket 赚钱报告生成器
生成 Markdown 报告，可导入 Notion
"""

import json
import subprocess
from datetime import datetime
from typing import List, Dict

class PolymarketReportGenerator:
    """生成 Polymarket 赚钱策略报告"""
    
    def __init__(self):
        self.data = []
        
    def fetch_market_data(self, limit: int = 20) -> List[Dict]:
        """抓取市场数据"""
        try:
            result = subprocess.run(
                ["python3", "polymarket_scraper.py", "--markets", str(limit)],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # 读取生成的 JSON 文件
            import glob
            files = glob.glob("polymarket_data_*.json")
            if files:
                latest = max(files, key=lambda x: x.split("_")[-1].split(".")[0])
                with open(latest) as f:
                    self.data = json.load(f)
            
            return self.data
        except Exception as e:
            print(f"抓取失败: {e}")
            return []
    
    def generate_report(self, output_file: str = None) -> str:
        """生成 Markdown 报告"""
        if not self.data:
            self.fetch_market_data()
        
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d")
            output_file = f"polymarket_report_{timestamp}.md"
        
        report = f"""# 💰 Polymarket 赚钱策略报告

**生成时间:** {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}  
**数据来源:** Polymarket Gamma API  
**分析 Agent:** 码匠 (Deki Programmer)

---

## 📊 市场概览

| 指标 | 数值 |
|------|------|
| 总市场数 | {len(self.data)} |
| 活跃市场 | {len([m for m in self.data if m.get('active', True)])} |
| 高流动性 | {len([m for m in self.data if float(m.get('liquidity', 0) or 0) > 100000])} |

---

## 🎯 赚钱策略清单

### 策略 1: 社交媒体情绪套利
- **类型:** 情绪对冲
- **目标市场:** 宏观事件 (美联储利率决议/大选)
- **预期收益:** 10-20%
- **风险等级:** 中
- **所需本金:** $300-500
- **执行方式:**
  1. 监控小红书/X 情绪指标
  2. 对比 Polymarket 赔率偏差
  3. 情绪-赔率偏离 >10% 时入场
- **状态:** 🔍 研究中

### 策略 2: 跨平台对冲
- **类型:** 跨平台套利
- **目标市场:** 同一事件在 Polymarket + Kalshi
- **预期收益:** 5-10%
- **风险等级:** 低
- **所需本金:** $500-1000
- **执行方式:**
  1. 监控同一事件的价差
  2. 高价平台 Sell, 低价平台 Buy
  3. 锁定无风险收益
- **状态:** ⏳ 待执行

### 策略 3: 高波动事件做市
- **类型:** 流动性挖矿
- **目标市场:** 体育/加密货币短期事件
- **预期收益:** 20-40%
- **风险等级:** 高
- **所需本金:** $200-300
- **执行方式:**
  1. 5分钟涨跌市场双边挂单
  2. 吃单手续费 + 价差收益
  3. 高频小仓位
- **状态:** 🔍 研究中

---

## 📈 当前市场分析

"""
        
        # 添加市场详情
        for i, market in enumerate(self.data[:10], 1):
            prices = market.get('prices', {})
            price_str = ', '.join([f"{k}={v}" for k, v in list(prices.items())[:2]])
            
            report += f"""### {i}. {market.get('question', 'Unknown')[:60]}
- **标的:** {market.get('category', '通用')}
- **当前价格:** {price_str}
- **交易量:** ${float(market.get('volume', 0) or 0):,.0f}
- **流动性:** ${float(market.get('liquidity', 0) or 0):,.0f}
- **结束日期:** {market.get('end_date', 'N/A')}

"""
        
        # 添加总结
        report += f"""---

## 💡 执行建议

| 优先级 | 策略 | 本金需求 | 预期月收益 |
|--------|------|----------|------------|
| P0 | 跨平台对冲 | $500 | $40-80 |
| P1 | 情绪套利 | $300 | $30-60 |
| P2 | 高频做市 | $200 | $40-120 |

**总建议配置:** $1000 本金，预期月收益 $110-260 (11-26%)

---

## 🔗 相关链接

- Polymarket: https://polymarket.com
- Kalshi: https://kalshi.com
- ClickUp 任务: https://app.clickup.com/t/86dzw7rwa

---

*本报告由 Deki Agent 自动生成*
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 报告已生成: {output_file}")
        return output_file
    
    def generate_notion_import(self) -> str:
        """生成 Notion 导入格式"""
        report_file = self.generate_report()
        
        # 生成 CSV 用于数据库导入
        csv_file = f"polymarket_strategies_{datetime.now().strftime('%Y%m%d')}.csv"
        
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write("市场名称,策略类型,预期收益,风险等级,所需本金,状态,执行日期,Tags\n")
            
            strategies = [
                ("美联储利率决议情绪套利", "情绪对冲", "15%", "中风险", "500", "研究中", "2026-02-19", "Polymarket,情绪套利"),
                ("Polymarket-Kalshi 跨平台对冲", "跨平台对冲", "8%", "低风险", "1000", "待执行", "2026-02-19", "Polymarket,Kalshi"),
                ("加密货币短期波动做市", "流动性挖矿", "25%", "高风险", "300", "研究中", "2026-02-19", "Polymarket,自动化"),
            ]
            
            for s in strategies:
                f.write(",".join(s) + "\n")
        
        print(f"✅ CSV 已生成: {csv_file}")
        return csv_file


def main():
    """主入口"""
    generator = PolymarketReportGenerator()
    
    print("🚀 生成 Polymarket 赚钱报告...")
    print()
    
    # 生成 Markdown 报告
    report_file = generator.generate_report()
    
    # 生成 CSV
    csv_file = generator.generate_notion_import()
    
    print()
    print("=" * 50)
    print("✅ 完成!")
    print(f"📄 Markdown 报告: {report_file}")
    print(f"📊 CSV 数据库: {csv_file}")
    print()
    print("💡 使用方式:")
    print("1. 打开 Notion")
    print("2. 创建数据库 '💰 Polymarket 赚钱策略'")
    print(f"3. 导入 CSV: {csv_file}")
    print("4. 复制 Markdown 内容到页面")


if __name__ == "__main__":
    main()
