# 🚀 Claude Agents Pipeline - Quick Start

## 🎯 重要变更

**解决Memory冲突**：现在使用 `@pipeline` 而不是 `#pipeline` 以避免与Claude Code Memory功能冲突。

## ⚡ 一键安装

```bash
cd ClaudeAgents
bash install.sh
```

## 🎮 使用方法

### 新的触发方式
- `@pipeline` - 复杂任务，多步骤处理
- `@quick` - 快速响应，简单查询
- 无前缀 - 自动智能检测

### 示例
```bash
@pipeline Convert this auth system to async with tests
@quick What's the async syntax in Python?
Convert this function to modern patterns  # 自动检测
```

## 📁 安装结果

安装到 `Kaggle/` 目录：
- `.claude/agents/` - 14个智能代理
- `scripts/` - 支持脚本
- `.env` - 配置文件

## 🔧 配置

1. 编辑 `Kaggle/.env` 添加API密钥：
```bash
OPENAI_API_KEY=your_key_here
```

2. 在Kaggle目录启动Claude Code

3. 开始使用 `@pipeline` 前缀！

## ✨ 功能特性

- 🎯 **智能路由** - 自动选择最佳执行模式
- 🔄 **异步转换** - 专业的同步→异步代码转换
- 🏗️ **多步骤管道** - 复杂任务的结构化处理
- 🚀 **跨平台** - Windows/WSL, Linux, macOS全支持
- 🛡️ **无冲突** - 完全兼容Claude Code Memory系统

---
**需要帮助？** 查看 `INSTALL_GUIDE.md` 获取详细信息