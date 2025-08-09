# Claude Code Subagent Pipeline

A sophisticated multi-agent development workflow system built on **Claude Code Sub-Agents** using Markdown-based agent definitions.

## Overview

This system implements a comprehensive development pipeline using Claude Code's subagent architecture. It orchestrates multiple specialized AI agents to handle complex development tasks through intent analysis, TDD planning, development execution, and evaluation phases with automatic rollback capabilities.

## 🚀 Key Features

- **Markdown-Based Subagents**: Agents defined in `.md` files with YAML frontmatter
- **Intelligent Routing**: Automatic query routing between quick responses and full pipeline
- **TDD Methodology**: Test-Driven Development with comprehensive coverage
- **Dual LLM Integration**: Combines Claude and GPT-5 capabilities
- **Automatic Rollback**: Safe recovery when evaluation fails
- **Structured Handoffs**: JSON schema for agent communication

## 🔧 Installation & Setup

### For New Environments

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/ClaudeAgents.git
   cd ClaudeAgents
   ```

2. **Set up Claude Code Subagents**
   Choose one of the following methods:

   **Option A: Global Installation (Recommended)**
   ```bash
   # Copy agents to your global Claude Code directory
   mkdir -p ~/.claude/agents
   cp -r .claude/agents/* ~/.claude/agents/
   ```

   **Option B: Project-Level Installation**
   ```bash
   # Keep agents in your project directory
   # Claude Code will automatically detect .claude/agents/ in your project
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Keys**
   ```bash
   # Required for Claude Code
   export CLAUDE_API_KEY=your_claude_key
   
   # Optional: For GPT-5 integration (enhanced planning and evaluation)
   export OPENAI_API_KEY=your_openai_key
   ```

5. **Verify Installation**
   ```bash
   # Start Claude Code in your project directory
   claude-code
   
   # Test the pipeline with a simple query
   "Convert this function to async"
   ```

### Integration with Existing Claude Code Setup

If you already have Claude Code configured:

1. **Backup Existing Agents** (if any)
   ```bash
   cp -r ~/.claude/agents ~/.claude/agents.backup
   ```

2. **Install ClaudeAgents**
   ```bash
   git clone https://github.com/your-username/ClaudeAgents.git
   cd ClaudeAgents
   cp -r .claude/agents/* ~/.claude/agents/
   ```

3. **Install Additional Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🏗️ Architecture

```
User Query → Router → Intent Analysis → Planning → Development → Evaluation
                ↓                                                      ↓
            Quick Response                                      Rollback (if failed)
```

## 🤖 Subagent Pipeline

### Stage 0: Routing
- **`router`**: Decides between quick response or full pipeline mode

### Stage 1: Intent Understanding
- **`intent-cc`**: Claude analyzes user intent and code context
- **`intent-gpt5`**: GPT-5 focuses on code touchpoints and technical details
- **`intent-merge-cc`**: Merges insights into comprehensive intent analysis

### Stage 2: Planning (TDD-First)
- **`plan-cc`**: Claude generates test-driven development plan
- **`plan-gpt5`**: GPT-5 enhances with edge cases and boundary testing
- **`plan-merge-cc`**: Creates final comprehensive development plan

### Stage 3: Development
- **`dev-cc`**: Executes development following TDD methodology

### Stage 4: Evaluation
- **`eval-gpt5`**: GPT-5 evaluates results and test coverage

### Stage 5: Rollback (If Needed)
- **`rollback-cc`**: Safely reverts changes when evaluation fails

## 📁 Project Structure

```
.claude/agents/          # Claude Code subagent definitions
├── router.md           # Query routing logic
├── intent-cc.md        # Claude intent analysis
├── intent-gpt5.md      # GPT-5 intent analysis
├── intent-merge-cc.md  # Intent merging
├── plan-cc.md          # Claude planning
├── plan-gpt5.md        # GPT-5 planning
├── plan-merge-cc.md    # Plan merging
├── dev-cc.md           # Development execution
├── eval-gpt5.md        # GPT-5 evaluation
└── rollback-cc.md      # Rollback handling

scripts/
└── gpt5_bridge.py      # GPT-5 integration script

examples/
└── async_conversion_workflow.md  # Example workflow
```

## 🚀 Usage

Start a Claude Code session and trigger the pipeline:

```bash
# Automatic pipeline detection
"Convert this module to async and add comprehensive tests"

# Explicit pipeline mode  
"#pipeline Convert this authentication system to use JWT tokens"
```

The system automatically detects complex development tasks and routes them through the appropriate pipeline stages.

## 📊 JSON Schema

The system uses structured JSON for agent communication:

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

## 🛠️ GPT-5 Integration

The system includes a bridge script for GPT-5 integration:

```bash
python scripts/gpt5_bridge.py --phase intent --input intent_cc.json --output intent_gpt5.json
```

## 🧪 TDD Focus

All development follows Test-Driven Development:
- Tests written before implementation
- Comprehensive test coverage validation
- Real test execution and verification
- Automated test result evaluation

## 📖 Example Workflow

See `examples/async_conversion_workflow.md` for a complete example of converting a synchronous module to async with comprehensive testing.

## 🔧 Customization

Each subagent can be customized by editing its Markdown file:

```markdown
---
name: custom-agent
description: Handles custom development tasks
tools: Read, Write, Edit, Bash
model: sonnet
---

Your custom agent prompt and instructions here...
```

## 🔍 Troubleshooting

### Common Issues

**Agents not found**
- Ensure agents are in `~/.claude/agents/` or `.claude/agents/` 
- Check file permissions and naming

**GPT-5 integration not working**
- Verify `OPENAI_API_KEY` is set correctly
- Ensure `scripts/gpt5_bridge.py` has execute permissions

**Pipeline not triggering**
- Try explicit pipeline mode with `#pipeline` prefix
- Check that task complexity meets pipeline criteria

### Verification Steps

1. **Check Agent Installation**
   ```bash
   ls ~/.claude/agents/
   # Should show: router.md, intent-cc.md, etc.
   ```

2. **Test Claude Code Integration**
   ```bash
   claude-code --version
   # Verify Claude Code is working
   ```

3. **Validate Dependencies**
   ```bash
   python -c "import openai; print('OpenAI package available')"
   ```

## 📚 Documentation

- `claude_code_pipeline_design.md`: Detailed system design
- `examples/`: Workflow examples and patterns
- `docs/`: Additional documentation

## 🤝 Contributing

This is a framework for creating sophisticated development workflows using Claude Code's subagent system. Feel free to extend and customize for your specific needs.

## 📄 License

MIT