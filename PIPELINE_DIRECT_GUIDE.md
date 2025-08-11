# 🚀 Pipeline Direct Mode Guide - `/pipeline` 命令详细指南

## 概述

Pipeline Direct模式是Claude Agents系统的核心功能，通过`/pipeline`命令显式调用完整的5阶段开发流程，并提供专业的实时状态显示。这是进行复杂开发任务的最佳选择。

## 🎯 核心特性

### ✨ 实时状态显示
- 🔍 当前执行的subagent实时显示
- 📊 阶段进度可视化
- ⏱️ 时间估算和剩余时间
- 💬 当前活动详细描述

### 🏗️ 完整开发流程
- **5个核心阶段**：意图分析 → 规划 → 开发 → 评估 → 回滚（如需要）
- **多智能体协作**：Claude + GPT-5 双重分析
- **TDD驱动**：测试驱动开发方法论
- **质量保证**：每阶段质量门检查

## 🚀 快速开始

### 基本用法

```bash
/pipeline <your development request>
```

### 示例

```bash
# 复杂功能开发
/pipeline Convert this authentication system to async with comprehensive tests

# 大型重构
/pipeline Refactor the user management system for better performance and maintainability

# 新功能实现
/pipeline Build a real-time notification system with WebSocket support

# API开发
/pipeline Create a RESTful API for the blog system with authentication
```

## 📋 与其他模式对比

| 特性 | `/pipeline` | `>>pipeline` | `/gpt5` | 自动检测 |
|------|-------------|-------------|---------|----------|
| 实时状态显示 | ✅ | ❌ | ❌ | ❌ |
| 完整5阶段流程 | ✅ | ✅ | ❌ | ✅ |
| 跳过复杂度分析 | ✅ | ❌ | ✅ | ❌ |
| 用户确认交互 | ✅ | ✅ | ❌ | ✅ |
| 专业界面 | ✅ | ❌ | ❌ | ❌ |
| 错误恢复 | ✅ | ✅ | ❌ | ✅ |

## 🔄 Pipeline执行流程

### 阶段1: 意图分析 (Intent Analysis)
```
📍 Stage 1/5: INTENT ANALYSIS
├─ [⚡] intent-cc      ⏳ Claude analyzing user intent...
├─ [📋] intent-gpt5    📋 Waiting...
└─ [📋] intent-merge-cc 📋 Pending...

💬 Current: Claude (intent-cc) is analyzing your request and identifying code touchpoints...
```

**执行内容**：
- Claude分析用户需求和代码上下文
- GPT-5提供技术深度分析
- 合并分析结果为综合意图理解

### 阶段2: 规划 (Planning)
```
📍 Stage 2/5: PLANNING
├─ [✅] plan-cc        ✅ Plan created (2m 30s)
├─ [⚡] plan-gpt5      ⏳ GPT-5 enhancing test coverage...
└─ [📋] plan-merge-cc  📋 Waiting...

💬 Current: GPT-5 (plan-gpt5) is analyzing edge cases and enhancing test coverage...
```

**执行内容**：
- Claude创建TDD驱动的开发计划
- GPT-5增强测试覆盖率和边界用例
- 合并为最终开发计划

### 阶段3: 开发 (Development)
```
📍 Stage 3/5: DEVELOPMENT
├─ [⚡] dev-cc         ⏳ Implementing features with TDD...

Current Milestone: Authentication Module
Progress: ████████░░░░░░░░ 60%
Tests: 8/12 passing

💬 Current: Claude (dev-cc) is implementing async authentication handlers...
```

**执行内容**：
- 遵循TDD方法论执行开发
- 实时显示开发进度
- 测试通过情况监控

### 阶段4: 评估 (Evaluation)
```
📍 Stage 4/5: EVALUATION
├─ [⚡] eval-gpt5      ⏳ GPT-5 evaluating implementation...

💬 Current: GPT-5 (eval-gpt5) is assessing code quality and test coverage...
```

**执行内容**：
- GPT-5全面评估代码质量
- 测试覆盖率分析
- 安全性和性能评估

### 阶段5: 完成/回滚 (Completion/Rollback)
```
🎉 PIPELINE COMPLETED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Duration: 15m 30s
Success Rate: 100%
Tests Passing: 12/12
```

## 🎮 实时状态显示详解

### 状态图标说明
- `[⚡]` - 当前正在执行
- `[✅]` - 成功完成
- `[⏳]` - 等待中/排队
- `[📋]` - 待执行
- `[❌]` - 执行失败
- `[⚠️]` - 需要注意

### 进度条含义
```
Progress: ████████████░░░░░░░░░░ 60% | Elapsed: 8m 45s | Est. Remaining: 6m 20s
```

- **进度条**：当前总体完成百分比
- **Elapsed**：已经消耗的时间
- **Est. Remaining**：预计剩余时间

## 🤝 用户交互点

### 意图确认
```
🤔 USER CONFIRMATION REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stage: Intent Analysis Complete
Result: System will convert authentication to async patterns

Key Points:
• Primary Goal: Async authentication implementation
• Code Touchpoints: 5 files, 12 functions identified
• Estimated Complexity: 7/10
• Time Estimate: 15-20 minutes

❓ Proceed with this understanding? (y/n):
```

### 计划确认
```
🤔 USER CONFIRMATION REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stage: Planning Complete
Result: Comprehensive TDD plan created

Key Points:
• Development Approach: Test-driven development
• Test Cases: 15 unit tests, 5 integration tests
• Milestones: 3 major milestones identified
• Estimated Duration: 18 minutes

❓ Approve this plan and begin implementation? (y/n):
```

## ❗ 错误处理

### Agent超时
```
⚠️ AGENT TIMEOUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agent: plan-gpt5
Duration: 5m 30s
Expected: 3m 00s

The agent is taking longer than expected.
Options:
1. Continue waiting (additional 5 minutes)
2. Retry with fresh agent
3. Skip this agent (if non-critical)

Choice (1-3):
```

### 阶段失败
```
❌ PIPELINE STAGE FAILED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Stage: development
Agent: dev-cc
Error: Test failures preventing deployment

Options:
1. Retry current stage
2. Skip to evaluation (review failures)
3. Abort and rollback changes
4. Manual intervention required

Choice (1-4):
```

## 🎯 使用场景

### 适合使用 `/pipeline` 的场景

#### ✅ 复杂功能开发
- 新功能实现
- 系统集成
- API开发
- 数据库设计

#### ✅ 大型重构项目
- 架构升级
- 性能优化
- 代码现代化
- 安全加固

#### ✅ 需要全面测试的项目
- 关键业务逻辑
- 外部集成
- 安全功能
- 性能敏感代码

#### ✅ 专业开发项目
- 生产环境部署
- 团队协作项目
- 代码审查准备
- 文档完整性要求

### 不适合使用 `/pipeline` 的场景

#### ❌ 简单查询
- 语法问题
- 概念解释
- 快速参考
- 🔄 **替代方案**: 使用 `/gpt5` 或不加前缀

#### ❌ 单文件小改动
- 简单bug修复
- 样式调整
- 配置更改
- 🔄 **替代方案**: 使用自动检测或 `>>quick`

## ⚙️ 高级配置

### 时间估算算法
Pipeline系统使用智能时间估算：
- **历史数据**：基于类似项目的执行时间
- **复杂度评分**：根据代码touchpoints和需求复杂度
- **Agent性能**：考虑各个agent的平均执行时间
- **动态调整**：根据实际执行情况实时调整

### 并行化优化
- **Intent阶段**：Claude和GPT-5可并行分析
- **Planning阶段**：基础计划和增强可并行
- **Development阶段**：测试和实现可交替进行
- **Evaluation阶段**：多维度评估可并行

## 📊 性能指标

### 典型执行时间
- **简单任务** (复杂度 1-3): 5-15分钟
- **中等任务** (复杂度 4-6): 15-30分钟  
- **复杂任务** (复杂度 7-8): 30-60分钟
- **大型项目** (复杂度 9-10): 1-2小时

### 成功率指标
- **Intent分析**: >95% 成功率
- **计划创建**: >90% 成功率
- **开发执行**: >85% 成功率
- **评估通过**: >80% 首次通过率

## 🔧 故障排除

### 常见问题

#### Pipeline卡住不动
**症状**：Status display长时间无更新
**解决方案**：
1. 检查网络连接
2. 确认GPT-5 API密钥有效
3. 检查系统资源使用情况

#### Agent执行失败
**症状**：显示红色错误状态
**解决方案**：
1. 查看错误详细信息
2. 选择重试选项
3. 如果持续失败，选择跳过或回滚

#### 时间估算不准确
**症状**：实际时间远超预估
**解决方案**：
1. 系统会自动学习和改进
2. 复杂项目可能需要人工干预
3. 考虑分解为更小的任务

## 💡 最佳实践

### 1. 清晰描述需求
```bash
# ✅ 好的描述
/pipeline Convert the user authentication system from synchronous to asynchronous patterns, including comprehensive error handling and unit tests

# ❌ 模糊描述  
/pipeline make auth async
```

### 2. 合理估算复杂度
- 单文件修改：简单 (1-3)
- 多文件重构：中等 (4-6)
- 系统级改动：复杂 (7-8)
- 架构重构：非常复杂 (9-10)

### 3. 准备好确认点
- 在意图分析后，准备确认理解是否正确
- 在计划阶段后，准备审查开发计划
- 遇到错误时，准备选择处理方式

### 4. 监控进度
- 留意状态显示中的异常
- 关注时间估算的准确性
- 适时进行人工干预

## 🔗 相关资源

- [GPT-5 Direct Guide](GPT5_DIRECT_GUIDE.md) - GPT-5直接访问指南
- [主README](README.md) - 项目总体介绍
- [测试脚本](test_pipeline_direct.py) - Pipeline测试工具
- [状态显示](scripts/pipeline_status_display.py) - 状态显示系统

## 📝 更新日志

### v1.0.0 (2025-08-11)
- 🎉 初始发布Pipeline Direct模式
- ✨ 实时状态显示系统
- 🔧 完整的5阶段开发流程
- 🤝 用户交互和确认点
- ❗ 智能错误处理和恢复
- 📊 进度可视化和时间估算

---

💡 **提示**：Pipeline Direct模式是进行专业开发的首选方式。它提供完整的开发流程、实时反馈和质量保证，确保您的项目达到生产级别的标准。