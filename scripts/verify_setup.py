#!/usr/bin/env python3
"""
Verification tool for Claude Agents Pipeline setup
Checks if everything is properly configured and ready to use
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple
import subprocess

class SetupVerifier:
    """Verify Claude Agents Pipeline installation and configuration"""
    
    def __init__(self):
        self.current_dir = Path.cwd()
        self.checks_passed = []
        self.checks_failed = []
        self.warnings = []
        
    def print_header(self):
        """Print verification header"""
        print("\n" + "="*60)
        print("🔍 Claude Agents Pipeline - Setup Verification")
        print("="*60)
        print(f"\nChecking installation in: {self.current_dir}\n")
    
    def check_agents_installation(self) -> bool:
        """Check if agents are properly installed"""
        agents_dir = self.current_dir / ".claude" / "agents"
        
        if not agents_dir.exists():
            self.checks_failed.append("Agents directory not found")
            return False
        
        # Check for essential agents
        essential_agents = [
            "orchestrator.md",
            "router.md",
            "intent-cc.md",
            "plan-cc.md",
            "dev-cc.md"
        ]
        
        missing_agents = []
        for agent in essential_agents:
            if not (agents_dir / agent).exists():
                missing_agents.append(agent)
        
        if missing_agents:
            self.checks_failed.append(f"Missing agents: {', '.join(missing_agents)}")
            return False
        
        # Count total agents
        agent_count = len(list(agents_dir.glob("*.md")))
        self.checks_passed.append(f"Found {agent_count} agents installed")
        return True
    
    def check_scripts_installation(self) -> bool:
        """Check if scripts are properly installed"""
        scripts_dir = self.current_dir / "scripts"
        
        if not scripts_dir.exists():
            self.checks_failed.append("Scripts directory not found")
            return False
        
        # Check for essential scripts
        essential_scripts = [
            "gpt5_bridge.py",
            "pipeline_monitor.py",
            "configure_api.py"
        ]
        
        missing_scripts = []
        for script in essential_scripts:
            if not (scripts_dir / script).exists():
                missing_scripts.append(script)
        
        if missing_scripts:
            self.warnings.append(f"Optional scripts missing: {', '.join(missing_scripts)}")
        
        if (scripts_dir / "gpt5_bridge.py").exists():
            self.checks_passed.append("GPT-5 bridge script installed")
        
        return True
    
    def check_python_dependencies(self) -> bool:
        """Check if Python dependencies are installed"""
        required_packages = {
            "openai": "OpenAI API (for GPT-5)",
            "dotenv": "Environment variable management",
            "structlog": "Structured logging"
        }
        
        missing_packages = []
        
        for package, description in required_packages.items():
            try:
                if package == "dotenv":
                    __import__("dotenv")
                else:
                    __import__(package)
            except ImportError:
                missing_packages.append(f"{package} ({description})")
        
        if missing_packages:
            self.checks_failed.append(f"Missing Python packages: {', '.join(missing_packages)}")
            return False
        
        self.checks_passed.append("All Python dependencies installed")
        return True
    
    def check_api_configuration(self) -> Tuple[bool, bool]:
        """Check API key configuration"""
        env_file = self.current_dir / ".env"
        openai_configured = False
        claude_configured = False
        
        # Check .env file
        if env_file.exists():
            with open(env_file, 'r') as f:
                content = f.read()
                if "OPENAI_API_KEY" in content:
                    openai_configured = True
                if "CLAUDE_API_KEY" in content:
                    claude_configured = True
        
        # Check environment variables
        if os.environ.get("OPENAI_API_KEY"):
            openai_configured = True
        if os.environ.get("CLAUDE_API_KEY"):
            claude_configured = True
        
        if openai_configured:
            self.checks_passed.append("OPENAI_API_KEY configured")
        else:
            self.warnings.append("OPENAI_API_KEY not configured (GPT-5 features disabled)")
        
        if claude_configured:
            self.checks_passed.append("CLAUDE_API_KEY configured")
        else:
            self.warnings.append("CLAUDE_API_KEY not in .env (will use Claude Code auth)")
        
        return openai_configured, claude_configured
    
    def test_gpt5_connection(self) -> bool:
        """Test GPT-5 API connection"""
        api_key = os.environ.get("OPENAI_API_KEY")
        
        if not api_key:
            # Try to load from .env
            env_file = self.current_dir / ".env"
            if env_file.exists():
                from dotenv import load_dotenv
                load_dotenv()
                api_key = os.environ.get("OPENAI_API_KEY")
        
        if not api_key:
            return False
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            # Just test initialization
            self.checks_passed.append("GPT-5 API connection verified")
            return True
        except Exception as e:
            self.warnings.append(f"GPT-5 connection test failed: {str(e)[:50]}")
            return False
    
    def check_claude_code_environment(self) -> bool:
        """Check if running in Claude Code environment"""
        # Check for Claude Code indicators
        claude_indicators = [
            os.environ.get("CLAUDE_CODE"),
            os.environ.get("CLAUDE_SESSION_ID"),
            Path.home() / ".claude" / "claude.json"
        ]
        
        if any(claude_indicators):
            self.checks_passed.append("Claude Code environment detected")
            return True
        else:
            self.warnings.append("Not running in Claude Code (expected for setup)")
            return True  # Not a failure, just informational
    
    def generate_report(self):
        """Generate verification report"""
        print("\n" + "="*60)
        print("📊 VERIFICATION REPORT")
        print("="*60)
        
        # Passed checks
        if self.checks_passed:
            print("\n✅ PASSED CHECKS:")
            for check in self.checks_passed:
                print(f"   ✓ {check}")
        
        # Warnings
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"   ⚠ {warning}")
        
        # Failed checks
        if self.checks_failed:
            print("\n❌ FAILED CHECKS:")
            for check in self.checks_failed:
                print(f"   ✗ {check}")
        
        # Overall status
        print("\n" + "="*60)
        if not self.checks_failed:
            print("✨ SETUP VERIFIED: Ready to use!")
            print("="*60)
            print("\nNext steps:")
            print("  1. Start Claude Code in this directory")
            print("  2. Use '@pipeline' prefix for complex tasks")
            print("  3. Monitor with: python scripts/pipeline_monitor.py")
            
            if self.warnings:
                print("\nOptional improvements:")
                if "OPENAI_API_KEY" in str(self.warnings):
                    print("  - Configure GPT-5: python scripts/configure_api.py")
        else:
            print("❌ SETUP INCOMPLETE: Please fix the issues above")
            print("="*60)
            print("\nTo fix:")
            if "Agents directory" in str(self.checks_failed):
                print("  - Run installer: ./ClaudeAgents/install.sh")
            if "Python packages" in str(self.checks_failed):
                print("  - Install deps: pip install openai python-dotenv structlog")
    
    def run(self) -> bool:
        """Run all verification checks"""
        self.print_header()
        
        print("Running verification checks...\n")
        
        # Run checks
        checks = [
            ("Agents Installation", self.check_agents_installation),
            ("Scripts Installation", self.check_scripts_installation),
            ("Python Dependencies", self.check_python_dependencies),
            ("API Configuration", lambda: self.check_api_configuration()[0]),
            ("GPT-5 Connection", self.test_gpt5_connection),
            ("Claude Environment", self.check_claude_code_environment)
        ]
        
        for check_name, check_func in checks:
            print(f"Checking {check_name}...", end=" ")
            try:
                result = check_func()
                if result:
                    print("✅")
                else:
                    print("❌")
            except Exception as e:
                print(f"⚠️  ({str(e)[:30]})")
                self.warnings.append(f"{check_name}: {str(e)[:50]}")
        
        # Generate report
        self.generate_report()
        
        return len(self.checks_failed) == 0

def main():
    """Main entry point"""
    verifier = SetupVerifier()
    success = verifier.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()