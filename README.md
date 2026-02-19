# 📊 Polymarket 赚钱策略研究

**仓库:** pmarket-an  
**目标:** 小本金 ($100-1000) 在预测市场套利  
**预期收益:** 月收益 10-25%  
**更新频率:** 每日自动报告

---

## 📁 文件结构

```
.
├── 📄 POLYMARKET_STRATEGY_GUIDE.md    # 核心策略手册
├── 📄 KALSHI_RESEARCH.md              # Kalshi 平台研究
├── 📄 Q1_2026_EVENTS.md               # Q1 高关注事件
├── 📄 SENTIMENT_MONITORING.md         # 情绪监控清单
├── 📄 PAPER_TRADING_GUIDE.md          # 模拟投资指南 ⭐NEW
├── 🐍 paper_trading_system.py         # 模拟投资核心系统 ⭐NEW
├── 🐍 quick_trade.py                  # 快速交易记录工具 ⭐NEW
├── 📁 paper_trading/                  # 模拟交易数据目录 ⭐NEW
├── 🐍 polymarket_scraper.py           # 数据抓取脚本
├── 🐍 polymarket_report.py            # 报告生成器
├── 🐍 daily_sentiment_monitor.py      # 每日情绪监控 (自动)
├── 🐍 event_alert_system.py           # 事件预警系统 (自动)
└── 🔧 run_monitor.sh                  # 一键启动监控
```

---

## 🎯 核心策略

| 策略 | 本金 | 月收益 | 风险 |
|------|------|--------|------|
| 跨平台对冲 | $400 | 5-10% | ⭐ 低 |
| 情绪套利 | $300 | 10-20% | ⭐⭐ 中 |
| 事件驱动 | $200 | 10-20% | ⭐⭐ 中 |

**$1000 配置:** 月收益 $70-140 (7-14%)

---

## 📅 近期重点事件

| 日期 | 事件 | 策略 |
|------|------|------|
| 3/7 | 非农就业数据 | 数据驱动 |
| 3/12 | CPI 数据 | 情绪套利 |
| 3/18-19 | FOMC 利率决议 | 跨平台对冲 |

---

## 🚀 快速开始

```bash
# 生成每日报告
python3 polymarket_report.py

# 抓取市场数据
python3 polymarket_scraper.py --markets 20

# 同步到 Notion
python3 polymarket_notion_db.py
```

---

## 📊 数据来源

- **Polymarket:** https://polymarket.com
- **Kalshi:** https://kalshi.com
- **情绪监控:** 小红书 + X (Twitter)

---

## 🤖 自动化 (Cron 任务)

| 任务 | 频率 | 功能 |
|------|------|------|
| 每日情绪监控 | 每天 09:00 UTC | 生成监控报告并推送到 GitHub |
| 事件预警检查 | 每 5 分钟 | 检查重点事件，提前5分钟预警 |
| 赚钱报告生成 | 每天 08:00 UTC | 生成策略报告 |

### 手动运行
```bash
# 一键启动所有监控
./run_monitor.sh

# 单独运行每日监控
python3 daily_sentiment_monitor.py

# 单独运行事件预警
python3 event_alert_system.py
```

### 重点事件自动提醒
- **3月7日** 非农就业数据 (提前5分钟预警)
- **3月12日** CPI数据 (提前5分钟预警)
- **3月19日** FOMC利率决议 (提前5分钟预警)

---

**研究 Agent:** 码匠 (Deki Programmer)  
**更新日期:** 2026-02-19

---

## 🎮 模拟投资系统 (Paper Trading)

**本金:** $100 USD  
**周期:** 7天高频交易  
**目标:** 测试策略，记录收益，截图留证

### 当前状态 (实时更新)

| 指标 | 数值 |
|------|------|
| 初始本金 | $100.00 |
| 当前总值 | $103.46 |
| 总盈亏 | +$3.46 (+3.46%) |
| 交易次数 | 1 笔 |
| 胜率 | 100% |

### 快速开始

```bash
# 启动模拟投资系统
python3 start_paper_trading.py

# 记录买入
python3 quick_trade.py buy "BTC Up" YES 0.52 30 "看涨理由" "screenshot.png"

# 记录卖出
python3 quick_trade.py sell "BTC Up" YES 0.58 "止盈理由" "screenshot.png"

# 查看状态
python3 quick_trade.py status

# 生成日报
python3 quick_trade.py report
```

### 交易记录

查看完整交易记录: `paper_trading/trades/`  
查看每日报告: `paper_trading/daily_reports/`  
查看交易日志: `paper_trading/TRADING_LOG.md`
