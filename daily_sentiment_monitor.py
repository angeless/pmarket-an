#!/usr/bin/env python3
"""
Polymarket 每日情绪监控脚本
自动生成报告并推送 GitHub
"""

import json
import subprocess
from datetime import datetime
from typing import Dict, List
import os

class DailySentimentMonitor:
    """每日情绪监控器"""
    
    def __init__(self):
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.report = {
            "date": self.date,
            "events": [],
            "sentiment": {},
            "opportunities": [],
            "notes": ""
        }
    
    def monitor_events(self) -> List[Dict]:
        """监控重点事件"""
        events = [
            {"name": "美联储3月利率决议", "date": "2026-03-19", "priority": "high", "sentiment": None},
            {"name": "3月CPI数据", "date": "2026-03-12", "priority": "high", "sentiment": None},
            {"name": "3月非农就业", "date": "2026-03-07", "priority": "high", "sentiment": None},
        ]
        return events
    
    def generate_sentiment_report(self) -> Dict:
        """生成情绪报告"""
        return {
            "xiaohongshu": {
                "keywords": ["美联储", "降息", "CPI"],
                "sentiment_score": 0,  # -5 to +5
                "notes": "需人工输入"
            },
            "twitter": {
                "keywords": ["#Fed", "#FOMC", "#CPI"],
                "sentiment_score": 0,
                "notes": "需人工输入"
            }
        }
    
    def identify_opportunities(self, events: List[Dict], sentiment: Dict) -> List[Dict]:
        """识别交易机会"""
        opportunities = []
        
        for event in events:
            days_until = (datetime.strptime(event["date"], "%Y-%m-%d") - datetime.now()).days
            
            if 0 <= days_until <= 7:
                opportunities.append({
                    "event": event["name"],
                    "days_until": days_until,
                    "action": "准备监控",
                    "priority": event["priority"]
                })
        
        return opportunities
    
    def generate_markdown_report(self) -> str:
        """生成 Markdown 报告"""
        report = f"""# 📊 每日情绪监控报告

**日期:** {self.date}  
**生成时间:** {datetime.now().strftime("%H:%M UTC")}  
**Agent:** 码匠

---

## 🎯 重点事件监控

| 事件 | 日期 | 剩余天数 | 优先级 | 状态 |
|------|------|----------|--------|------|
"""
        
        for event in self.report["events"]:
            days = (datetime.strptime(event["date"], "%Y-%m-%d") - datetime.now()).days
            status = "🔥 临近" if days <= 3 else "⏳ 监控中"
            report += f"| {event['name']} | {event['date']} | {days}天 | {event['priority']} | {status} |\n"
        
        report += f"""
---

## 📱 情绪指标

### 小红书
- **监控关键词:** {', '.join(self.report["sentiment"].get("xiaohongshu", {}).get("keywords", []))}
- **情绪评分:** {self.report["sentiment"].get("xiaohongshu", {}).get("sentiment_score", 0)}/5
- **备注:** {self.report["sentiment"].get("xiaohongshu", {}).get("notes", "")}

### X (Twitter)
- **监控关键词:** {', '.join(self.report["sentiment"].get("twitter", {}).get("keywords", []))}
- **情绪评分:** {self.report["sentiment"].get("twitter", {}).get("sentiment_score", 0)}/5
- **备注:** {self.report["sentiment"].get("twitter", {}).get("notes", "")}

---

## 💡 交易机会

"""
        
        if self.report["opportunities"]:
            for opp in self.report["opportunities"]:
                report += f"- **{opp['event']}** ({opp['days_until']}天)\n"
                report += f"  - 行动: {opp['action']}\n"
                report += f"  - 优先级: {opp['priority']}\n\n"
        else:
            report += "暂无临近事件\n"
        
        report += f"""
---

## 📝 今日任务

- [ ] 小红书情绪采集
- [ ] X (Twitter) 情绪采集
- [ ] Polymarket 价格记录
- [ ] 偏离度计算
- [ ] Notion 数据库更新

---

*报告由 Deki Agent 自动生成*
"""
        
        return report
    
    def save_and_push(self):
        """保存报告并推送到 GitHub"""
        # 生成报告
        self.report["events"] = self.monitor_events()
        self.report["sentiment"] = self.generate_sentiment_report()
        self.report["opportunities"] = self.identify_opportunities(
            self.report["events"], 
            self.report["sentiment"]
        )
        
        # 保存 JSON
        json_file = f"reports/daily_sentiment_{self.date}.json"
        os.makedirs("reports", exist_ok=True)
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(self.report, f, ensure_ascii=False, indent=2)
        
        # 保存 Markdown
        md_file = f"reports/daily_sentiment_{self.date}.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(self.generate_markdown_report())
        
        print(f"✅ 报告生成: {md_file}")
        
        # 推送到 GitHub
        try:
            subprocess.run(["git", "add", "reports/"], check=True)
            subprocess.run([
                "git", "commit", "-m", 
                f"Daily sentiment report: {self.date}"
            ], check=True)
            subprocess.run([
                "git", "push", "origin", "main"
            ], check=True, env={
                **os.environ,
                "GIT_SSH_COMMAND": "ssh -i ~/.ssh/pmarket_deploy -o StrictHostKeyChecking=no"
            })
            print("✅ 已推送到 GitHub")
        except Exception as e:
            print(f"⚠️ GitHub 推送失败: {e}")


def main():
    """主入口"""
    monitor = DailySentimentMonitor()
    monitor.save_and_push()
    print(f"\n📊 {monitor.date} 监控报告已完成")


if __name__ == "__main__":
    main()
