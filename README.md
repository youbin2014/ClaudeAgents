# Claude Agents Framework

A powerful multi-agent system powered by Claude for automated software development with TDD methodology.

## Overview

This framework implements a sophisticated pipeline that orchestrates multiple specialized Claude agents to handle complex development tasks. It features intent analysis, planning, development, and evaluation phases with automatic rollback capabilities.

## Key Features

- **Multi-Agent Architecture**: Specialized agents for different aspects of development
- **TDD Methodology**: Test-Driven Development approach with comprehensive test coverage
- **Dual LLM Integration**: Combines Claude and GPT-5 capabilities for enhanced results
- **Automatic Rollback**: Safe rollback mechanism when evaluation fails
- **Intelligent Routing**: Smart query routing based on complexity analysis

## System Architecture

```
User Query → Router → Intent Analysis → Planning → Development → Evaluation
                ↓                                                      ↓
            Quick Response                                      Rollback (if failed)
```

## Core Agents

### Intent Analysis
- **intent-cc**: Claude-based intent analysis
- **intent-gpt5**: GPT-5 enhanced intent analysis  
- **intent-merge-cc**: Merges insights from both LLMs

### Planning
- **plan-cc**: Claude-based TDD planning
- **plan-gpt5**: GPT-5 comprehensive planning
- **plan-merge-cc**: Combines planning strategies

### Development
- **dev-cc**: Main development execution agent
- **rollback-cc**: Handles safe rollback when needed

### Orchestration
- **orchestrator**: Coordinates the entire pipeline
- **router**: Routes queries based on complexity

## Quick Start

```python
from claude_agents import Orchestrator

# Initialize the orchestrator
orchestrator = Orchestrator()

# Process a development request
result = orchestrator.process("Implement a user authentication system")
```

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Configure your API keys in `.env`:

```
CLAUDE_API_KEY=your_claude_key
OPENAI_API_KEY=your_openai_key
```

## License

MIT