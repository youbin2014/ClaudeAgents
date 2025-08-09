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
        # Default to parent directory (project root) instead of current directory
        self.target_dir = Path(target_dir) if target_dir else (Path.cwd().parent if Path.cwd().name == "ClaudeAgents" else Path.cwd())
        self.agents_source = self.source_dir / ".claude" / "agents"
        self.agents_target = self.target_dir / ".claude" / "agents"
        self.scripts_source = self.source_dir / "scripts"
        self.scripts_target = self.target_dir / "scripts"
    
    def safe_print(self, text, fallback=None):
        """Print text with Unicode fallback"""
        try:
            print(text)
        except UnicodeEncodeError:
            if fallback:
                print(fallback)
            else:
                # Remove emojis and special characters
                clean_text = text.replace("🚀", "").replace("📦", "").replace("✅", "OK:").replace("❌", "ERROR:").replace("⚠️", "WARNING:")
                print(clean_text.strip())
        
    def print_header(self):
        """Print installation header"""
        print("\n" + "="*60)
        self.safe_print("🚀 Claude Agents Pipeline - Python Setup")
        print("="*60)
        print(f"\nSource: {self.source_dir}")
        print(f"Target: {self.target_dir}\n")
    
    def check_environment(self):
        """Check Python environment"""
        try:
            print("📦 Checking environment...")
        except UnicodeEncodeError:
            print("Checking environment...")
        
        # Check Python version
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            try:
                print(f"❌ Python {version.major}.{version.minor} detected")
            except UnicodeEncodeError:
                print(f"ERROR: Python {version.major}.{version.minor} detected")
            print("   Python 3.8+ is required")
            return False
        
        try:
            print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        except UnicodeEncodeError:
            print(f"OK: Python {version.major}.{version.minor}.{version.micro}")
        
        # Check if in git repo (warning only)
        if not (self.target_dir / ".git").exists():
            try:
                print("⚠️  Not in a git repository (optional)")
            except UnicodeEncodeError:
                print("WARNING: Not in a git repository (optional)")
        
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
            print(f"⚠️  Agent source not found: {self.agents_source}")
            print("   Creating basic agent files...")
            # Create basic agent files if source doesn't exist
            basic_agents = {
                "pipeline.md": "# Pipeline Agent\nCore pipeline orchestration agent",
                "async_converter.md": "# Async Converter\nConvert sync code to async",
                "code_analyzer.md": "# Code Analyzer\nAnalyze and improve code quality"
            }
            
            for filename, content in basic_agents.items():
                agent_file = self.agents_target / filename
                agent_file.write_text(content)
                agent_count += 1
            
            print(f"✅ Created {agent_count} basic agents")
        
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
            target_file = self.scripts_target / script
            
            if source_file.exists():
                # Skip if source and target are the same file
                if source_file.resolve() != target_file.resolve():
                    try:
                        shutil.copy2(source_file, target_file)
                        copied += 1
                        self.safe_print(f"   ✅ {script}")
                    except (PermissionError, OSError) as e:
                        print(f"   ⚠️  Could not copy {script}: {e}")
                else:
                    self.safe_print(f"   ✅ {script} (already in place)")
        
        self.safe_print(f"✅ Processed {len(essential_scripts)} scripts")
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
            # Check if configure_api.py exists
            if (self.scripts_target / "configure_api.py").exists():
                from configure_api import APIConfigurator
                configurator = APIConfigurator()
                configurator.interactive_setup()
                return True
            else:
                print("⚠️  API configurator script not found")
                print("   Creating basic .env file...")
                self.create_basic_env()
                return True
            
        except ImportError as e:
            print(f"⚠️  Could not import API configurator: {e}")
            print("   Creating basic .env file...")
            self.create_basic_env()
            return True
    
    def create_basic_env(self):
        """Create a basic .env file template"""
        env_content = """# Claude Agents Pipeline Configuration
# Add your API keys here

# OpenAI API Key for GPT-5 integration
# OPENAI_API_KEY=your_openai_api_key_here

# Claude API Key (optional, Claude Code handles this)
# CLAUDE_API_KEY=your_claude_api_key_here
"""
        env_file = self.target_dir / ".env"
        if not env_file.exists():
            env_file.write_text(env_content)
            print(f"✅ Created .env template at {env_file}")
            print("   Please add your API keys manually")
        else:
            print("✅ .env file already exists")
    
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
print("     - '@pipeline Implement feature X' (explicit pipeline)")
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
            print("  3. Use '@pipeline' for complex tasks")
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