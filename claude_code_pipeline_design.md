# Claude Code Sub-Agent Pipeline Design

**Created on:** 2025-08-08
**Purpose:** Automate development tasks via a multi-agent Claude Code pipeline, with GPT-5 integration and rollback capability.

---

## 🔁 Overview

This pipeline supports both **quick queries** and **full development workflows** using Claude Code subagents. The system routes queries automatically via a `router` subagent, then proceeds through four main stages:

1. **Intent Understanding**
2. **Planning (TDD-first)**
3. **Development**
4. **Evaluation**
5. **Rollback (if required)**

---

## 📌 Subagents

### A0: `router` (Routing Agent)
- **Purpose:** Decides whether to use `quick` response or full `pipeline` based on user query or override tag.
- **Triggers:** Any new query.
- **Output:** `RouterDecision` JSON object.

### A1: `intent-cc`
- **Purpose:** Claude deeply analyzes the user intent, context, and related code.
- **Output:** `IntentDraft` JSON.

### A2: `intent-gpt5`
- **Purpose:** GPT-5 focuses on code-touchpoint analysis and complements Claude’s intent.
- **Tool:** `gpt5_cli` or manual bridging.

### A3: `intent-merge-cc`
- **Purpose:** Merges A1 and A2 results into final `IntentDraft`, asks user to confirm before moving to plan phase.

### B1: `plan-cc`
- **Purpose:** Claude generates a test-driven `PlanDraft`, including milestones, tasks, testing strategy, and test cases.

### B2: `plan-gpt5`
- **Purpose:** GPT-5 strengthens the plan with edge case test samples and boundary coverage.

### B3: `plan-merge-cc`
- **Purpose:** Merge B1 and B2 into the final plan. Confirm with user.

### C1: `dev-cc`
- **Purpose:** Execute the development plan by editing code and implementing tests. Ensure all tests pass.

### D1: `eval-gpt5`
- **Purpose:** GPT-5 evaluates the development result and test coverage. Produces verdict.

### E1: `rollback-cc`
- **Purpose:** On evaluation failure or user request, restore codebase using rollback plan.

---

## 🧩 Shared JSON Schema

Each stage uses a structured handoff format. See below for examples:

### `RouterDecision`
```json
{"mode": "pipeline", "override_detected": true, "reasons": ["User added #pipeline"]}
```

### `IntentDraft`
```json
{"context": "...", "primary_goals": ["..."], "secondary_goals": ["..."],
"expected_outcomes": ["..."], "code_touchpoints": [{"path": "...", "reason": "..."}]}
```

### `PlanDraft`
```json
{"milestones": [{"name": "...", "deliverables": ["..."]}],
"test_strategy": {"levels": ["unit", "integration"], "tools": ["pytest"]},
"test_cases": [{"id": "TC1", "given": "...", "when": "...", "then": "..."}]}
```

### `DevResult`
```json
{"diff_unified": "...", "tests_added": ["..."], "test_run": {"summary": "...", "passed": true}}
```

### `EvalReport`
```json
{"verdict": "needs_changes", "findings": [{"type": "test", "detail": "missing case"}]}
```

---

## 🛡️ Rollback Strategy

### E1: `rollback-cc`
- **Purpose:** Based on `DevResult`, restore changed files and test status.
- **Triggers:** Either EvalReport.verdict == `needs_changes` or user manually requests rollback.
- **Actions:** Revert to previous file states using version control or cached state.

---

## 🧠 GPT-5 Integration

Use a command-line tool `gpt5_cli` for interacting with GPT-5:
```bash
gpt5_cli --phase intent --input intent_cc.json --output intent_gpt5.json
```

Can be replaced with manual bridging if needed.

---

## 🧪 TDD Focus

The planning and development stages must follow **Test-Driven Development**:
- Write tests before feature implementation.
- Validate with real test runs.
- Use Claude to generate and execute test files.

---

## ✅ Example Workflow

1. User asks: “我希望将这个模块转换成异步版本，并写好单元测试。”
2. → `router` detects `pipeline` required.
3. → `intent-cc`, `intent-gpt5`, `intent-merge-cc` create final intent.
4. → `plan-cc`, `plan-gpt5`, `plan-merge-cc` define the TDD plan.
5. → `dev-cc` executes.
6. → `eval-gpt5` evaluates result.
7. If failed, → `rollback-cc` restores code.

---

## 🔚
This file is ready to be pasted into Claude Code as the design document for creating your sub-agent system.
