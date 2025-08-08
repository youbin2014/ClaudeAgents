# Claude Code Multi-Agent Development Pipeline

A sophisticated multi-agent system for Claude Code that automates development workflows using a pipeline of specialized subagents, with optional GPT-5 integration for enhanced capabilities.

## 🚀 Overview

This system implements a complete development pipeline using Claude Code's subagent feature, orchestrating multiple specialized agents to handle different aspects of software development:

- **Intelligent Routing**: Automatically determines whether queries need quick responses or full pipeline processing
- **Multi-Model Integration**: Combines Claude's contextual understanding with GPT-5's technical depth
- **Test-Driven Development**: Enforces TDD methodology throughout the development process
- **Safe Rollback**: Complete rollback capability with lesson learning
- **Quality Assurance**: Built-in evaluation and quality gates

## 📁 Project Structure

```
ClaudeAgents/
├── .claude/
│   └── agents/                    # Claude Code subagent definitions
│       ├── router.md              # Routes queries to quick/pipeline mode
│       ├── intent-cc.md           # Claude intent analysis
│       ├── intent-gpt5.md         # GPT-5 intent analysis
│       ├── intent-merge-cc.md     # Merges intent analyses
│       ├── plan-cc.md             # Claude planning
│       ├── plan-gpt5.md           # GPT-5 planning enhancement
│       ├── plan-merge-cc.md       # Merges planning
│       ├── dev-cc.md              # Development execution
│       ├── eval-gpt5.md           # GPT-5 evaluation
│       ├── rollback-cc.md         # Rollback management
│       └── orchestrator.md        # Main pipeline coordinator
├── scripts/
│   └── gpt5_bridge.py            # GPT-5 API integration script
├── examples/                      # Example workflows
├── claude_code_pipeline_design.md # Original design document
└── README.md                      # This file
```

## 🎯 Pipeline Stages

### 1. **Routing Stage** (`router`)
Analyzes queries to determine execution mode:
- **Quick Mode**: Simple questions, documentation, explanations
- **Pipeline Mode**: Implementation, refactoring, complex development tasks

### 2. **Intent Understanding** (`intent-cc`, `intent-gpt5`, `intent-merge-cc`)
Deep analysis of user requirements:
- Primary and secondary goals identification
- Code touchpoint analysis
- Risk assessment
- Complexity estimation

### 3. **Planning Stage** (`plan-cc`, `plan-gpt5`, `plan-merge-cc`)
Comprehensive TDD planning:
- Milestone definition
- Test case generation
- Implementation sequencing
- Rollback strategy

### 4. **Development Stage** (`dev-cc`)
Actual implementation following TDD:
- Test-first implementation
- Code generation
- Quality checks
- Performance validation

### 5. **Evaluation Stage** (`eval-gpt5`)
Comprehensive assessment:
- Requirement verification
- Test coverage analysis
- Security assessment
- Performance evaluation

### 6. **Rollback Stage** (`rollback-cc`)
Safe reversion when needed:
- State restoration
- Lesson capture
- Knowledge preservation

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ClaudeAgents.git
cd ClaudeAgents
```

### 2. Install Python Dependencies (for GPT-5 integration)
```bash
pip install openai python-dotenv
```

### 3. Set Up API Keys
Create a `.env` file:
```bash
OPENAI_API_KEY=your_gpt5_api_key_here
```

### 4. Verify Installation
The subagents should automatically appear in Claude Code. Test with:
```bash
# In Claude Code, type:
/agents
```

## 📖 Usage

### Basic Usage

#### Quick Query
```bash
# In Claude Code
"What is the difference between async and sync functions?"
# Router will automatically route to quick mode
```

#### Pipeline Mode
```bash
# In Claude Code
"#pipeline Convert the authentication module to use JWT tokens with comprehensive tests"
# Forces full pipeline execution
```

### Manual Agent Invocation

You can invoke specific agents directly:

```bash
# Use the router to analyze a query
@router analyze whether this needs full pipeline: "implement user registration"

# Run intent analysis
@intent-cc analyze the requirements for: "add caching to the API"

# Trigger development
@dev-cc implement the planned features from the current plan
```

### GPT-5 Integration

The system can work with or without GPT-5:

#### With GPT-5 (Enhanced Mode)
- Set `OPENAI_API_KEY` in `.env`
- GPT-5 agents will automatically activate
- Provides deeper technical analysis and comprehensive test coverage

#### Without GPT-5 (Claude-Only Mode)
- System automatically falls back to Claude-only workflow
- All features remain available with Claude's capabilities
- No external API requirements

### Using the GPT-5 Bridge Manually

```bash
# Analyze intent with GPT-5
python scripts/gpt5_bridge.py --phase intent \
  --input intent_request.json \
  --output intent_response.json

# Enhance planning with GPT-5
python scripts/gpt5_bridge.py --phase plan \
  --input plan_request.json \
  --output plan_response.json

# Evaluate with GPT-5
python scripts/gpt5_bridge.py --phase eval \
  --input eval_request.json \
  --output eval_response.json
```

## 🎮 Example Workflows

### Example 1: Simple Module Conversion
```bash
# In Claude Code
"Convert the user module to async and add comprehensive tests"

# Pipeline flow:
1. Router → pipeline mode
2. Intent-cc + Intent-gpt5 → Understand requirements
3. Plan-cc + Plan-gpt5 → Create TDD plan
4. Dev-cc → Implement with tests
5. Eval-gpt5 → Evaluate results
```

### Example 2: Quick Documentation
```bash
# In Claude Code
"Explain how JWT authentication works"

# Pipeline flow:
1. Router → quick mode
2. Direct response (no full pipeline needed)
```

### Example 3: Complex Refactoring
```bash
# In Claude Code
"#pipeline Refactor the entire API layer to use dependency injection with full test coverage"

# Pipeline flow:
1. Router → pipeline mode (forced)
2. Full pipeline execution with all agents
3. Comprehensive testing and evaluation
4. Rollback available if needed
```

## 🔍 Subagent Details

### Core Agents

| Agent | Purpose | Tools | Model |
|-------|---------|-------|-------|
| router | Query routing | Read, Grep, Glob | Claude |
| intent-cc | Intent analysis | Read, Grep, Glob, TodoWrite | Claude |
| intent-gpt5 | Technical analysis | Bash, Read, Write | GPT-5 |
| plan-cc | TDD planning | Read, Write, Bash, Grep, Glob, TodoWrite | Claude |
| plan-gpt5 | Test enhancement | Bash, Read, Write | GPT-5 |
| dev-cc | Implementation | Read, Write, Edit, MultiEdit, Bash, Grep, Glob, TodoWrite | Claude |
| eval-gpt5 | Evaluation | Read, Bash, Grep, Glob | GPT-5 |
| rollback-cc | Rollback | Read, Write, Edit, Bash, Grep, Glob, TodoWrite | Claude |
| orchestrator | Coordination | Read, Write, TodoWrite, Bash, Grep, Glob | Claude |

### Agent Communication

Agents communicate through structured JSON formats:

- **RouterDecision**: Routing decisions with confidence scores
- **IntentDraft**: Comprehensive understanding of requirements
- **PlanDraft**: TDD plans with milestones and test cases
- **DevResult**: Development outcomes with test results
- **EvalReport**: Evaluation verdicts with findings
- **RollbackPlan**: Restoration strategies

## 🛠️ Configuration

### Customizing Agents

Edit agent files in `.claude/agents/` to:
- Modify agent behavior
- Add new capabilities
- Adjust tool permissions
- Change decision criteria

### Tool Permissions

Each agent has specific tool access defined in its YAML frontmatter:
```yaml
---
name: agent-name
description: Agent purpose
tools: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
---
```

## 🚦 Quality Gates

The pipeline includes multiple quality checkpoints:

1. **Intent Confirmation**: User approves understanding
2. **Plan Approval**: User reviews plan before implementation
3. **Test Validation**: All tests must pass
4. **Evaluation Gate**: GPT-5 assessment must pass
5. **Rollback Option**: Available at any failure point

## 🔒 Security Considerations

- API keys stored in `.env` (never commit)
- Agents have minimal required permissions
- Rollback capability for safety
- Security testing included in evaluation

## 📊 Performance

- **Quick Mode**: <5 seconds response time
- **Pipeline Mode**: 30 seconds to 5 minutes depending on complexity
- **Parallel Processing**: Where possible (intent analysis, planning)
- **Caching**: Results cached to avoid redundant API calls

## 🐛 Troubleshooting

### Common Issues

1. **Agents not appearing in Claude Code**
   - Ensure files are in `.claude/agents/` directory
   - Check YAML frontmatter syntax
   - Restart Claude Code

2. **GPT-5 integration failing**
   - Verify `OPENAI_API_KEY` is set
   - Check network connectivity
   - System automatically falls back to Claude-only

3. **Pipeline stuck**
   - Use `@orchestrator status` to check state
   - Manually invoke next agent if needed
   - Use rollback if necessary

## 🤝 Contributing

Contributions are welcome! To add new agents or enhance existing ones:

1. Create new agent file in `.claude/agents/`
2. Follow the existing agent format
3. Test the agent workflow
4. Submit PR with description

## 📜 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Built for Claude Code's subagent system
- Leverages GPT-5's advanced capabilities
- Inspired by modern DevOps pipelines
- TDD methodology from software engineering best practices

## 📮 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing agents for examples
- Refer to Claude Code documentation

---

**Created**: 2025-08-08  
**Version**: 1.0.0  
**Status**: Production Ready