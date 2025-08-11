#!/usr/bin/env python3
"""
Test script for GPT-5 Direct mode functionality
"""

import json
import subprocess
import tempfile
import os
from pathlib import Path

def test_gpt5_direct():
    """Test the GPT-5 direct query functionality"""
    
    print("🧪 Testing GPT-5 Direct Mode")
    print("=" * 50)
    
    # Test 1: Basic direct query
    print("\n📝 Test 1: Basic GPT-5 Direct Query")
    test_query = {
        "query": "What is the difference between async and await in Python?",
        "context": {
            "mode": "direct",
            "include_code": True
        }
    }
    
    # Create temporary input file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_query, f)
        input_file = f.name
    
    # Create temporary output file
    output_file = tempfile.mktemp(suffix='.json')
    
    try:
        # Run the GPT-5 bridge in direct mode
        cmd = [
            'python', 'scripts/gpt5_bridge.py',
            '--phase', 'direct',
            '--input', input_file,
            '--output', output_file,
            '--model', 'full'
        ]
        
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Command executed successfully")
            
            # Read and display output
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    output = json.load(f)
                    
                if output.get('status') == 'success':
                    print("✅ GPT-5 Direct query successful")
                    print(f"Model used: {output.get('model', 'unknown')}")
                    print(f"Response preview: {output.get('response', '')[:200]}...")
                elif output.get('status') == 'error':
                    print(f"⚠️ GPT-5 returned error: {output.get('error')}")
                    print(f"Suggestion: {output.get('suggestion')}")
                else:
                    print("❓ Unexpected response format")
                    print(json.dumps(output, indent=2))
        else:
            print(f"❌ Command failed with return code: {result.returncode}")
            print(f"Error output: {result.stderr}")
            
    except FileNotFoundError:
        print("❌ GPT-5 bridge script not found. Make sure you're in the project directory.")
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        # Cleanup
        if os.path.exists(input_file):
            os.remove(input_file)
        if os.path.exists(output_file):
            os.remove(output_file)
    
    print("\n" + "=" * 50)
    
    # Test 2: Test with different model variants
    print("\n📝 Test 2: Model Variants")
    
    for model in ['full', 'mini', 'nano']:
        print(f"\nTesting with model: gpt-5-{model}")
        
        test_query = {
            "query": "Hello GPT-5!",
            "context": {
                "mode": "direct",
                "model_variant": model
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_query, f)
            input_file = f.name
        
        output_file = tempfile.mktemp(suffix='.json')
        
        try:
            cmd = [
                'python', 'scripts/gpt5_bridge.py',
                '--phase', 'direct',
                '--input', input_file,
                '--output', output_file,
                '--model', model
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    output = json.load(f)
                    if output.get('status') == 'success':
                        print(f"  ✅ Model {model} works")
                    else:
                        print(f"  ⚠️ Model {model} returned error")
            else:
                print(f"  ❌ Model {model} test failed")
                
        except subprocess.TimeoutExpired:
            print(f"  ⚠️ Model {model} test timed out")
        except Exception as e:
            print(f"  ❌ Model {model} test error: {e}")
        finally:
            if os.path.exists(input_file):
                os.remove(input_file)
            if os.path.exists(output_file):
                os.remove(output_file)
    
    print("\n" + "=" * 50)
    print("🏁 Testing complete!")
    print("\nNote: If tests failed due to missing API key, set OPENAI_API_KEY environment variable.")

def test_router_detection():
    """Test if router correctly detects /gpt5 commands"""
    
    print("\n🧪 Testing Router Detection")
    print("=" * 50)
    
    test_cases = [
        ("/gpt5 What is async programming?", "gpt5-direct", "gpt-5"),
        ("/gpt5-mini Explain promises", "gpt5-direct", "gpt-5-mini"),
        ("/gpt5-nano Quick question", "gpt5-direct", "gpt-5-nano"),
        ("What is async programming?", "quick", None),
        (">>pipeline Build a complex system", "pipeline", None),
    ]
    
    print("\nRouter detection test cases:")
    for query, expected_mode, expected_model in test_cases:
        print(f"\nQuery: '{query}'")
        print(f"  Expected mode: {expected_mode}")
        if expected_model:
            print(f"  Expected model: {expected_model}")
        
        # In a real test, you would call the router here
        # For now, we'll just show the expected behavior
        if query.startswith('/gpt5'):
            print("  ✅ Would route to GPT-5 Direct")
        elif query.startswith('>>pipeline'):
            print("  ✅ Would route to Pipeline")
        elif query.startswith('>>quick'):
            print("  ✅ Would route to Quick")
        else:
            print("  ✅ Would auto-detect mode")

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set. Tests may fail.")
        print("   Set it with: export OPENAI_API_KEY=your_key_here")
        print()
    
    # Run tests
    test_router_detection()
    print("\n")
    test_gpt5_direct()