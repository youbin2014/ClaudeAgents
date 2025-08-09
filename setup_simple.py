#!/usr/bin/env python3
"""
Simple Setup script for Claude Agents Pipeline
Safe version without Unicode characters
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def main():
    print("\n" + "="*60)
    print("Claude Agents Pipeline - Simple Setup")
    print("="*60)
    
    # Determine target directory - parent if running from ClaudeAgents
    if Path.cwd().name == "ClaudeAgents":
        target_dir = Path("..")
        print(f"Installing from: {Path.cwd()}")
        print(f"Installing to: {target_dir.resolve()}")
    else:
        target_dir = Path(".")
        print(f"Installing to: {target_dir.resolve()}")
    
    # Check Python version
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"ERROR: Python {version.major}.{version.minor} detected")
        print("Python 3.8+ is required")
        return False
    
    print(f"OK: Python {version.major}.{version.minor}.{version.micro}")
    
    # Create directories
    claude_dir = target_dir / ".claude" / "agents"
    scripts_dir = target_dir / "scripts"
    
    claude_dir.mkdir(parents=True, exist_ok=True)
    scripts_dir.mkdir(parents=True, exist_ok=True)
    
    print("OK: Directories created")
    
    # Create basic agent files
    agents = {
        "pipeline.md": "# Pipeline Agent\nCore pipeline orchestration agent",
        "async_converter.md": "# Async Converter\nConvert sync code to async",
        "code_analyzer.md": "# Code Analyzer\nAnalyze and improve code quality"
    }
    
    for filename, content in agents.items():
        (claude_dir / filename).write_text(content, encoding='utf-8')
    
    print(f"OK: Created {len(agents)} agent files")
    
    # Copy scripts if they exist
    source_scripts = Path(__file__).parent / "scripts"
    if source_scripts.exists():
        for script in ["gpt5_bridge.py", "pipeline_monitor.py", "configure_api.py"]:
            src = source_scripts / script
            dst = scripts_dir / script
            
            if src.exists():
                # Skip if source and destination are the same file
                if src.resolve() != dst.resolve():
                    try:
                        shutil.copy2(src, dst)
                        print(f"OK: Copied {script}")
                    except (PermissionError, OSError) as e:
                        print(f"WARNING: Could not copy {script}: {e}")
                else:
                    print(f"OK: {script} already in place")
            else:
                print(f"WARNING: {script} not found in source")
    
    # Install dependencies
    print("Installing dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "openai", "python-dotenv", "structlog"
        ], check=True, capture_output=True)
        print("OK: Dependencies installed")
    except subprocess.CalledProcessError:
        print("WARNING: Failed to install some dependencies")
    
    # Create .env template
    env_content = """# Claude Agents Pipeline Configuration
# OPENAI_API_KEY=your_key_here
"""
    env_file = target_dir / ".env"
    if not env_file.exists():
        env_file.write_text(env_content)
        print("OK: Created .env template")
    else:
        print("OK: .env file already exists")
    
    print("\n" + "="*60)
    print("Installation completed!")
    print("="*60)
    print("\nNext steps:")
    print("1. Add your OPENAI_API_KEY to .env file")
    print("2. Start Claude Code in this directory")
    print("3. Use '@pipeline' for complex tasks")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)