# 🤖 GPT-5 Direct Access Guide

## 概述

GPT-5 Direct模式允许您绕过标准pipeline，直接访问GPT-5 API以获得即时响应。这对于快速查询、代码分析和不需要完整开发流程的问题特别有用。

## 🚀 快速开始

### 基本用法

```bash
/gpt5 <your question or request>
```

### 示例

```bash
# 技术概念解释
/gpt5 Explain the difference between async/await and promises

# 代码分析
/gpt5 Review this function for performance issues: [paste code]

# 架构建议
/gpt5 Design a distributed caching system using Redis

# 算法设计
/gpt5 Implement a rate limiting algorithm with token bucket
```

## 📋 可用模型

### GPT-5（默认）
```bash
/gpt5 <query>
```
- 完整的GPT-5功能
- 最高准确度
- 适合复杂问题

### GPT-5 Mini
```bash
/gpt5-mini <query>
```
- 更快的响应时间
- 较低的成本
- 适合中等复杂度问题

### GPT-5 Nano
```bash
/gpt5-nano <query>
```
- 最快的响应时间
- 最低成本
- 适合简单查询

## 🎯 使用场景

### 适合使用GPT-5 Direct的场景

1. **快速技术咨询**
   - 概念解释
   - 最佳实践建议
   - 技术比较

2. **代码审查**
   - 性能分析
   - 安全漏洞检测
   - 代码质量评估

3. **问题解决**
   - 调试帮助
   - 错误分析
   - 解决方案建议

4. **学习和教育**
   - 技术教程
   - 概念澄清
   - 示例代码

### 不适合使用GPT-5 Direct的场景

1. **多文件项目实现**
   - 使用 `>>pipeline` 代替

2. **需要测试的功能开发**
   - 使用完整pipeline以包含TDD

3. **需要多步骤验证的任务**
   - 使用标准pipeline流程

## ⚙️ 配置

### API密钥设置

1. 编辑 `.env` 文件：
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

2. 或使用配置脚本：
```bash
python scripts/configure_api.py
```

## 🔄 工作原理

```mermaid
graph LR
    A[用户输入 /gpt5] --> B[路由器检测]
    B --> C[GPT-5 Direct Agent]
    C --> D[准备查询]
    D --> E[调用GPT-5 API]
    E --> F[格式化响应]
    F --> G[返回给用户]
```

### 执行流程

1. **命令检测**：路由器识别 `/gpt5` 前缀
2. **模式选择**：激活GPT-5 Direct模式
3. **查询准备**：提取用户查询，收集上下文
4. **API调用**：通过 `gpt5_bridge.py` 调用GPT-5
5. **响应处理**：格式化并返回结果

## 📊 与Pipeline模式对比

| 特性 | GPT-5 Direct | Pipeline模式 |
|------|-------------|------------|
| 响应时间 | 2-5秒 | 5-30分钟 |
| 适用场景 | 查询、分析 | 实现、开发 |
| 测试支持 | ❌ | ✅ |
| 多步骤处理 | ❌ | ✅ |
| 成本 | 低 | 高 |
| 复杂度处理 | 中等 | 高 |

## 🛠️ 高级功能

### 包含文件上下文

当您的查询涉及特定文件时，GPT-5 Direct会自动包含相关上下文：

```bash
/gpt5 How can I optimize the database queries in user_service.py?
# 系统会自动读取user_service.py并包含在查询中
```

### 代码块支持

您可以在查询中直接包含代码块：

```bash
/gpt5 Review this code for security issues:
```python
def authenticate(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    return db.execute(query)
```
```

### 多轮对话（未来功能）

即将支持的功能：
- 保持对话上下文
- 后续问题
- 澄清和深入

## ❗ 错误处理

### 常见错误及解决方案

1. **API密钥缺失**
```
❌ OpenAI API key not configured
解决方案：设置OPENAI_API_KEY环境变量
```

2. **速率限制**
```
⚠️ Rate limit reached
解决方案：等待60秒或使用/gpt5-mini
```

3. **网络错误**
```
❌ Failed to connect to GPT-5 API
解决方案：检查网络连接，稍后重试
```

## 💡 最佳实践

1. **明确具体**：提供清晰、具体的问题
2. **包含上下文**：相关时包含代码或错误消息
3. **选择正确的模型**：根据复杂度选择合适的模型变体
4. **使用适当的模式**：简单查询用Direct，复杂实现用Pipeline

## 📈 性能指标

- **平均响应时间**：2-5秒
- **成功率**：>95%
- **令牌使用**：每次查询1000-4000令牌
- **并发支持**：是

## 🔗 相关资源

- [主README](README.md)
- [Pipeline模式指南](README.md#pipeline阶段)
- [API配置](scripts/configure_api.py)
- [GPT-5 Bridge源码](scripts/gpt5_bridge.py)

## 📝 更新日志

### v1.0.0 (2025-08-08)
- 初始发布GPT-5 Direct模式
- 支持三种模型变体（full, mini, nano）
- 自动上下文包含
- 错误处理和重试逻辑

---

💡 **提示**：GPT-5 Direct模式是对现有pipeline系统的补充，而不是替代。根据您的具体需求选择最合适的模式。