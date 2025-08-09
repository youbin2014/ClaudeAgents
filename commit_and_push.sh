#!/bin/bash

# Script to commit and push changes
# Run this script manually to push the production optimization changes

echo "🚀 Committing and pushing production environment optimizations..."

# Add SSH key
ssh-add ~/.ssh/id_ed25519_github

# Navigate to project directory
cd /Users/bytedance/PycharmProjects/ClaudeAgents

# Add all changes
git add -A

# Commit with detailed message
git commit -m "Add production deployment tools and one-click installation

- Created install.sh for one-click setup in production environments
- Added setup.py as Python alternative to bash installer
- Created configure_api.py for interactive GPT-5 API key configuration
- Added verify_setup.py for installation verification
- Updated README with production deployment guide at the top
- Automatic GPT-5 API key prompting during installation
- Support for environments without GPT-5 (graceful fallback)

Features:
- One-command installation: git clone && ./install.sh
- Interactive API key configuration with secure .env storage
- Comprehensive verification tool to check setup status
- Cross-platform support with Python alternative
- Clear documentation for production use cases

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to remote
git push origin main

echo "✅ Changes pushed successfully!"