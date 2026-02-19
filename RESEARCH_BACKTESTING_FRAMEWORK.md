## 📚 开源工具发现：Polymarket 回测框架

**来源:** Reddit r/polymarket_bets  
**原文链接:** https://www.reddit.com/r/polymarket_bets/comments/1r56a0p/currently_making_an_opensource_backtesting/  
**发现时间:** 2026-02-19  
**价值评级:** ⭐⭐⭐⭐⭐ (高价值工具)

---

### 项目概述

**开发者:** Future_Cheek_5077  
**项目类型:** 开源回测框架  
**支持平台:** Polymarket + Kalshi  
**数据集:** ~58GB 未压缩历史数据  
**状态:** 开发中，持续更新

**核心功能:**
- 下载 Polymarket 和 Kalshi 的最大可用数据集
- 支持集成主流回测框架：
  - Nautilus Trader
  - Backtrader
  - Minitrader
  - VectorBT
- 干净的数据/回测基础设施

---

### 为什么这对我们重要

**当前问题:**
- 我们的策略没有经过历史数据验证
- 无法测试"公允价值计算器"的有效性
- 缺乏量化分析工具

**这个框架可以帮我们:**
1. **回测现有策略** - 验证 Jesus vs GTA 等策略的历史表现
2. **优化参数** - 找到最佳的入场/出场价格
3. **风险管理** - 计算最大回撤、夏普比率
4. **新策略开发** - 基于历史数据发现模式

---

### 集成计划

**Phase 1: 获取数据**
```bash
# 下载框架
# 获取 58GB 历史数据
# 了解数据结构
```

**Phase 2: 回测现有策略**
- Jesus vs GTA 策略
- OKC Thunder 策略
- BTC $1M 策略
- 验证我们的认知变现理论

**Phase 3: 开发公允价值计算器**
- 基于历史数据训练模型
- 测试预测准确性
- 集成到交易决策中

**Phase 4: 自动化交易**
- 策略验证通过后
- 接入 CLOB API
- 自动执行回测通过的策略

---

### 立即行动项

**需要做的:**
1. **Star GitHub 仓库** - 关注项目进展
2. **下载数据集** - 获取 58GB 历史数据
3. **学习框架** - 了解如何使用 backtrader/vectorBT
4. **回测现有持仓** - 验证我们的5个策略

**GitHub 搜索关键词:**
- "Polymarket backtesting"
- "Kalshi backtesting framework"
- "prediction markets backtest"

---

### 待创建 ClickUp 任务

- [ ] 研究开源回测框架 GitHub 仓库
- [ ] 下载 58GB Polymarket 历史数据集
- [ ] 学习 backtrader/vectorBT 使用方法
- [ ] 回测 Jesus vs GTA 策略（发现错误前）
- [ ] 回测当前 5 个持仓的历史表现
- [ ] 基于历史数据开发公允价值模型
- [ ] 验证"认知变现"策略的有效性

---

### 与当前研究的关联

**PolyPredict AI (之前发现):**
- 浏览器插件，实时计算公允价值
- 但无法验证其准确性

**这个开源框架:**
- 可以基于历史数据验证类似策略
- 可以自己开发"PolyPredict 替代品"
- 量化验证我们的交易逻辑

**结论:**
这个工具是我们从"感性交易"升级到"量化交易"的关键基础设施。

---

*发现来源: r/polymarket_bets (用户手动分享)*  
*工具价值: ⭐⭐⭐⭐⭐ (优先级高)*  
*下一步: 立即创建 ClickUp 任务跟踪*
