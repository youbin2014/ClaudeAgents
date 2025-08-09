#!/bin/bash

# Claude Code Multi-Agent Pipeline Setup Script
# This script sets up the environment for the multi-agent development pipeline

echo "🚀 Claude Code Multi-Agent Pipeline Setup"
echo "========================================="

# Check if we're in the right directory
if [ ! -d ".claude/agents" ]; then
    echo "❌ Error: .claude/agents directory not found!"
    echo "Please run this script from the ClaudeAgents root directory."
    exit 1
fi

# Check Python installation
echo "📦 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION found"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install openai python-dotenv --quiet
if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed"
else
    echo "⚠️  Warning: Failed to install some Python dependencies"
    echo "   You can install them manually with: pip3 install openai python-dotenv"
fi

# Check for .env file
echo ""
echo "🔑 Checking API configuration..."
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# OpenAI API Key for GPT-5 integration (optional)
# Get your key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=

# Add other configuration here as needed
EOF
    echo "✅ Created .env file"
    echo "⚠️  Please add your OpenAI API key to .env for GPT-5 integration"
    echo "   The system will work without it using Claude-only mode"
else
    echo "✅ .env file exists"
    if grep -q "OPENAI_API_KEY=" .env && ! grep -q "OPENAI_API_KEY=$" .env; then
        echo "✅ OpenAI API key configured"
    else
        echo "⚠️  OpenAI API key not configured (GPT-5 features will be disabled)"
    fi
fi

# Make scripts executable
echo ""
echo "🔧 Setting up scripts..."
chmod +x scripts/gpt5_bridge.py 2>/dev/null
echo "✅ Scripts configured"

# Verify subagents
echo ""
echo "🤖 Verifying subagents..."
AGENT_COUNT=$(ls -1 .claude/agents/*.md 2>/dev/null | wc -l)
if [ $AGENT_COUNT -gt 0 ]; then
    echo "✅ Found $AGENT_COUNT subagents:"
    for agent in .claude/agents/*.md; do
        agent_name=$(basename "$agent" .md)
        echo "   - $agent_name"
    done
else
    echo "❌ No subagents found in .claude/agents/"
    exit 1
fi

# Create examples directory if it doesn't exist
if [ ! -d "examples" ]; then
    mkdir -p examples
    echo "✅ Created examples directory"
fi

# Final instructions
echo ""
echo "✨ Setup Complete!"
echo "=================="
echo ""
echo "Next steps:"
echo "1. Open Claude Code in this directory"
echo "2. Type '/agents' to see all available subagents"
echo "3. Try a simple query to test the router:"
echo "   'What is async programming?'"
echo "4. Try a pipeline query:"
echo "   '@pipeline Convert a module to async with tests'"
echo ""
echo "For GPT-5 integration:"
echo "1. Add your OpenAI API key to .env file"
echo "2. The system will automatically use GPT-5 when available"
echo ""
echo "Documentation:"
echo "- README.md for full documentation"
echo "- examples/ for workflow examples"
echo "- .claude/agents/ to customize agents"
echo ""
echo "Happy coding! 🎉"