#!/bin/bash
# Polymarket 自动化监控系统启动脚本

echo "🚀 启动 Polymarket 监控系统..."
echo "================================"

# 设置环境
export GIT_SSH_COMMAND="ssh -i ~/.ssh/pmarket_deploy -o StrictHostKeyChecking=no"

cd ~/pmarket-an || exit 1

# 检查是否在 Git 仓库中
if [ ! -d ".git" ]; then
    echo "❌ 不在 Git 仓库中"
    exit 1
fi

# 运行每日监控
echo ""
echo "📊 运行每日情绪监控..."
python3 daily_sentiment_monitor.py

# 运行事件预警
echo ""
echo "🚨 检查事件预警..."
python3 event_alert_system.py

echo ""
echo "================================"
echo "✅ 监控完成"
echo "时间: $(date)"
