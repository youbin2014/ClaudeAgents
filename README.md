# 🚀 Claude Agents Pipeline

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/youbin2014/ClaudeAgents)

> **智能多步骤任务处理系统** - 为Claude Code提供专业的pipeline执行能力

## 🎯 核心特性

- **🎯 智能路由** - 自动选择最佳执行模式
- **🔄 异步转换** - 专业的同步→异步代码转换  
- **🏗️ 多步骤管道** - 复杂任务的结构化处理
- **🚀 跨平台支持** - Windows/WSL, Linux, macOS
- **🛡️ 完全兼容** - 与Claude Code Memory系统无冲突

## ⚡ 快速开始

### 一键安装

```bash
git clone https://github.com/youbin2014/ClaudeAgents.git
cd ClaudeAgents
bash install.sh
```

### 配置API密钥

编辑生成的 `.env` 文件：
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

或使用配置工具：
```bash
python scripts/configure_api.py
```

## 🎮 使用方法

### 触发方式（重要更新）

**避免符号冲突**：经测试发现`@`和`#`符号与Claude Code内置功能冲突，现改用`>>`前缀

**新的触发方式**：
- `/pipeline` - 显式调用完整pipeline，包含实时状态显示
- `/gpt5` - 直接访问GPT-5，绕过pipeline获得即时响应
- `/gpt5-mini` - 使用GPT-5 mini模型（更快速）
- `/gpt5-nano` - 使用GPT-5 nano模型（最快速）
- `>>pipeline` - 强制使用复杂任务pipeline模式（传统方式）
- `>>quick` - 强制使用快速响应模式  
- 自动检测 - 不加前缀时系统自动判断

### 使用示例

```bash
# 显式pipeline - 完整开发流程，实时状态显示
/pipeline Convert this authentication system to async with comprehensive tests

# 直接GPT-5查询 - 绕过pipeline获得即时响应
/gpt5 Explain the performance implications of async/await in Python

# 使用GPT-5 mini进行快速响应
/gpt5-mini What's the difference between Promise and async/await?

# 复杂任务 - 传统pipeline方式
>>pipeline Convert this authentication system to async with comprehensive tests

# 快速查询 - 明确指定快速模式
>>quick What is the syntax for async functions?

# 自动检测 - 系统根据复杂度判断
Convert this function to use modern async patterns
```

## 🏗️ 架构

```
User Query → Router → Intent Analysis → Planning → Development → Evaluation
    ↓          ↓                                                      ↓
  Command?   Quick Response                                  Rollback (if failed)
    ↓
  /pipeline → Pipeline Direct (实时状态显示)
  /gpt5     → GPT-5 Direct
```

## 🤖 Pipeline阶段

### Stage 0: 路由
- **`router`**: 决定使用Pipeline直接模式、GPT-5直接模式、快速响应或完整pipeline模式
- **`pipeline-direct`**: 处理/pipeline命令，执行完整pipeline并提供实时状态显示
- **`gpt5-direct`**: 处理/gpt5命令，直接调用GPT-5 API（绕过pipeline）

### Stage 1: 意图理解
- **`intent-cc`**: Claude分析用户意图和代码上下文
- **`intent-gpt5`**: GPT-5专注代码接触点和技术细节
- **`intent-merge-cc`**: 合并洞察为综合意图分析

### Stage 2: 规划 (TDD优先)
- **`plan-cc`**: Claude生成测试驱动开发计划
- **`plan-gpt5`**: GPT-5增强边界情况和边界测试
- **`plan-merge-cc`**: 创建最终综合开发计划

### Stage 3: 开发
- **`dev-cc`**: 遵循TDD方法论执行开发

### Stage 4: 评估
- **`eval-gpt5`**: GPT-5评估结果和测试覆盖率

### Stage 5: 回滚 (如需要)
- **`rollback-cc`**: 评估失败时安全恢复更改

## 📁 项目结构

```
.claude/agents/          # Claude Code子代理定义
├── router.md           # 查询路由逻辑
├── intent-cc.md        # Claude意图分析
├── intent-gpt5.md      # GPT-5意图分析
├── intent-merge-cc.md  # 意图合并
├── plan-cc.md          # Claude规划
├── plan-gpt5.md        # GPT-5规划
├── plan-merge-cc.md    # 计划合并
├── dev-cc.md           # 开发执行
├── eval-gpt5.md        # GPT-5评估
└── rollback-cc.md      # 回滚处理

scripts/
└── gpt5_bridge.py      # GPT-5集成脚本
```

## 🔧 安装方法

### 方法1: 统一安装脚本（推荐）

```bash
cd ClaudeAgents
bash install.sh
```

统一脚本会：
- ✅ 自动检测系统（Windows/WSL, Linux, macOS）
- ✅ 自动修复Windows换行符问题
- ✅ 智能寻找合适的Python版本
- ✅ 处理系统特定的pip安装
- ✅ 安装到正确的父目录
- ✅ 使用`>>`前缀避免与Claude Code内置功能冲突

### 方法2: 备用Python安装

如果bash不可用：

```bash
# 简化Python安装（跨平台）
cd ClaudeAgents
python setup_simple.py
```

## 安装后文件结构

```
项目目录/
├── .claude/
│   └── agents/           # Claude Code agent文件
├── scripts/              # 支持脚本
│   ├── gpt5_bridge.py
│   ├── pipeline_monitor.py
│   └── configure_api.py
└── .env                  # 环境变量配置
```

## 📊 监控Pipeline进度

### 内置代理状态显示
```
╔══════════════════════════════════════════════════════╗
║  🔍 INTENT ANALYSIS AGENT (CLAUDE) - ACTIVE         ║
║  Stage: 1/5 - Intent Understanding                   ║
╚══════════════════════════════════════════════════════╝
```

### Pipeline监控工具
```bash
# 启动实时监控
python scripts/pipeline_monitor.py

# 检查状态一次
python scripts/pipeline_monitor.py --once
```

## 📊 JSON Schema

系统使用结构化JSON进行代理通信：

### RouterDecision
```json
{"mode": "pipeline", "override_detected": true, "reasons": ["Complex development task"]}
```

### IntentDraft
```json
{
  "context": "Converting synchronous code to async",
  "primary_goals": ["Add async/await support", "Maintain API compatibility"],
  "code_touchpoints": [{"path": "auth.py", "reason": "Main authentication logic"}]
}
```

### PlanDraft
```json
{
  "milestones": [{"name": "Convert core functions", "deliverables": ["async auth methods"]}],
  "test_strategy": {"levels": ["unit", "integration"], "tools": ["pytest-asyncio"]},
  "test_cases": [{"id": "TC1", "given": "sync function", "when": "converted", "then": "async compatible"}]
}
```

## 🛠️ GPT-5集成

GPT-5已于2025年8月正式发布，完全支持API调用。包含GPT-5集成桥接脚本：

```bash
# 支持三种GPT-5模型规格
python scripts/gpt5_bridge.py --phase intent --input intent_cc.json --output intent_gpt5.json

# 模型选择：
# - gpt-5 (完整版): $1.25/1M input tokens, $10/1M output tokens  
# - gpt-5-mini (轻量版): $0.25/1M input tokens, $2/1M output tokens
# - gpt-5-nano (超轻量版): $0.05/1M input tokens, $0.40/1M output tokens
```

## 🧪 TDD焦点

所有开发遵循测试驱动开发：
- 实现前编写测试
- 全面测试覆盖率验证
- 真实测试执行和验证
- 自动化测试结果评估

## 🔍 故障排除

### 常见问题

**找不到代理**
- 确保代理在 `~/.claude/agents/` 或 `.claude/agents/` 中
- 检查文件权限和命名

**GPT-5集成不工作**
- 验证 `OPENAI_API_KEY` 设置正确
- 确保 `scripts/gpt5_bridge.py` 有执行权限

**Pipeline未触发**
- 尝试使用 `@pipeline` 前缀显式pipeline模式
- 检查任务复杂度是否满足pipeline标准

### 验证步骤

1. **检查代理安装**
   ```bash
   ls ~/.claude/agents/
   # 应显示: router.md, intent-cc.md, etc.
   ```

2. **测试Claude Code集成**
   ```bash
   claude-code --version
   # 验证Claude Code工作正常
   ```

3. **验证依赖**
   ```bash
   python -c "import openai; print('OpenAI package available')"
   ```

## 🔧 自定义

可通过编辑Markdown文件自定义每个子代理：

```markdown
---
name: custom-agent
description: Handles custom development tasks
tools: Read, Write, Edit, Bash
model: sonnet
---

Your custom agent prompt and instructions here...
```

## 🤝 贡献

这是一个使用Claude Code子代理系统创建复杂开发工作流的框架。欢迎扩展和自定义以满足您的特定需求。

## 📄 许可证

MIT