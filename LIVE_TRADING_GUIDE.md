# 🔥 Polymarket 真实交易接入指南

**警告：** 本指南涉及真实资金交易，请谨慎操作！

---

## 📋 前置条件

1. **Polygon 钱包**（MetaMask）
   - 已安装 MetaMask 浏览器插件
   - 已添加 Polygon 网络
   - 有钱包私钥（导出备用）

2. **Polymarket 账户**
   - 访问过 https://polymarket.com
   - 完成邮箱/Google 登录
   - 账户已激活（有过至少一次登录）

3. **资金准备**
   - USDC（用于交易）
   - 少量 ETH（用于 gas，约 0.01-0.1 ETH）

---

## 🚀 快速开始

### 第一步：安装环境

```bash
cd ~/pmarket-an
chmod +x install_live_trading.sh
./install_live_trading.sh
```

或手动安装：
```bash
pip3 install py-clob-client
```

### 第二步：获取必要信息

#### 1. 导出 MetaMask 私钥
1. 打开 MetaMask
2. 点击账户图标 → "账户详情"
3. 点击 "导出私钥"
4. 输入密码，复制私钥（以 0x 开头）

**⚠️ 安全警告：**
- 私钥 = 你的资产控制权
- 不要泄露给任何人
- 不要截图或保存在不安全的地方

#### 2. 获取 Polymarket 代理钱包地址
1. 访问 https://polymarket.com/settings
2. 查看 "Deposit Address" 或 "Wallet Address"
3. 这个地址是你的 **Funder 地址**（不是 MetaMask 地址！）

**注意：**
- 如果你从未登录过 Polymarket，需要先登录一次
- 这个地址是 Polymarket 为你创建的代理合约地址
- 资金需要转到这里才能交易

### 第三步：配置

```bash
python3 setup_trading.py setup
```

按提示输入：
- 私钥（0x...）
- Funder 地址（0x...）

### 第四步：生成 API 凭证

```bash
python3 setup_trading.py creds
```

这一步会：
1. 使用私钥进行 L1 认证
2. 向 Polymarket 申请 API 凭证
3. 保存 apiKey、secret、passphrase

### 第五步：测试连接

```bash
python3 setup_trading.py test
```

如果显示余额信息，说明配置成功！

---

## 💰 查看余额

```bash
python3 live_trader.py balance
```

---

## 📈 下单交易

### 获取 Token ID

在下单前，需要知道市场的 token ID：

```python
# 从市场数据获取
import requests
response = requests.get("https://gamma-api.polymarket.com/markets")
markets = response.json()

for m in markets:
    if "Trump" in m.get("question", ""):
        print(f"Market: {m['question']}")
        print(f"Token IDs: {m.get('clobTokenIds', [])}")
```

### 买入示例

```bash
python3 live_trader.py buy TOKEN_ID PRICE SIZE

# 示例：以 0.52 的价格买入 $30
python3 live_trader.py buy 0x1234... 0.52 30
```

### 卖出示例

```bash
python3 live_trader.py sell TOKEN_ID PRICE SIZE

# 示例：以 0.58 的价格卖出 $30
python3 live_trader.py sell 0x1234... 0.58 30
```

---

## 📋 查看订单

```bash
# 查看未成交订单
python3 live_trader.py orders
```

---

## ❌ 取消订单

```bash
# 取消特定订单
python3 live_trader.py cancel ORDER_ID

# 取消所有订单
python3 live_trader.py cancel-all
```

---

## 📝 交易记录

所有交易自动记录在：
- `paper_trading/real_trades.json`
- GitHub 同步

---

## ⚠️ 风险提示

1. **资金风险**
   - 预测市场有亏损可能
   - 不要投入无法承受损失的资金
   - 建议从小额开始测试

2. **技术风险**
   - 私钥泄露 = 资金被盗
   - 交易不可逆
   - 网络拥堵可能导致交易失败

3. **合规风险**
   - 确保你所在地区允许使用 Polymarket
   - 遵守当地法律法规
   - 注意税务申报义务

---

## 🔧 故障排除

### Error: INVALID_SIGNATURE
- 检查私钥格式（需要 0x 开头）
- 确保使用正确的私钥

### Error: Invalid Funder Address
- Funder 必须是 Polymarket 代理地址
- 不是 MetaMask 钱包地址
- 查看 https://polymarket.com/settings

### Error: NONCE_ALREADY_USED
- 运行 `setup_trading.py creds` 重新生成

### 余额显示为 0
- 确保资金在 Polygon 网络
- 确保资金在 Polymarket 代理地址
- 可能需要先充值到 Polymarket

---

## 📞 需要帮助？

1. Polymarket 官方文档：https://docs.polymarket.com
2. Discord 社区：https://discord.gg/polymarket
3. 查看 GitHub Issues

---

**准备好了吗？开始你的第一笔真实交易吧！** 🚀
