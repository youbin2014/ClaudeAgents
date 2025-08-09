#!/bin/bash

# Claude Agents Pipeline - One-Click Installation Script
# This script sets up the Claude Agents system in a production environment

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CLAUDE_AGENTS_DIR=".claude/agents"
SCRIPTS_DIR="scripts"
CONFIG_FILE=".env"

# Print colored message
print_message() {
    echo -e "${2}${1}${NC}"
}

# Print header
print_header() {
    echo ""
    echo "════════════════════════════════════════════════════════════"
    echo "  🚀 Claude Agents Pipeline - Installation Script"
    echo "════════════════════════════════════════════════════════════"
    echo ""
}

# Check if running in a git repository
check_git_repo() {
    if [ ! -d ".git" ]; then
        print_message "⚠️  Warning: Not in a git repository. This script is designed to run in your project's root directory." "$YELLOW"
        read -p "Continue anyway? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Check Python installation
check_python() {
    print_message "📦 Checking Python installation..." "$BLUE"
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_message "❌ Python is not installed. Please install Python 3.8 or higher." "$RED"
        exit 1
    fi
    
    # Check Python version
    PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_message "✅ Python $PYTHON_VERSION found" "$GREEN"
}

# Install Claude Agents
install_agents() {
    print_message "📂 Installing Claude Code agents..." "$BLUE"
    
    # Create .claude directory if it doesn't exist
    mkdir -p "$CLAUDE_AGENTS_DIR"
    
    # Get the directory where this script is located
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
    
    # Copy agents from ClaudeAgents repo
    if [ -d "$SCRIPT_DIR/.claude/agents" ]; then
        cp -r "$SCRIPT_DIR/.claude/agents/"* "$CLAUDE_AGENTS_DIR/" 2>/dev/null || true
        print_message "✅ Agents installed to $CLAUDE_AGENTS_DIR" "$GREEN"
    else
        print_message "⚠️  Agents directory not found in $SCRIPT_DIR" "$YELLOW"
        print_message "   Make sure you're running this from the ClaudeAgents directory" "$YELLOW"
    fi
    
    # Copy scripts
    if [ ! -d "$SCRIPTS_DIR" ]; then
        mkdir -p "$SCRIPTS_DIR"
    fi
    
    # Copy only necessary scripts
    for script in gpt5_bridge.py pipeline_monitor.py; do
        if [ -f "$SCRIPT_DIR/scripts/$script" ]; then
            cp "$SCRIPT_DIR/scripts/$script" "$SCRIPTS_DIR/"
            print_message "✅ Copied $script to $SCRIPTS_DIR" "$GREEN"
        fi
    done
}

# Install Python dependencies
install_dependencies() {
    print_message "📦 Installing Python dependencies..." "$BLUE"
    
    # Check if requirements.txt exists in ClaudeAgents directory
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
    
    if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
        $PYTHON_CMD -m pip install -q -r "$SCRIPT_DIR/requirements.txt"
        print_message "✅ Python dependencies installed" "$GREEN"
    else
        # Install essential packages
        print_message "Installing essential packages..." "$BLUE"
        $PYTHON_CMD -m pip install -q openai python-dotenv structlog
        print_message "✅ Essential packages installed" "$GREEN"
    fi
}

# Configure API keys
configure_api_keys() {
    print_message "🔑 Configuring API keys..." "$BLUE"
    
    # Check for existing .env file
    if [ -f "$CONFIG_FILE" ]; then
        print_message "Found existing .env file" "$GREEN"
        source "$CONFIG_FILE"
    fi
    
    # Check for CLAUDE_API_KEY
    if [ -z "$CLAUDE_API_KEY" ]; then
        print_message "⚠️  CLAUDE_API_KEY not found in environment" "$YELLOW"
        print_message "   Please set it in your Claude Code configuration" "$YELLOW"
    else
        print_message "✅ CLAUDE_API_KEY found" "$GREEN"
    fi
    
    # Check for OPENAI_API_KEY (GPT-5)
    if [ -z "$OPENAI_API_KEY" ]; then
        print_message "" "$NC"
        print_message "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "$YELLOW"
        print_message "⚠️  GPT-5 API Key Required" "$YELLOW"
        print_message "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "$YELLOW"
        print_message "" "$NC"
        print_message "The pipeline uses GPT-5 for enhanced planning and evaluation." "$NC"
        print_message "Please enter your OpenAI API key (it will be saved to .env):" "$NC"
        print_message "" "$NC"
        
        read -s -p "OpenAI API Key: " OPENAI_KEY
        echo
        
        if [ ! -z "$OPENAI_KEY" ]; then
            # Add to .env file
            if grep -q "OPENAI_API_KEY" "$CONFIG_FILE" 2>/dev/null; then
                # Update existing key
                if [[ "$OSTYPE" == "darwin"* ]]; then
                    sed -i '' "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$OPENAI_KEY/" "$CONFIG_FILE"
                else
                    sed -i "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$OPENAI_KEY/" "$CONFIG_FILE"
                fi
            else
                # Add new key
                echo "OPENAI_API_KEY=$OPENAI_KEY" >> "$CONFIG_FILE"
            fi
            
            # Export for current session
            export OPENAI_API_KEY=$OPENAI_KEY
            
            print_message "✅ OpenAI API key configured" "$GREEN"
        else
            print_message "⚠️  No API key provided. GPT-5 features will be disabled." "$YELLOW"
            print_message "   You can add it later to the .env file." "$YELLOW"
        fi
    else
        print_message "✅ OPENAI_API_KEY found" "$GREEN"
    fi
}

# Verify installation
verify_installation() {
    print_message "🔍 Verifying installation..." "$BLUE"
    
    # Check agents
    if [ -d "$CLAUDE_AGENTS_DIR" ] && [ "$(ls -A $CLAUDE_AGENTS_DIR)" ]; then
        AGENT_COUNT=$(ls -1 $CLAUDE_AGENTS_DIR/*.md 2>/dev/null | wc -l)
        print_message "✅ Found $AGENT_COUNT agents installed" "$GREEN"
    else
        print_message "❌ Agents not properly installed" "$RED"
        return 1
    fi
    
    # Check GPT-5 bridge
    if [ -f "$SCRIPTS_DIR/gpt5_bridge.py" ]; then
        print_message "✅ GPT-5 bridge script installed" "$GREEN"
    else
        print_message "⚠️  GPT-5 bridge not found (optional)" "$YELLOW"
    fi
    
    # Test GPT-5 connection if API key exists
    if [ ! -z "$OPENAI_API_KEY" ]; then
        print_message "Testing GPT-5 connection..." "$BLUE"
        $PYTHON_CMD -c "
import os
import sys
try:
    from openai import OpenAI
    client = OpenAI(api_key='$OPENAI_API_KEY')
    # Just check if the client initializes (don't make actual API call)
    print('✅ GPT-5 connection configured')
except Exception as e:
    print(f'⚠️  GPT-5 connection test failed: {e}')
    sys.exit(1)
" || print_message "⚠️  GPT-5 connection could not be verified" "$YELLOW"
    fi
    
    return 0
}

# Create quick start script
create_quickstart() {
    cat > "claude-agents-start.sh" << 'EOF'
#!/bin/bash
# Quick start script for Claude Agents Pipeline

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

echo "🚀 Claude Agents Pipeline Ready!"
echo ""
echo "Usage in Claude Code:"
echo "  1. Start Claude Code in this directory"
echo "  2. Use pipeline commands:"
echo "     - 'Convert this to async' (auto-detect pipeline)"
echo "     - '#pipeline Implement feature X' (explicit pipeline)"
echo ""
echo "Monitor pipeline progress:"
echo "  python scripts/pipeline_monitor.py"
echo ""

# Optional: Start Claude Code if installed
if command -v claude-code &> /dev/null; then
    read -p "Start Claude Code now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        claude-code
    fi
fi
EOF
    chmod +x claude-agents-start.sh
    print_message "✅ Created quick start script: ./claude-agents-start.sh" "$GREEN"
}

# Main installation flow
main() {
    print_header
    
    print_message "Starting installation in: $(pwd)" "$BLUE"
    echo ""
    
    # Run checks and installation
    check_git_repo
    check_python
    install_agents
    install_dependencies
    configure_api_keys
    
    echo ""
    print_message "════════════════════════════════════════════════════════════" "$GREEN"
    
    if verify_installation; then
        create_quickstart
        
        print_message "✨ Installation completed successfully!" "$GREEN"
        print_message "════════════════════════════════════════════════════════════" "$GREEN"
        echo ""
        print_message "Next steps:" "$BLUE"
        print_message "  1. Run ./claude-agents-start.sh to get started" "$NC"
        print_message "  2. Or start Claude Code directly in this directory" "$NC"
        print_message "  3. Use '#pipeline' prefix for complex tasks" "$NC"
        echo ""
        print_message "📚 Documentation: Check README.md for detailed usage" "$BLUE"
    else
        print_message "⚠️  Installation completed with warnings" "$YELLOW"
        print_message "   Please check the error messages above" "$YELLOW"
    fi
}

# Run main function
main "$@"