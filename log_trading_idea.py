#!/usr/bin/env python3
"""
交易想法记录到 Notion
保存所有交易想法供后续分析
"""

import json
import os
from datetime import datetime
from typing import Dict, List

class TradingIdeaLogger:
    """交易想法记录器"""
    
    def __init__(self):
        self.ideas_file = "paper_trading/trading_ideas.json"
        os.makedirs("paper_trading", exist_ok=True)
        
    def log_idea(self, idea: Dict):
        """记录交易想法"""
        # 添加时间戳
        idea["timestamp"] = datetime.now().isoformat()
        idea["date"] = datetime.now().strftime("%Y-%m-%d")
        idea["time"] = datetime.now().strftime("%H:%M")
        
        # 加载现有想法
        ideas = self._load_ideas()
        
        # 添加新想法
        ideas.append(idea)
        
        # 保存
        with open(self.ideas_file, "w", encoding="utf-8") as f:
            json.dump(ideas, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 交易想法已记录: {idea.get('market', 'Unknown')}")
        
        # 同时生成 Markdown 日志
        self._append_to_markdown(idea)
    
    def _load_ideas(self) -> List[Dict]:
        """加载已有想法"""
        if os.path.exists(self.ideas_file):
            with open(self.ideas_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def _append_to_markdown(self, idea: Dict):
        """追加到 Markdown 日志"""
        md_file = "paper_trading/trading_ideas.md"
        
        # 如果是新文件，添加标题
        if not os.path.exists(md_file):
            with open(md_file, "w", encoding="utf-8") as f:
                f.write("# 📝 交易想法日志\n\n")
                f.write("**自动记录所有交易想法和机会**\n\n")
                f.write("---\n\n")
        
        # 追加想法
        with open(md_file, "a", encoding="utf-8") as f:
            f.write(f"## {idea['date']} {idea['time']}\n\n")
            f.write(f"**市场:** {idea.get('market', 'Unknown')}\n\n")
            f.write(f"**操作:** {idea.get('action', 'Unknown')}\n\n")
            f.write(f"**理由:** {idea.get('reason', '')}\n\n")
            f.write(f"**风险:** {idea.get('risk', 'Unknown')}\n\n")
            f.write(f"**建议本金:** ${idea.get('suggested_capital', 0)}\n\n")
            
            if idea.get('screenshot'):
                f.write(f"**截图:** {idea['screenshot']}\n\n")
            
            if idea.get('user_input'):
                f.write(f"**用户输入:** {idea['user_input']}\n\n")
            
            f.write(f"**状态:** 待执行\n\n")
            f.write("---\n\n")
    
    def get_recent_ideas(self, hours: int = 24) -> List[Dict]:
        """获取最近的想法"""
        ideas = self._load_ideas()
        cutoff = datetime.now().timestamp() - (hours * 3600)
        
        recent = []
        for idea in ideas:
            try:
                idea_time = datetime.fromisoformat(idea['timestamp']).timestamp()
                if idea_time > cutoff:
                    recent.append(idea)
            except:
                continue
        
        return recent


def main():
    """测试入口"""
    logger = TradingIdeaLogger()
    
    # 示例想法
    test_idea = {
        "market": "Bitcoin Up or Down - Feb 19",
        "action": "BUY_YES",
        "reason": "技术指标突破，情绪看涨",
        "risk": "中",
        "suggested_capital": 25,
        "screenshot": "market_view_20260219.png",
        "user_input": "手动发现的突破机会"
    }
    
    logger.log_idea(test_idea)
    print("\n最近的想法:")
    for idea in logger.get_recent_ideas(hours=1):
        print(f"  - {idea.get('market')}: {idea.get('action')}")


if __name__ == "__main__":
    main()
