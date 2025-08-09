# Claude Agents Pipeline 安装指南

## 🎯 统一安装解决方案

**重大更新**：
1. **解决Memory冲突** - 改用 `@pipeline` 替代 `#pipeline` 避免与Claude Code Memory功能冲突
2. **统一安装脚本** - 一个脚本支持所有系统（Windows/WSL, Linux, macOS）
3. **智能系统检测** - 自动检测操作系统、Python环境和终端支持
4. **完美兼容性** - 解决所有换行符、编码和依赖问题

## 🚀 一键安装（推荐）

```bash
cd ClaudeAgents
bash install.sh
```

这个统一脚本会：
- ✅ 自动检测你的系统（Windows/WSL, Linux, macOS）
- ✅ 自动修复Windows换行符问题
- ✅ 智能寻找合适的Python版本
- ✅ 处理系统特定的pip安装
- ✅ 安装到正确的父目录
- ✅ 创建系统适配的启动脚本

## 🔧 备用安装方法

如果bash不可用，使用Python脚本：

```bash
# 简化Python安装（跨平台）
cd ClaudeAgents
python setup_simple.py

# 标准Python安装
cd ClaudeAgents  
python setup.py
```

## 安装后的文件结构

安装成功后，您的项目目录会有：

```
项目目录/
├── .claude/
│   └── agents/           # Claude Code agent文件
│       ├── pipeline.md
│       ├── async_converter.md
│       └── code_analyzer.md (等)
├── scripts/              # 支持脚本
│   ├── gpt5_bridge.py
│   ├── pipeline_monitor.py
│   └── configure_api.py
├── .env                  # 环境变量配置
└── quickstart.py         # 快速启动脚本 (仅setup.py创建)
```

## 配置API密钥

1. 编辑 `.env` 文件：
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

2. 或使用配置脚本：
```bash
python scripts/configure_api.py
```

## 🎮 使用方法

### 新的触发方式（重要变更）

**不再使用 `#pipeline`** - 避免与Claude Code Memory冲突

**新的触发方式**：
- `@pipeline` - 强制使用复杂任务pipeline模式
- `@quick` - 强制使用快速响应模式  
- 自动检测 - 不加前缀时系统自动判断

### 使用示例

```bash
# 复杂任务 - 明确指定pipeline
@pipeline Convert this authentication system to async with comprehensive tests

# 快速查询 - 明确指定快速模式
@quick What is the syntax for async functions?

# 自动检测 - 系统根据复杂度判断
Convert this function to use modern async patterns
```

### 启动流程

1. 在Kaggle目录中启动Claude Code
2. 使用新的 `@pipeline` 或 `@quick` 前缀
3. 享受无冲突的pipeline体验

## 验证安装

运行以下命令检查安装状态：
```bash
python scripts/configure_api.py --check
```

## 故障排除

- 如果遇到Unicode编码错误，使用 `setup_simple.py`
- 如果权限错误，确保有写入权限
- 如果依赖安装失败，手动运行 `pip install openai python-dotenv structlog`

## 更新

要更新到最新版本，重新运行安装脚本即可。现有配置会被保留。