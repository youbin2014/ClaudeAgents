#!/usr/bin/env python3
"""
Setup script for Claude Agents Pipeline
Alternative to bash install.sh for Python-based installation
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import argparse

class ClaudeAgentsSetup:
    """Setup Claude Agents in production environment"""
    
    def __init__(self, target_dir=None):
        self.source_dir = Path(__file__).parent
        self.target_dir = Path(target_dir) if target_dir else Path.cwd()
        self.agents_source = self.source_dir / ".claude" / "agents"
        self.agents_target = self.target_dir / ".claude" / "agents"
        self.scripts_source = self.source_dir / "scripts"
        self.scripts_target = self.target_dir / "scripts"
        
    def print_header(self):
        """Print installation header"""
        print("\n" + "="*60)
        print("🚀 Claude Agents Pipeline - Python Setup")
        print("="*60)
        print(f"\nSource: {self.source_dir}")
        print(f"Target: {self.target_dir}\n")
    
    def check_environment(self):
        """Check Python environment"""
        print("📦 Checking environment...")
        
        # Check Python version
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print(f"❌ Python {version.major}.{version.minor} detected")
            print("   Python 3.8+ is required")
            return False
        
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        
        # Check if in git repo (warning only)
        if not (self.target_dir / ".git").exists():
            print("⚠️  Not in a git repository (optional)")
        
        return True
    
    def install_agents(self):
        """Install agent files"""
        print("\n📂 Installing agents...")
        
        # Create target directory
        self.agents_target.mkdir(parents=True, exist_ok=True)
        
        # Copy agent files
        agent_count = 0
        if self.agents_source.exists():
            for agent_file in self.agents_source.glob("*.md"):
                shutil.copy2(agent_file, self.agents_target / agent_file.name)
                agent_count += 1
            
            print(f"✅ Installed {agent_count} agents to {self.agents_target}")
        else:
            print(f"❌ Agent source not found: {self.agents_source}")
            return False
        
        return True
    
    def install_scripts(self):
        """Install supporting scripts"""
        print("\n📜 Installing scripts...")
        
        # Create scripts directory
        self.scripts_target.mkdir(parents=True, exist_ok=True)
        
        # Essential scripts to copy
        essential_scripts = [
            "gpt5_bridge.py",
            "pipeline_monitor.py",
            "configure_api.py"
        ]
        
        copied = 0
        for script in essential_scripts:
            source_file = self.scripts_source / script
            if source_file.exists():
                shutil.copy2(source_file, self.scripts_target / script)
                copied += 1
                print(f"   ✅ {script}")
        
        print(f"✅ Installed {copied} scripts")
        return True
    
    def install_dependencies(self):
        """Install Python dependencies"""
        print("\n📦 Installing Python dependencies...")
        
        requirements_file = self.source_dir / "requirements.txt"
        
        if requirements_file.exists():
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-q", "-r", str(requirements_file)],
                    check=True
                )
                print("✅ Dependencies installed from requirements.txt")
            except subprocess.CalledProcessError as e:
                print(f"⚠️  Failed to install from requirements.txt: {e}")
                return self.install_minimal_dependencies()
        else:
            return self.install_minimal_dependencies()
        
        return True
    
    def install_minimal_dependencies(self):
        """Install minimal required dependencies"""
        print("Installing minimal dependencies...")
        
        packages = ["openai", "python-dotenv", "structlog"]
        
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-q"] + packages,
                check=True
            )
            print("✅ Minimal dependencies installed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    def configure_api_keys(self):
        """Configure API keys"""
        print("\n🔑 Configuring API keys...")
        
        # Import the configure_api module
        sys.path.insert(0, str(self.scripts_target))
        
        try:
            from configure_api import APIConfigurator
            
            configurator = APIConfigurator()
            configurator.interactive_setup()
            return True
            
        except ImportError:
            print("⚠️  Could not import API configurator")
            print("   Run: python scripts/configure_api.py")
            return False
    
    def create_quickstart(self):
        """Create quickstart script"""
        quickstart_content = """#!/usr/bin/env python3
'''Quick start for Claude Agents Pipeline'''

import os
import sys
from pathlib import Path

# Load environment variables
env_file = Path('.env')
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv()

print("🚀 Claude Agents Pipeline Ready!")
print()
print("Usage in Claude Code:")
print("  1. Start Claude Code in this directory")
print("  2. Use pipeline commands:")
print("     - 'Convert this to async' (auto-detect pipeline)")
print("     - '#pipeline Implement feature X' (explicit pipeline)")
print()
print("Monitor pipeline progress:")
print("  python scripts/pipeline_monitor.py")
print()

# Check configuration
if not os.getenv('OPENAI_API_KEY'):
    print("⚠️  OPENAI_API_KEY not set. Run: python scripts/configure_api.py")
"""
        
        quickstart_file = self.target_dir / "quickstart.py"
        quickstart_file.write_text(quickstart_content)
        quickstart_file.chmod(0o755)
        
        print(f"✅ Created quickstart script: {quickstart_file}")
    
    def verify_installation(self):
        """Verify the installation"""
        print("\n🔍 Verifying installation...")
        
        checks = {
            "Agents directory": self.agents_target.exists(),
            "Scripts directory": self.scripts_target.exists(),
            "GPT-5 bridge": (self.scripts_target / "gpt5_bridge.py").exists(),
            "API configurator": (self.scripts_target / "configure_api.py").exists(),
            "Environment file": (self.target_dir / ".env").exists()
        }
        
        all_passed = True
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check}")
            if not passed:
                all_passed = False
        
        return all_passed
    
    def run(self, skip_api_config=False):
        """Run the complete setup"""
        self.print_header()
        
        if not self.check_environment():
            return False
        
        if not self.install_agents():
            return False
        
        if not self.install_scripts():
            return False
        
        if not self.install_dependencies():
            return False
        
        if not skip_api_config:
            self.configure_api_keys()
        
        self.create_quickstart()
        
        if self.verify_installation():
            print("\n" + "="*60)
            print("✨ Installation completed successfully!")
            print("="*60)
            print("\nNext steps:")
            print("  1. Configure API keys: python scripts/configure_api.py")
            print("  2. Start Claude Code in this directory")
            print("  3. Use '#pipeline' for complex tasks")
            return True
        else:
            print("\n⚠️  Installation completed with warnings")
            return False

def main():
    parser = argparse.ArgumentParser(description="Setup Claude Agents Pipeline")
    parser.add_argument("--target", help="Target directory (default: current)")
    parser.add_argument("--skip-api", action="store_true", help="Skip API configuration")
    
    args = parser.parse_args()
    
    setup = ClaudeAgentsSetup(args.target)
    success = setup.run(skip_api_config=args.skip_api)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()