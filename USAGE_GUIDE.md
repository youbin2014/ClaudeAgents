# Claude Code Subagent System 使用指南

## 🚀 系统概述

这个项目提供了一个基于Claude Code subagent的完整开发流水线，可以自动处理从需求分析到代码实现的完整开发流程。

## 📋 前置条件

### 1. 确保Claude Code已安装
```bash
# 检查Claude Code版本
claude --version

# 应该显示版本 >= 1.0.64
```

### 2. 配置API密钥
```bash
# 创建 .env 文件
echo "OPENAI_API_KEY=your_openai_key_here" > .env

# 或者设置环境变量
export OPENAI_API_KEY="your_openai_key_here"
```

### 3. 安装Python依赖
```bash
pip install -r requirements.txt
```

## 🔧 集成到Claude Code

### 方法1：项目级别集成
```bash
# 在项目根目录下，subagent文件已经在 .claude/agents/ 目录中
# Claude Code会自动检测并加载这些subagent
ls .claude/agents/
# 应该看到: router.md, intent-cc.md, plan-cc.md, dev-cc.md 等文件
```

### 方法2：全局集成（可选）
```bash
# 复制到全局Claude Code配置目录
cp -r .claude/agents/* ~/.claude/agents/
```

## 🎯 使用方式

### 1. 启动Claude Code会话
```bash
# 在项目目录下启动Claude Code
claude

# 或者指定项目路径
claude /path/to/your/project
```

### 2. 使用Subagent系统

#### 方式A: 自动检测模式
直接描述你的开发需求，系统会自动判断是否需要使用完整流水线：

```
# 简单问题 - 会使用快速响应
"这个Python函数有什么语法错误？"

# 复杂任务 - 自动触发完整流水线  
"实现一个用户认证系统，包括JWT token支持和完整的单元测试"
```

#### 方式B: 显式触发模式
使用标签强制指定模式：

```
# 强制使用完整流水线
"#pipeline 将这个同步模块转换为异步版本，并添加全面的测试覆盖"

# 强制使用快速模式
"#quick 解释一下这段代码的作用"
```

#### 方式C: 直接调用特定subagent
```
# 直接使用特定agent
"Use the router to analyze this development request"
"Use the intent-cc to understand my requirements"
"Use the dev-cc to implement this feature"
```

## 🔄 完整工作流程示例

### 示例1: 异步转换任务

**输入:**
```
"我想将这个用户管理模块转换为异步版本，确保所有数据库操作都是异步的，并添加完整的单元测试"
```

**系统执行流程:**

1. **Router分析** → 检测到复杂实现任务，启动流水线模式

2. **Intent分析** → `intent-cc` 和 `intent-gpt5` 并行分析
   - Claude分析: 理解业务需求和代码结构
   - GPT-5分析: 专注代码影响点和技术细节
   - `intent-merge-cc`: 合并分析结果

3. **计划阶段** → `plan-cc` 和 `plan-gpt5` 并行规划
   - Claude计划: TDD方法论和实现步骤  
   - GPT-5计划: 边界测试和测试用例设计
   - `plan-merge-cc`: 合并为最终计划

4. **开发执行** → `dev-cc` 按计划实现
   - 先写测试用例
   - 实现异步功能
   - 确保所有测试通过

5. **评估验证** → `eval-gpt5` 全面评估
   - 代码质量检查
   - 测试覆盖率分析
   - 性能和安全评估

6. **回滚(如需要)** → `rollback-cc` 安全回滚

### 示例2: 简单查询

**输入:**
```
"Python中async函数的语法是什么？"
```

**系统执行:**
- Router直接判断为简单查询 → 快速响应模式
- 直接提供语法说明，无需完整流水线

## 🛠️ 高级配置

### 自定义Subagent

编辑 `.claude/agents/` 目录下的Markdown文件来自定义agent行为：

```markdown
---
name: custom-agent
description: 自定义agent的描述
tools: Read, Write, Edit, Bash  # 指定可用工具
model: sonnet                   # 指定使用的模型
---

你的自定义agent提示词和指令...
```

### GPT-5集成测试

```bash
# 测试GPT-5桥接脚本
echo '{"query": "test request"}' > test_input.json
python scripts/gpt5_bridge.py --phase intent --input test_input.json --output test_output.json
cat test_output.json
```

### 调试模式

在Claude Code中启用详细日志：
```bash
# 设置调试级别
export CLAUDE_LOG_LEVEL=DEBUG

# 启动Claude Code
claude --verbose
```

## 📊 JSON通信格式

系统使用结构化JSON在各agent间通信：

### RouterDecision
```json
{
  "mode": "pipeline",
  "override_detected": false,
  "confidence": 0.9,
  "reasons": ["Complex implementation", "Testing required"]
}
```

### IntentDraft
```json
{
  "context": "Converting user management to async",
  "primary_goals": ["Add async/await support", "Maintain API compatibility"],
  "code_touchpoints": [
    {
      "path": "user_manager.py", 
      "reason": "Main sync functions",
      "risk_level": "medium"
    }
  ],
  "estimated_complexity": 7
}
```

## 🔍 故障排除

### 常见问题

1. **Subagent不被识别**
   ```bash
   # 检查agent文件格式
   ls -la .claude/agents/
   # 确保YAML frontmatter格式正确
   ```

2. **GPT-5集成失败**
   ```bash
   # 检查API密钥
   echo $OPENAI_API_KEY
   # 测试连接
   python -c "from openai import OpenAI; print('API key works')"
   ```

3. **Agent工具访问问题**
   ```bash
   # 检查tools配置
   head -10 .claude/agents/router.md
   ```

### 日志查看

Claude Code的日志通常位于：
- macOS: `~/Library/Logs/Claude Code/`
- Linux: `~/.local/share/claude-code/logs/`
- Windows: `%APPDATA%/Claude Code/logs/`

## 🎯 最佳实践

1. **明确描述需求**: 越具体的描述，系统分析越准确
2. **合理使用标签**: 复杂任务用 `#pipeline`，简单问题用 `#quick`
3. **迭代优化**: 根据结果调整agent配置和提示词
4. **测试驱动**: 让系统专注于TDD方法论
5. **监控性能**: 关注token使用和响应时间

## 📈 进阶用法

### 批处理模式
```bash
# 处理多个开发任务
for task in task1.txt task2.txt task3.txt; do
    claude --input "$task" --output "result_$(basename $task .txt).json"
done
```

### 团队协作
- 共享 `.claude/agents/` 配置
- 统一GPT-5集成配置  
- 建立代码review流程

### CI/CD集成
```yaml
# .github/workflows/claude-review.yml
name: Claude Code Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Claude Code Review
        run: |
          claude "#pipeline Review this PR for code quality and test coverage"
```

## 📚 更多资源

- [Claude Code官方文档](https://docs.anthropic.com/claude-code)
- [Subagent深入指南](https://docs.anthropic.com/claude-code/sub-agents)
- [项目设计文档](./claude_code_pipeline_design.md)
- [异步转换示例](./examples/async_conversion_workflow.md)

---

## 💡 小贴士

- 系统会学习你的使用模式，越用越智能
- 可以随时用 `#quick` 或 `#pipeline` 覆盖自动判断
- GPT-5集成是可选的，没有API密钥也能正常工作
- 定期更新subagent配置以适应项目需求变化

开始使用这个强大的AI驱动开发流水线，让Claude Code帮你自动化整个开发过程！🚀