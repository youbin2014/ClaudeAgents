#!/usr/bin/env python3
"""
GPT-5 Bridge Script for Claude Code Subagents

This script acts as a bridge between Claude Code subagents and GPT-5 API.
It handles intent analysis, planning, and evaluation tasks using GPT-5's capabilities.

Usage:
    python gpt5_bridge.py --phase intent --input input.json --output output.json
    python gpt5_bridge.py --phase plan --input input.json --output output.json
    python gpt5_bridge.py --phase eval --input input.json --output output.json
"""

import json
import os
import sys
import argparse
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GPT5Bridge:
    """Bridge for GPT-5 integration with Claude Code subagents."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize GPT-5 client."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.client = AsyncOpenAI(api_key=self.api_key)
        # GPT-5 model variants
        self.models = {
            "full": "gpt-5",
            "mini": "gpt-5-mini",
            "nano": "gpt-5-nano"
        }
    
    async def analyze_intent(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze intent using GPT-5's code understanding capabilities."""
        query = data.get("query", "")
        context = data.get("context", {})
        
        prompt = f"""Analyze this development request with focus on code-level impact:

Request: {query}

Context: {json.dumps(context, indent=2) if context else "No additional context"}

Using your code analysis capabilities (74.9% SWE-bench performance), identify:
1. Primary technical objectives
2. Specific code touchpoints and why they'll be affected
3. Dependencies and integration points
4. Risk assessment for each touchpoint
5. Testing requirements
6. Performance implications

Provide a structured IntentDraft in JSON format:
{{
  "context": "Comprehensive understanding",
  "primary_goals": ["goal1", "goal2"],
  "secondary_goals": ["goal1"],
  "expected_outcomes": ["outcome1"],
  "code_touchpoints": [
    {{
      "path": "file/path",
      "reason": "why affected",
      "risk_level": "low|medium|high",
      "estimated_changes": number
    }}
  ],
  "estimated_complexity": 1-10,
  "constraints": ["constraint1"],
  "assumptions": ["assumption1"]
}}"""
        
        response = await self.client.chat.completions.create(
            model=self.models["full"],
            messages=[
                {"role": "system", "content": "You are GPT-5, excelling at code analysis with state-of-the-art performance."},
                {"role": "user", "content": prompt}
            ],
            reasoning="medium",  # GPT-5 specific parameter
            verbosity="detailed",  # GPT-5 specific parameter
            temperature=0.4,
            max_tokens=4000
        )
        
        # Parse the response
        content = response.choices[0].message.content
        
        # Try to extract JSON from the response
        try:
            # Find JSON block in the response
            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                result = json.loads(json_match.group())
            else:
                # Fallback: create structured response from text
                result = {
                    "context": content,
                    "primary_goals": ["Extracted from GPT-5 analysis"],
                    "secondary_goals": [],
                    "expected_outcomes": ["See context for details"],
                    "code_touchpoints": [],
                    "estimated_complexity": 5,
                    "constraints": [],
                    "assumptions": []
                }
        except json.JSONDecodeError:
            result = {
                "context": content,
                "primary_goals": ["Analysis provided in context"],
                "secondary_goals": [],
                "expected_outcomes": ["See context"],
                "code_touchpoints": [],
                "estimated_complexity": 5,
                "constraints": [],
                "assumptions": []
            }
        
        return {
            "intent_draft": result,
            "model": self.models["full"],
            "reasoning_level": "medium",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def enhance_plan(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance planning with GPT-5's testing expertise."""
        intent = data.get("intent", {})
        initial_plan = data.get("initial_plan", {})
        
        prompt = f"""Enhance this development plan with comprehensive test cases and edge case coverage:

Intent: {json.dumps(intent, indent=2)}

Initial Plan: {json.dumps(initial_plan, indent=2) if initial_plan else "No initial plan"}

Focus on:
1. Comprehensive test coverage including edge cases
2. Performance testing scenarios
3. Security vulnerability testing
4. Integration test requirements
5. Specific test implementation examples

Provide enhanced test cases and improvements in JSON format:
{{
  "enhanced_test_cases": [
    {{
      "id": "TC_ID",
      "name": "Test name",
      "given": "Initial state",
      "when": "Action",
      "then": "Expected result",
      "test_type": "unit|integration|e2e|performance",
      "priority": "critical|high|medium|low",
      "edge_case": true|false,
      "implementation_hint": "How to implement"
    }}
  ],
  "test_coverage_analysis": {{
    "covered_scenarios": ["scenario1"],
    "gaps_identified": ["gap1"],
    "recommended_additions": ["addition1"]
  }},
  "performance_considerations": ["consideration1"],
  "security_test_requirements": ["requirement1"]
}}"""
        
        response = await self.client.chat.completions.create(
            model=self.models["full"],
            messages=[
                {"role": "system", "content": "You are GPT-5, expert at test-driven development and comprehensive test planning."},
                {"role": "user", "content": prompt}
            ],
            reasoning="high",  # High reasoning for test planning
            verbosity="detailed",
            temperature=0.5,
            max_tokens=5000
        )
        
        content = response.choices[0].message.content
        
        # Parse response
        try:
            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = {"raw_analysis": content}
        except json.JSONDecodeError:
            result = {"raw_analysis": content}
        
        return {
            "plan_enhancements": result,
            "model": self.models["full"],
            "reasoning_level": "high",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def evaluate_development(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate development results using GPT-5."""
        dev_result = data.get("dev_result", {})
        plan = data.get("plan", {})
        intent = data.get("intent", {})
        
        prompt = f"""Evaluate the following development work comprehensively:

Original Intent: {json.dumps(intent, indent=2)}

Plan: {json.dumps(plan, indent=2)}

Development Result: {json.dumps(dev_result, indent=2)}

Provide a comprehensive evaluation covering:
1. Whether requirements are met
2. Code quality assessment
3. Test coverage adequacy
4. Security vulnerabilities
5. Performance implications
6. Potential issues or improvements
7. Overall verdict

Output in JSON format:
{{
  "verdict": "passed|needs_changes|failed",
  "findings": [
    {{
      "type": "test|code|performance|security|documentation",
      "severity": "critical|high|medium|low",
      "detail": "Description",
      "location": "Optional file/line",
      "suggestion": "How to fix"
    }}
  ],
  "test_coverage_analysis": {{
    "coverage_percentage": number,
    "uncovered_critical_paths": ["path1"],
    "test_quality_score": number
  }},
  "code_quality_score": 0.0-10.0,
  "security_assessment": {{
    "vulnerabilities_found": ["vuln1"],
    "risk_level": "low|medium|high"
  }},
  "performance_assessment": {{
    "potential_bottlenecks": ["bottleneck1"],
    "optimization_opportunities": ["opportunity1"]
  }},
  "suggestions": ["suggestion1"],
  "confidence": 0.0-1.0
}}"""
        
        response = await self.client.chat.completions.create(
            model=self.models["full"],
            messages=[
                {"role": "system", "content": "You are GPT-5, evaluating code with expertise achieving 88% on Aider Polyglot benchmark."},
                {"role": "user", "content": prompt}
            ],
            reasoning="high",  # High reasoning for evaluation
            verbosity="comprehensive",
            temperature=0.3,
            max_tokens=6000
        )
        
        content = response.choices[0].message.content
        
        # Parse response
        try:
            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = {
                    "verdict": "needs_changes",
                    "raw_evaluation": content,
                    "confidence": 0.7
                }
        except json.JSONDecodeError:
            result = {
                "verdict": "needs_changes",
                "raw_evaluation": content,
                "confidence": 0.7
            }
        
        return {
            "evaluation": result,
            "model": self.models["full"],
            "reasoning_level": "high",
            "timestamp": datetime.utcnow().isoformat()
        }

async def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="GPT-5 Bridge for Claude Code Subagents")
    parser.add_argument("--phase", required=True, choices=["intent", "plan", "eval"],
                       help="Processing phase")
    parser.add_argument("--input", required=True, help="Input JSON file path")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    parser.add_argument("--model", default="full", choices=["full", "mini", "nano"],
                       help="GPT-5 model variant")
    parser.add_argument("--api-key", help="OpenAI API key (optional, can use env var)")
    
    args = parser.parse_args()
    
    # Load input data
    try:
        with open(args.input, 'r') as f:
            input_data = json.load(f)
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Initialize bridge
    try:
        bridge = GPT5Bridge(api_key=args.api_key)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Process based on phase
    try:
        if args.phase == "intent":
            result = await bridge.analyze_intent(input_data)
        elif args.phase == "plan":
            result = await bridge.enhance_plan(input_data)
        elif args.phase == "eval":
            result = await bridge.evaluate_development(input_data)
        else:
            raise ValueError(f"Unknown phase: {args.phase}")
        
        # Write output
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"Successfully processed {args.phase} phase. Output written to {args.output}")
        
    except Exception as e:
        print(f"Error during processing: {e}", file=sys.stderr)
        # Write error output
        error_result = {
            "error": str(e),
            "phase": args.phase,
            "timestamp": datetime.utcnow().isoformat()
        }
        with open(args.output, 'w') as f:
            json.dump(error_result, f, indent=2)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())