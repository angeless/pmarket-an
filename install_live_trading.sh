#!/bin/bash
# Polymarket 真实交易环境安装脚本

echo "============================================"
echo "🔥 Polymarket 真实交易环境安装"
echo "============================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

echo "✅ Python3 已安装"

# 安装依赖
echo ""
echo "📦 安装依赖..."
pip3 install py-clob-client --break-system-packages 2>/dev/null || pip3 install py-clob-client

echo ""
echo "✅ 安装完成！"
echo ""
echo "============================================"
echo "下一步："
echo "============================================"
echo ""
echo "1. 确保你已经："
echo "   - 登录过 https://polymarket.com"
echo "   - 有 MetaMask 钱包（Polygon 网络）"
echo "   - 钱包里有 USDC 和少量 ETH（gas）"
echo ""
echo "2. 配置交易环境："
echo "   python3 setup_trading.py setup"
echo ""
echo "3. 生成 API 凭证："
echo "   python3 setup_trading.py creds"
echo ""
echo "4. 测试连接："
echo "   python3 setup_trading.py test"
echo ""
echo "5. 开始交易："
echo "   python3 live_trader.py balance"
echo ""
echo "⚠️  警告：涉及真实资金，请谨慎操作！"
echo "============================================"
