#!/usr/bin/env python3
"""
事件前预警系统
在重点事件前5分钟发送执行提醒
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict

class EventAlertSystem:
    """事件预警系统"""
    
    def __init__(self):
        self.events = self.load_events()
    
    def load_events(self) -> List[Dict]:
        """加载重点事件"""
        return [
            {
                "name": "3月非农就业数据",
                "date": "2026-03-07",
                "time": "08:30",  # UTC+8
                "strategy": "数据驱动",
                "action": "数据发布前5分钟根据预期下注，发布后30分钟平仓",
                "capital": 200
            },
            {
                "name": "3月CPI数据",
                "date": "2026-03-12", 
                "time": "08:30",
                "strategy": "情绪套利",
                "action": "对比情绪指标与市场价格，偏离>10%时入场",
                "capital": 300
            },
            {
                "name": "美联储3月利率决议",
                "date": "2026-03-19",
                "time": "02:00",  # FOMC公布时间
                "strategy": "跨平台对冲",
                "action": "在Polymarket和Kalshi之间寻找价差套利",
                "capital": 400
            }
        ]
    
    def check_upcoming_events(self) -> List[Dict]:
        """检查即将发生的事件"""
        now = datetime.now()
        alerts = []
        
        for event in self.events:
            event_dt = datetime.strptime(
                f"{event['date']} {event['time']}", 
                "%Y-%m-%d %H:%M"
            )
            
            # 计算距离事件的时间
            time_diff = event_dt - now
            minutes_until = time_diff.total_seconds() / 60
            
            # 提前5分钟预警
            if 0 < minutes_until <= 5:
                alerts.append({
                    **event,
                    "minutes_until": int(minutes_until),
                    "urgency": "critical"
                })
            # 提前1小时提醒
            elif 55 <= minutes_until <= 65:
                alerts.append({
                    **event,
                    "minutes_until": int(minutes_until),
                    "urgency": "prepare"
                })
        
        return alerts
    
    def generate_alert_message(self, alerts: List[Dict]) -> str:
        """生成预警消息"""
        if not alerts:
            return None
        
        message = "🚨 **Polymarket 事件预警**\n\n"
        
        for alert in alerts:
            if alert["urgency"] == "critical":
                message += f"🔥 **{alert['name']}**\n"
                message += f"⏰ **{alert['minutes_until']}分钟后执行**\n"
                message += f"💰 本金: ${alert['capital']}\n"
                message += f"📋 策略: {alert['strategy']}\n"
                message += f"🎯 行动: {alert['action']}\n\n"
            else:
                message += f"⏳ **{alert['name']}**\n"
                message += f"🕐 约1小时后开始\n"
                message += f"📋 策略: {alert['strategy']}\n"
                message += f"💰 准备本金: ${alert['capital']}\n\n"
        
        message += "---\n"
        message += "⚠️ 请确认:\n"
        message += "- [ ] Polymarket 已登录\n"
        message += "- [ ] 资金已到位\n"
        message += "- [ ] 情绪数据已采集\n"
        
        return message
    
    def save_alert_log(self, alerts: List[Dict]):
        """保存预警日志"""
        if not alerts:
            return
        
        date_str = datetime.now().strftime("%Y%m%d_%H%M")
        log_file = f"alerts/alert_{date_str}.json"
        
        import os
        os.makedirs("alerts", exist_ok=True)
        
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "alerts": alerts
            }, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 预警日志保存: {log_file}")


def main():
    """主入口"""
    alert_system = EventAlertSystem()
    alerts = alert_system.check_upcoming_events()
    
    if alerts:
        message = alert_system.generate_alert_message(alerts)
        print(message)
        alert_system.save_alert_log(alerts)
        
        # 发送 Discord 通知 (如果配置了 webhook)
        import os
        webhook_url = os.environ.get("DISCORD_WEBHOOK")
        if webhook_url:
            import requests
            requests.post(webhook_url, json={"content": message})
    else:
        print("✅ 暂无临近事件")


if __name__ == "__main__":
    main()
