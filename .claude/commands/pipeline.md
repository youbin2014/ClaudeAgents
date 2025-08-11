# Pipeline Direct Execution

Multi-step pipeline orchestration for complex development tasks with full TDD workflow.

## Usage
```
/pipeline your complex task description
```

## What this command does
1. Analyzes your request using intent analysis (Claude + GPT-5)
2. Creates a comprehensive development plan with testing strategy
3. Implements the solution following TDD methodology
4. Evaluates and validates the results
5. Provides rollback capability if needed

## Pipeline Stages
- **Intent Analysis**: Understanding requirements and code touchpoints
- **Planning**: Creating detailed implementation plan with test cases
- **Development**: TDD-based implementation with continuous testing
- **Evaluation**: Comprehensive quality assessment
- **Rollback**: Safe reversion if evaluation fails

## Examples
- `/pipeline implement user authentication with JWT`
- `/pipeline optimize database performance for user queries`
- `/pipeline refactor legacy code to modern patterns`

## Technical Implementation
Uses the `pipeline-direct` agent which orchestrates multiple specialized agents:
- `intent-cc` and `intent-gpt5` for requirement analysis
- `plan-cc` and `plan-gpt5` for comprehensive planning
- `dev-cc` for TDD-based development
- `eval-gpt5` for quality evaluation
- `rollback-cc` for safe rollback when needed

Task: $ARGUMENTS