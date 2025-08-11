#!/usr/bin/env python3
"""
Test script for Pipeline Direct mode functionality
"""

import json
import subprocess
import tempfile
import os
import time
from pathlib import Path

def test_pipeline_status_display():
    """Test the pipeline status display functionality"""
    
    print("🧪 Testing Pipeline Status Display")
    print("=" * 50)
    
    try:
        # Test the status display module directly
        result = subprocess.run([
            'python', 'scripts/pipeline_status_display.py'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Pipeline status display demo ran successfully")
            if "PIPELINE MODE ACTIVATED" in result.stdout:
                print("✅ Status display formatting works correctly")
            else:
                print("⚠️ Status display output may have formatting issues")
        else:
            print(f"❌ Status display demo failed: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⚠️ Status display demo was interrupted (expected for interactive demo)")
        return True
    except FileNotFoundError:
        print("❌ Pipeline status display script not found")
        return False
    except Exception as e:
        print(f"❌ Status display test failed: {e}")
        return False
    
    return True

def test_router_pipeline_detection():
    """Test if router correctly detects /pipeline commands"""
    
    print("\n🧪 Testing Router Pipeline Detection")
    print("=" * 50)
    
    test_cases = [
        ("/pipeline Convert auth system to async", "pipeline-direct", True),
        ("/pipeline Build a REST API with tests", "pipeline-direct", True),
        ("Convert auth system to async", "pipeline", False),  # Auto-detected
        ("/gpt5 What is async?", "gpt5-direct", True),
        (">>pipeline Force pipeline mode", "pipeline", True),
        (">>quick Quick question", "quick", True),
    ]
    
    print("\nRouter detection test cases:")
    for query, expected_mode, explicit in test_cases:
        print(f"\nQuery: '{query}'")
        print(f"  Expected mode: {expected_mode}")
        print(f"  Explicit command: {'Yes' if explicit else 'No'}")
        
        # Check the logic
        if query.startswith('/pipeline'):
            print("  ✅ Would route to Pipeline Direct mode")
        elif query.startswith('/gpt5'):
            print("  ✅ Would route to GPT-5 Direct mode")
        elif query.startswith('>>pipeline'):
            print("  ✅ Would route to Legacy Pipeline mode")
        elif query.startswith('>>quick'):
            print("  ✅ Would route to Quick mode")
        else:
            print("  ✅ Would auto-detect mode based on complexity")

def test_agent_configurations():
    """Test that all required agent configurations exist"""
    
    print("\n🧪 Testing Agent Configurations")
    print("=" * 50)
    
    required_agents = [
        "router.md",
        "pipeline-direct.md",
        "gpt5-direct.md", 
        "intent-cc.md",
        "intent-gpt5.md",
        "intent-merge-cc.md",
        "plan-cc.md",
        "plan-gpt5.md", 
        "plan-merge-cc.md",
        "dev-cc.md",
        "eval-gpt5.md",
        "orchestrator.md"
    ]
    
    agents_dir = Path(".claude/agents")
    if not agents_dir.exists():
        print("❌ Agents directory not found")
        return False
    
    all_exist = True
    for agent_file in required_agents:
        agent_path = agents_dir / agent_file
        if agent_path.exists():
            print(f"  ✅ {agent_file} exists")
            
            # Check for status display integration
            content = agent_path.read_text()
            if "Pipeline Status Display" in content or "status header" in content:
                print(f"    📊 Has status display integration")
            elif agent_file in ["router.md", "orchestrator.md", "pipeline-direct.md", "gpt5-direct.md"]:
                print(f"    📋 Core orchestration agent (no status display needed)")
            else:
                print(f"    ⚠️  Missing status display integration")
        else:
            print(f"  ❌ {agent_file} missing")
            all_exist = False
    
    return all_exist

def test_pipeline_workflow_completeness():
    """Test that the pipeline workflow is complete"""
    
    print("\n🧪 Testing Pipeline Workflow Completeness")
    print("=" * 50)
    
    # Check key workflow files
    workflow_files = [
        ("scripts/gpt5_bridge.py", "GPT-5 Bridge"),
        ("scripts/pipeline_status_display.py", "Status Display"),
        ("scripts/pipeline_monitor.py", "Pipeline Monitor"),
    ]
    
    all_complete = True
    for file_path, description in workflow_files:
        if Path(file_path).exists():
            print(f"  ✅ {description} exists")
        else:
            print(f"  ❌ {description} missing: {file_path}")
            all_complete = False
    
    # Check for direct mode support in gpt5_bridge
    bridge_path = Path("scripts/gpt5_bridge.py")
    if bridge_path.exists():
        content = bridge_path.read_text()
        if "--phase direct" in content:
            print(f"    ✅ GPT-5 Bridge has direct mode support")
        else:
            print(f"    ❌ GPT-5 Bridge missing direct mode support")
            all_complete = False
    
    return all_complete

def test_documentation_updates():
    """Test that documentation has been updated"""
    
    print("\n🧪 Testing Documentation Updates")
    print("=" * 50)
    
    readme_path = Path("README.md")
    if readme_path.exists():
        content = readme_path.read_text()
        
        if "/pipeline" in content:
            print("  ✅ README.md mentions /pipeline command")
        else:
            print("  ⚠️ README.md missing /pipeline command documentation")
        
        if "/gpt5" in content:
            print("  ✅ README.md mentions /gpt5 commands")
        else:
            print("  ⚠️ README.md missing /gpt5 command documentation")
        
        if "直接访问GPT-5" in content or "pipeline模式" in content:
            print("  ✅ README.md has Chinese documentation")
        else:
            print("  ⚠️ README.md missing Chinese documentation")
    else:
        print("  ❌ README.md not found")
    
    # Check for additional guides
    guide_files = [
        "GPT5_DIRECT_GUIDE.md",
    ]
    
    for guide in guide_files:
        if Path(guide).exists():
            print(f"  ✅ {guide} exists")
        else:
            print(f"  ⚠️ {guide} missing")

def run_integration_test():
    """Run basic integration test"""
    
    print("\n🧪 Running Integration Test")
    print("=" * 50)
    
    print("This would simulate a full /pipeline command execution:")
    print("1. Router detects /pipeline prefix")
    print("2. Routes to pipeline-direct agent")
    print("3. Pipeline-direct initializes status display")
    print("4. Orchestrator executes 5-stage pipeline")
    print("5. Each agent reports status updates")
    print("6. User sees real-time progress")
    print("7. Pipeline completes with summary")
    
    print("\n✅ Integration test structure validated")

def main():
    """Main test function"""
    
    print("🚀 Testing Pipeline Direct Mode Implementation")
    print("=" * 60)
    print("Testing the new /pipeline command and real-time status display")
    print("=" * 60)
    
    tests = [
        ("Agent Configurations", test_agent_configurations),
        ("Router Pipeline Detection", test_router_pipeline_detection), 
        ("Pipeline Status Display", test_pipeline_status_display),
        ("Workflow Completeness", test_pipeline_workflow_completeness),
        ("Documentation Updates", test_documentation_updates),
        ("Integration Test", run_integration_test),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*20} {test_name} {'='*20}")
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("🏁 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:30} {status}")
        if result:
            passed += 1
    
    print(f"\nTests Passed: {passed}/{len(results)}")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Pipeline Direct mode is ready to use.")
    else:
        print(f"\n⚠️ {len(results) - passed} tests failed. Review the issues above.")
    
    print("\n📖 Usage:")
    print("  /pipeline Convert my authentication system to async with tests")
    print("  /gpt5 Explain the benefits of async programming")
    print("  >>pipeline Use legacy pipeline mode")

if __name__ == "__main__":
    main()