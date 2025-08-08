# Example Workflow: Async Module Conversion

This example demonstrates how the multi-agent pipeline handles a real-world task: converting a synchronous module to async with comprehensive testing.

## Initial Request

```
User: "#pipeline Convert the user authentication module to async and add comprehensive unit tests"
```

## Pipeline Execution Flow

### Stage 1: Routing (router)

**Input**: User query with #pipeline tag  
**Decision**:
```json
{
  "mode": "pipeline",
  "override_detected": true,
  "reasons": ["Manual override tag #pipeline detected"],
  "confidence": 1.0,
  "complexity_score": 0.75
}
```
**Result**: → Full pipeline mode activated

### Stage 2: Intent Analysis

#### 2a. Claude Analysis (intent-cc)
```json
{
  "context": "Converting synchronous authentication module to async implementation with testing",
  "primary_goals": [
    "Convert all sync functions to async",
    "Maintain backward compatibility",
    "Add comprehensive test coverage"
  ],
  "secondary_goals": [
    "Improve performance through async I/O",
    "Enable concurrent request handling"
  ],
  "code_touchpoints": [
    {
      "path": "auth/authentication.py",
      "reason": "Main module requiring async conversion",
      "risk_level": "high",
      "estimated_changes": 200
    },
    {
      "path": "auth/middleware.py",
      "reason": "Middleware must handle async functions",
      "risk_level": "medium",
      "estimated_changes": 100
    }
  ],
  "estimated_complexity": 7,
  "constraints": ["Zero downtime deployment", "API compatibility"],
  "assumptions": ["Async framework available", "Database supports async"]
}
```

#### 2b. GPT-5 Analysis (intent-gpt5)
```json
{
  "context": "Technical analysis reveals async conversion impacts session handling and database connections",
  "primary_goals": [
    "Async conversion of authentication functions",
    "Connection pool management for async DB",
    "Comprehensive async-aware testing"
  ],
  "code_touchpoints": [
    {
      "path": "auth/authentication.py",
      "reason": "Core functions need async/await",
      "risk_level": "high",
      "estimated_changes": 250,
      "dependencies": ["db/connection.py", "cache/redis.py"]
    },
    {
      "path": "tests/test_authentication.py",
      "reason": "Tests need async test runners",
      "risk_level": "low",
      "estimated_changes": 150
    }
  ],
  "gpt5_insights": {
    "performance_impact": "Expected 3x throughput improvement",
    "security_considerations": "Ensure async doesn't introduce race conditions in token generation",
    "edge_cases": ["Concurrent login attempts", "Connection pool exhaustion"]
  }
}
```

#### 2c. Merged Intent (intent-merge-cc)
```json
{
  "context": "Comprehensive async conversion with focus on authentication module, middleware, and testing",
  "primary_goals": [
    "Convert all authentication functions to async",
    "Implement async-aware connection pooling",
    "Add comprehensive async test coverage",
    "Maintain API compatibility"
  ],
  "code_touchpoints": [
    {
      "path": "auth/authentication.py",
      "risk_level": "high",
      "estimated_changes": 250
    },
    {
      "path": "auth/middleware.py",
      "risk_level": "medium",
      "estimated_changes": 100
    },
    {
      "path": "tests/test_authentication.py",
      "risk_level": "low",
      "estimated_changes": 150
    },
    {
      "path": "db/connection.py",
      "risk_level": "medium",
      "estimated_changes": 50
    }
  ],
  "estimated_complexity": 8,
  "requires_user_confirmation": true
}
```

**User Confirmation**: ✓ Proceed with plan

### Stage 3: Planning

#### 3a. Claude Planning (plan-cc)
```json
{
  "milestones": [
    {
      "name": "Setup async test infrastructure",
      "deliverables": ["pytest-asyncio setup", "async test fixtures"],
      "success_criteria": ["All test runners support async"]
    },
    {
      "name": "Convert core authentication",
      "deliverables": ["Async login/logout", "Async token validation"],
      "success_criteria": ["All auth functions are async", "Tests pass"]
    },
    {
      "name": "Update middleware",
      "deliverables": ["Async middleware handlers"],
      "success_criteria": ["Middleware handles async auth"]
    }
  ],
  "test_strategy": {
    "levels": ["unit", "integration", "performance"],
    "tools": ["pytest", "pytest-asyncio", "locust"],
    "coverage_target": 90
  },
  "test_cases": [
    {
      "id": "TC001",
      "name": "Async login success",
      "given": "Valid credentials",
      "when": "async login called",
      "then": "Returns token asynchronously"
    }
  ]
}
```

#### 3b. GPT-5 Enhancement (plan-gpt5)
```json
{
  "enhanced_test_cases": [
    {
      "id": "TC_GPT5_001",
      "name": "Concurrent login race condition",
      "given": "100 simultaneous login requests for same user",
      "when": "All requests hit login endpoint",
      "then": "Only one session created, others receive existing",
      "edge_case": true,
      "implementation_hint": "Use asyncio.gather() to simulate"
    },
    {
      "id": "TC_GPT5_002",
      "name": "Connection pool exhaustion",
      "given": "Max connections reached",
      "when": "New auth request arrives",
      "then": "Graceful queuing or rejection",
      "edge_case": true
    }
  ],
  "performance_considerations": [
    {
      "area": "Database connections",
      "solution": "Implement connection pooling with asyncpg",
      "impact": "10x concurrent request handling"
    }
  ]
}
```

#### 3c. Final Plan (plan-merge-cc)
Comprehensive plan combining:
- 3 development milestones
- 15 test cases (including edge cases)
- Performance benchmarks
- Rollback strategy

**User Confirmation**: ✓ Proceed with development

### Stage 4: Development (dev-cc)

**Execution**:
1. ✅ Set up pytest-asyncio
2. ✅ Write async tests first (TDD)
3. ✅ Convert authentication.py to async
4. ✅ Update middleware for async
5. ✅ Run all tests
6. ✅ Performance validation

**Result**:
```json
{
  "diff_unified": "... 350 lines changed ...",
  "files_modified": ["auth/authentication.py", "auth/middleware.py"],
  "files_created": ["tests/test_async_auth.py"],
  "tests_added": ["test_async_login", "test_concurrent_requests", "test_pool_exhaustion"],
  "test_run": {
    "passed": true,
    "total_tests": 15,
    "passed_tests": 15,
    "failed_tests": 0,
    "coverage": 92
  }
}
```

### Stage 5: Evaluation (eval-gpt5)

**GPT-5 Assessment**:
```json
{
  "verdict": "passed",
  "findings": [
    {
      "type": "performance",
      "severity": "low",
      "detail": "Consider caching decoded tokens",
      "suggestion": "Implement 60-second token cache"
    }
  ],
  "test_coverage_analysis": {
    "coverage_percentage": 92,
    "uncovered_critical_paths": [],
    "test_quality_score": 9.2
  },
  "code_quality_score": 8.7,
  "security_assessment": {
    "vulnerabilities_found": [],
    "risk_level": "low"
  },
  "suggestions": [
    "Add performance monitoring",
    "Consider rate limiting for auth endpoints"
  ],
  "confidence": 0.95
}
```

### Stage 6: Completion

**Final Summary**:
- ✅ All requirements met
- ✅ 92% test coverage achieved
- ✅ Performance improved (3x throughput)
- ✅ No security vulnerabilities
- ✅ Successfully deployed

## Key Learnings

1. **Multi-Agent Collaboration**: Claude provided context and structure, GPT-5 added technical depth
2. **TDD Success**: Writing tests first caught 3 edge cases early
3. **Performance Gains**: Async conversion yielded 3x throughput improvement
4. **Safety Net**: Rollback plan available but not needed

## Running This Example

```bash
# In Claude Code, simply paste:
"#pipeline Convert the user authentication module to async and add comprehensive unit tests"

# Or invoke the orchestrator directly:
@orchestrator execute pipeline for: "Convert auth module to async with tests"
```

## Customization

To adapt this workflow for your needs:

1. Modify agent prompts in `.claude/agents/`
2. Adjust test coverage targets in plan agents
3. Configure GPT-5 reasoning levels in bridge script
4. Add domain-specific validators in eval agent

---

This example demonstrates the full power of the multi-agent pipeline, showing how specialized agents work together to deliver high-quality, well-tested code transformations.