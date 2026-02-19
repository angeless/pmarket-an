# 🎮 Polymarket 模拟投资系统使用指南

## 💰 模拟投资参数

- **初始本金:** $100 USD
- **交易周期:** 7天（2026-02-19 至 2026-02-26）
- **交易频率:** 高频（每日最多5笔）
- **目标:** 测试策略，记录收益

---

## 📋 工作流程

### 每日流程

1. **早上 (09:00 UTC)**
   - 查看自动生成的情绪监控报告
   - 确定今日关注的市场

2. **盘中 (随时)**
   - 寻找交易机会（情绪-价格偏离 >10%）
   - 截图记录当前价格
   - 告诉我买入信息

3. **交易执行**
   - 我告诉你交易决策
   - 你截图保存买入/卖出价格
   - 我记录到系统中

4. **收盘后**
   - 生成当日交易报告
   - 计算当日收益
   - 推送到 GitHub

---

## 📝 记录交易的方法

### 方法 1: 直接告诉我

在 Discord 发送：
```
买入
市场: Bitcoin Up or Down - Feb 19
方向: YES
价格: 0.52
金额: $30
理由: 技术指标看涨，社交媒体情绪积极
截图: buy_btc_20260219.png
```

我会自动记录到系统。

### 方法 2: 使用快速记录工具

```bash
cd ~/pmarket-an
python3 quick_trade.py buy "BTC Up" YES 0.52 30 "看涨" "screenshot.png"
```

### 方法 3: 在 Python 中操作

```python
from paper_trading_system import PaperTradingSystem

system = PaperTradingSystem(initial_capital=100.0)

# 买入
trade = system.buy(
    market="Bitcoin Up or Down - Feb 19",
    side="YES",
    price=0.52,
    amount=30.0,
    reason="看涨趋势",
    screenshot="buy_btc.png"
)

# 卖出
system.sell(
    market="Bitcoin Up or Down - Feb 19",
    side="YES",
    exit_price=0.58,
    reason="止盈",
    screenshot="sell_btc.png"
)

# 查看状态
summary = system.get_portfolio_summary()
print(f"总盈亏: ${summary['total_pnl']:+.2f}")

# 生成日报
report = system.generate_daily_report()
```

---

## 📸 截图要求

每次交易必须截图保存：

### 买入截图
- 市场名称
- 当前价格（Yes/No）
- 交易量/流动性
- 时间戳

### 卖出截图
- 市场名称
- 卖出价格
- 盈亏情况
- 时间戳

**截图命名规则:**
- 买入: `buy_[market]_[YYYYMMDD]_[HHMMSS].png`
- 卖出: `sell_[market]_[YYYYMMDD]_[HHMMSS].png`

---

## 📊 查看记录

### 实时查看
```bash
# 查看投资组合状态
python3 quick_trade.py status

# 生成日报
python3 quick_trade.py report
```

### 文件位置
```
paper_trading/
├── portfolio.json              # 投资组合状态
├── trades/                     # 所有交易记录
│   ├── TRADE_20260219_001.json
│   └── ...
├── screenshots/                # 截图保存目录
│   ├── buy_btc_20260219.png
│   └── ...
├── daily_reports/              # 每日报告
│   ├── report_20260219.md
│   └── ...
├── TRADING_LOG.md             # 交易日志
└── today_plan.json            # 今日计划
```

---

## 🎯 交易策略提醒

### 每日检查清单
- [ ] 查看情绪监控报告
- [ ] 确定今日目标市场
- [ ] 设置价格提醒
- [ ] 准备截图工具
- [ ] 确认资金分配

### 交易规则
1. **单笔不超过 $30** (本金的 30%)
2. **每日最多 5 笔交易**
3. **止损线 -15%**
4. **必须记录理由和截图**

### 重点关注
- 加密货币短期涨跌（5分钟/小时）
- 体育事件（赛前波动）
- 政治事件（新闻驱动）

---

## 📈 收益计算

### 每日结算
- 现金余额
- 持仓市值
- 当日盈亏
- 累计收益率

### 一周总结
- 总交易次数
- 胜率
- 最大单笔盈利
- 最大单笔亏损
- 最终收益率

---

## 🔄 自动化支持

已配置的自动任务：

| 任务 | 频率 | 输出 |
|------|------|------|
| 情绪监控报告 | 每天 09:00 UTC | `daily_sentiment_YYYY-MM-DD.md` |
| 事件预警 | 每 5 分钟 | Discord 通知 |
| 交易记录备份 | 每笔交易后 | GitHub 推送 |

---

## 📞 如何与我协作

### 发现交易机会时
发送给我：
1. 市场名称
2. 当前价格
3. 你的分析/理由
4. 截图

我会：
1. 记录买入交易
2. 更新持仓
3. 计算潜在收益
4. 生成记录文件

### 平仓时
发送给我：
1. 市场名称
2. 卖出价格
3. 盈亏情况
4. 截图

我会：
1. 记录卖出交易
2. 计算实际收益
3. 更新投资组合
4. 生成交易总结

---

## 🚀 开始交易

### 第一步：初始化
```bash
cd ~/pmarket-an
python3 start_paper_trading.py
```

### 第二步：寻找机会
- 访问 Polymarket: https://polymarket.com
- 使用 Gmail 登录: deki.angel.partner@gmail.com
- 浏览活跃市场

### 第三步：记录交易
- 发现机会后截图
- 告诉我交易信息
- 我记录到系统

### 第四步：每日复盘
- 查看生成的日报
- 分析交易得失
- 调整次日策略

---

**准备好开始了吗？** 告诉我第一笔交易！
