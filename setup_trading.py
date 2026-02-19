#!/usr/bin/env python3
"""
Polymarket 真实交易客户端配置
步骤：
1. 获取 Polygon 钱包私钥
2. 登录 Polymarket.com 获取代理钱包地址
3. 生成 API 凭证
4. 测试连接
"""

import os
import json
from datetime import datetime

CONFIG_FILE = "paper_trading/polymarket_config.json"

def setup_config():
    """设置配置文件"""
    print("=" * 60)
    print("🔐 Polymarket 真实交易配置")
    print("=" * 60)
    print()
    
    print("⚠️  警告：此配置将涉及真实资金和私钥")
    print("   请确保：")
    print("   1. 你已经登录过 Polymarket.com")
    print("   2. 你有 Polygon 钱包（MetaMask）")
    print("   3. 钱包里有 USDC 和少量 ETH（gas）")
    print()
    
    config = {}
    
    # 1. 私钥
    print("步骤 1: Polygon 钱包私钥")
    print("-" * 40)
    print("从 MetaMask 导出私钥（以 0x 开头）")
    private_key = input("输入私钥: ").strip()
    if private_key:
        config["private_key"] = private_key
    
    print()
    
    # 2. 代理钱包地址（Funder）
    print("步骤 2: Polymarket 代理钱包地址")
    print("-" * 40)
    print("登录 https://polymarket.com/settings")
    print("查看 'Deposit Address' 或 'Wallet Address'")
    funder = input("输入地址: ").strip()
    if funder:
        config["funder_address"] = funder
    
    print()
    
    # 3. API 凭证（留空，稍后自动生成）
    print("步骤 3: API 凭证")
    print("-" * 40)
    print("API 凭证将通过 L1 认证自动生成")
    config["api_credentials"] = None
    
    # 4. 其他设置
    config["chain_id"] = 137  # Polygon mainnet
    config["host"] = "https://clob.polymarket.com"
    config["created_at"] = datetime.now().isoformat()
    
    # 保存配置
    os.makedirs("paper_trading", exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    
    print()
    print("✅ 配置已保存到:", CONFIG_FILE)
    print()
    print("下一步：运行 generate_credentials.py 生成 API 凭证")


def generate_credentials():
    """生成 API 凭证"""
    try:
        from py_clob_client.client import ClobClient
    except ImportError:
        print("❌ 请先安装 py-clob-client:")
        print("   pip install py-clob-client")
        return
    
    # 加载配置
    if not os.path.exists(CONFIG_FILE):
        print("❌ 配置文件不存在，请先运行 setup_config.py")
        return
    
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
    
    private_key = config.get("private_key")
    funder = config.get("funder_address")
    
    if not private_key or not funder:
        print("❌ 配置不完整，请先运行 setup_config.py")
        return
    
    print("=" * 60)
    print("🔑 生成 API 凭证")
    print("=" * 60)
    print()
    
    try:
        client = ClobClient(
            host=config["host"],
            chain_id=config["chain_id"],
            key=private_key,
            signature_type=1,  # POLY_PROXY
            funder=funder
        )
        
        print("正在生成 API 凭证...")
        creds = client.create_or_derive_api_creds()
        
        config["api_credentials"] = {
            "api_key": creds.apiKey,
            "secret": creds.secret,
            "passphrase": creds.passphrase
        }
        
        # 保存
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        
        print()
        print("✅ API 凭证生成成功！")
        print(f"   API Key: {creds.apiKey[:20]}...")
        print()
        print("现在可以运行真实交易脚本了！")
        
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        print()
        print("常见问题：")
        print("1. 私钥格式错误（需要 0x 开头）")
        print("2. Funder 地址错误（不是 MetaMask 地址，而是 Polymarket 代理地址）")
        print("3. 网络连接问题")
        print("4. 需要先访问 Polymarket.com 激活账户")


def test_connection():
    """测试连接"""
    try:
        from py_clob_client.client import ClobClient
    except ImportError:
        print("❌ 请先安装 py-clob-client")
        return
    
    if not os.path.exists(CONFIG_FILE):
        print("❌ 配置文件不存在")
        return
    
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
    
    creds = config.get("api_credentials")
    if not creds:
        print("❌ 没有 API 凭证，请先运行 generate_credentials.py")
        return
    
    print("=" * 60)
    print("🧪 测试连接")
    print("=" * 60)
    print()
    
    try:
        from py_clob_client.client import ClobClient, ApiCreds
        
        client = ClobClient(
            host=config["host"],
            chain_id=config["chain_id"],
            key=config["private_key"],
            creds=ApiCreds(
                api_key=creds["api_key"],
                api_secret=creds["secret"],
                api_passphrase=creds["passphrase"]
            ),
            signature_type=1,
            funder=config["funder_address"]
        )
        
        # 测试获取余额
        print("正在获取账户信息...")
        balance = client.get_balance()
        print()
        print("✅ 连接成功！")
        print(f"   余额信息: {balance}")
        
    except Exception as e:
        print(f"❌ 连接失败: {e}")


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 setup_trading.py setup     # 配置基本信息")
        print("  python3 setup_trading.py creds     # 生成 API 凭证")
        print("  python3 setup_trading.py test      # 测试连接")
        return
    
    command = sys.argv[1]
    
    if command == "setup":
        setup_config()
    elif command == "creds":
        generate_credentials()
    elif command == "test":
        test_connection()
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
