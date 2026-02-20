#!/bin/bash
# Polymarket 三大策略启动器

echo "========================================"
echo "🚀 Polymarket 套利策略工具箱"
echo "========================================"
echo ""

# 显示菜单
echo "选择要运行的策略:"
echo ""
echo "1) 🔥 跨平台套利监控 (Kalshi vs Polymarket)"
echo "2) 🔍 低效市场捡漏扫描"
echo "3) 📊 情绪量化分析"
echo "4) ⚡ 运行全部策略"
echo "5) 📈 查看当前持仓状态"
echo ""
echo "0) 退出"
echo ""

read -p "请输入选项 (0-5): " choice

case $choice in
    1)
        echo ""
        echo "启动跨平台套利监控..."
        python3 cross_platform_monitor.py
        ;;
    2)
        echo ""
        echo "启动低效市场扫描..."
        python3 inefficient_market_scanner.py
        ;;
    3)
        echo ""
        echo "启动情绪分析..."
        python3 sentiment_analyzer.py
        ;;
    4)
        echo ""
        echo "运行全部策略..."
        echo ""
        echo "【1/3】跨平台套利监控"
        python3 cross_platform_monitor.py
        echo ""
        echo "【2/3】低效市场扫描"
        python3 inefficient_market_scanner.py
        echo ""
        echo "【3/3】情绪分析"
        python3 sentiment_analyzer.py
        ;;
    5)
        echo ""
        echo "查看持仓状态..."
        python3 check_position.py 2>/dev/null || echo "check_position.py 未找到"
        cat paper_trading/portfolio.json 2>/dev/null | python3 -m json.tool
        ;;
    0)
        echo "退出"
        exit 0
        ;;
    *)
        echo "无效选项"
        ;;
esac
