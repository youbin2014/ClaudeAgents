#!/bin/bash

# Claude Agents Pipeline - Universal Installation Script
# Auto-detects system and provides optimal installation experience
# Compatible with Windows/WSL, Linux, macOS, and various Python configurations

set -e  # Exit on error

# System detection
detect_system() {
    # Platform detection
    if [[ "$OSTYPE" =~ ^darwin ]]; then
        SYSTEM="macos"
        PLATFORM="macOS"
    elif [[ "$OSTYPE" =~ ^linux ]]; then
        SYSTEM="linux"
        PLATFORM="Linux"
    elif [[ "$OSTYPE" =~ ^(msys|cygwin|win32) ]] || [[ -n "$WSL_DISTRO_NAME" ]]; then
        SYSTEM="windows"
        PLATFORM="Windows/WSL"
    else
        SYSTEM="unknown"
        PLATFORM="Unknown"
    fi
    
    # Architecture detection
    ARCH=$(uname -m 2>/dev/null || echo "unknown")
    
    # Shell detection
    CURRENT_SHELL=$(basename "$SHELL" 2>/dev/null || echo "unknown")
}

# Colors with fallback for different terminals
setup_colors() {
    if [[ -t 1 ]] && [[ "${TERM:-}" != "dumb" ]] && command -v tput >/dev/null 2>&1; then
        RED=$(tput setaf 1 2>/dev/null || echo '')
        GREEN=$(tput setaf 2 2>/dev/null || echo '')
        YELLOW=$(tput setaf 3 2>/dev/null || echo '')
        BLUE=$(tput setaf 4 2>/dev/null || echo '')
        BOLD=$(tput bold 2>/dev/null || echo '')
        NC=$(tput sgr0 2>/dev/null || echo '')
    else
        RED=''
        GREEN=''
        YELLOW=''
        BLUE=''
        BOLD=''
        NC=''
    fi
}

# Configuration
TARGET_DIR=".."
CLAUDE_AGENTS_DIR="../.claude/agents"
SCRIPTS_DIR="../scripts"
CONFIG_FILE="../.env"

# Print functions
print_msg() { echo -e "${2:-}${1}${NC}"; }
print_header() {
    echo ""
    echo "${BOLD}============================================================${NC}"
    echo "${BOLD}  🚀 Claude Agents Pipeline - Universal Installer${NC}"
    echo "${BOLD}============================================================${NC}"
    echo ""
    print_msg "System: ${PLATFORM} (${ARCH})" "$BLUE"
    print_msg "Shell: ${CURRENT_SHELL}" "$BLUE"
    print_msg "Installing from: $(pwd)" "$BLUE"
    print_msg "Installing to: $(cd "$TARGET_DIR" 2>/dev/null && pwd || echo "$(pwd)/..")" "$BLUE"
    echo ""
}

# Fix line endings for Windows/WSL
fix_line_endings() {
    if [[ "$SYSTEM" == "windows" ]]; then
        print_msg "Fixing line endings for Windows/WSL..." "$BLUE"
        
        # Try multiple methods to fix line endings
        if command -v dos2unix >/dev/null 2>&1; then
            dos2unix "$0" *.sh 2>/dev/null || true
            print_msg "  ✓ Fixed with dos2unix" "$GREEN"
        elif command -v sed >/dev/null 2>&1; then
            sed -i 's/\r$//' "$0" *.sh 2>/dev/null || true
            print_msg "  ✓ Fixed with sed" "$GREEN"
        else
            print_msg "  ! Line ending tools not available, continuing..." "$YELLOW"
        fi
    fi
}

# Find working Python installation
find_python() {
    print_msg "Finding Python installation..." "$BLUE"
    
    # Python candidates in order of preference
    python_candidates=()
    
    # Add system-specific candidates
    case "$SYSTEM" in
        "windows")
            python_candidates=("python" "python3" "py" "python3.12" "python3.11" "python3.10" "python3.9" "python3.8")
            ;;
        "macos")
            python_candidates=("python3" "python" "python3.12" "python3.11" "python3.10" "python3.9" "python3.8")
            ;;
        "linux"|*)
            python_candidates=("python3" "python" "python3.12" "python3.11" "python3.10" "python3.9" "python3.8")
            ;;
    esac
    
    # Test each candidate
    for cmd in "${python_candidates[@]}"; do
        if command -v "$cmd" >/dev/null 2>&1; then
            version=$($cmd -c "import sys; print('.'.join(map(str, sys.version_info[:2])))" 2>/dev/null)
            if [[ $? -eq 0 ]] && $cmd -c "import sys; sys.exit(0 if sys.version_info >= (3,8) else 1)" 2>/dev/null; then
                PYTHON_CMD="$cmd"
                PYTHON_VERSION="$version"
                print_msg "  ✓ Found Python $version ($cmd)" "$GREEN"
                return 0
            fi
        fi
    done
    
    # Python not found
    print_msg "  ✗ No suitable Python 3.8+ found" "$RED"
    print_msg "    Please install Python 3.8+ and try again" "$RED"
    
    case "$SYSTEM" in
        "windows")
            print_msg "    Download from: https://www.python.org/downloads/" "$YELLOW"
            ;;
        "macos")
            print_msg "    Try: brew install python3" "$YELLOW"
            ;;
        "linux")
            print_msg "    Try: sudo apt update && sudo apt install python3 python3-pip" "$YELLOW"
            ;;
    esac
    
    return 1
}

# Install agents
install_agents() {
    print_msg "Installing agents..." "$BLUE"
    
    # Create directory
    mkdir -p "$CLAUDE_AGENTS_DIR"
    
    # Get script directory
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # Copy agents if they exist
    agent_count=0
    if [[ -d "$SCRIPT_DIR/.claude/agents" ]]; then
        cp -r "$SCRIPT_DIR/.claude/agents/"* "$CLAUDE_AGENTS_DIR/" 2>/dev/null || true
        agent_count=$(find "$CLAUDE_AGENTS_DIR" -name "*.md" 2>/dev/null | wc -l)
        print_msg "  ✓ Copied $agent_count agent files" "$GREEN"
    else
        # Create essential agents
        cat > "$CLAUDE_AGENTS_DIR/pipeline.md" << 'EOF'
# Pipeline Agent
Core pipeline orchestration for complex task management and multi-step operations.
EOF
        
        cat > "$CLAUDE_AGENTS_DIR/async_converter.md" << 'EOF'  
# Async Converter
Convert synchronous code to asynchronous patterns with proper async/await syntax.
EOF
        
        cat > "$CLAUDE_AGENTS_DIR/router.md" << 'EOF'
# Router Agent  
Routes queries to appropriate execution mode based on complexity analysis.
Supports @quick and @pipeline override tags.
EOF
        
        agent_count=3
        print_msg "  ✓ Created $agent_count essential agents" "$GREEN"
    fi
}

# Install scripts
install_scripts() {
    print_msg "Installing scripts..." "$BLUE"
    
    mkdir -p "$SCRIPTS_DIR"
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    essential_scripts=("gpt5_bridge.py" "pipeline_monitor.py" "configure_api.py")
    
    for script in "${essential_scripts[@]}"; do
        src="$SCRIPT_DIR/scripts/$script"
        dst="$SCRIPTS_DIR/$script"
        
        if [[ -f "$src" ]]; then
            if [[ -f "$dst" ]] && cmp -s "$src" "$dst" 2>/dev/null; then
                print_msg "  ✓ $script (up to date)" "$GREEN"
            else
                if cp "$src" "$dst" 2>/dev/null; then
                    print_msg "  ✓ $script" "$GREEN"
                else
                    print_msg "  ! $script (copy failed)" "$YELLOW"
                fi
            fi
        else
            print_msg "  ! $script (not found in source)" "$YELLOW"
        fi
    done
}

# Install dependencies with system-specific handling
install_dependencies() {
    print_msg "Installing Python packages..." "$BLUE"
    
    # Check if pip is available
    if ! $PYTHON_CMD -m pip --version >/dev/null 2>&1; then
        print_msg "  ! pip not available, attempting to install..." "$YELLOW"
        
        case "$SYSTEM" in
            "linux")
                if command -v apt >/dev/null 2>&1; then
                    print_msg "    Installing pip via apt..." "$BLUE"
                    sudo apt update && sudo apt install -y python3-pip
                elif command -v yum >/dev/null 2>&1; then
                    print_msg "    Installing pip via yum..." "$BLUE"
                    sudo yum install -y python3-pip
                fi
                ;;
            "macos")
                if command -v brew >/dev/null 2>&1; then
                    print_msg "    Installing pip via brew..." "$BLUE"
                    brew install python3
                fi
                ;;
            "windows")
                print_msg "    Please install pip manually or use Python installer with pip" "$YELLOW"
                ;;
        esac
        
        # Check again after installation attempt
        if ! $PYTHON_CMD -m pip --version >/dev/null 2>&1; then
            print_msg "  ! pip still not available, skipping package installation" "$YELLOW"
            return 0
        fi
    fi
    
    # Essential packages for the pipeline
    packages=("openai>=1.0.0" "python-dotenv>=1.0.0" "structlog>=23.0.0")
    
    installed=0
    failed=0
    
    for pkg in "${packages[@]}"; do
        pkg_name=$(echo "$pkg" | cut -d'>' -f1)
        if $PYTHON_CMD -m pip install -q "$pkg" >/dev/null 2>&1; then
            print_msg "  ✓ $pkg_name" "$GREEN"
            ((installed++))
        else
            print_msg "  ! $pkg_name (failed)" "$YELLOW"
            ((failed++))
        fi
    done
    
    if [[ $failed -eq 0 ]]; then
        print_msg "  ✓ All packages installed successfully" "$GREEN"
    else
        print_msg "  ! $failed packages failed, $installed succeeded" "$YELLOW"
        print_msg "    Pipeline will work with reduced functionality" "$YELLOW"
    fi
}

# Create configuration
create_config() {
    print_msg "Creating configuration..." "$BLUE"
    
    if [[ ! -f "$CONFIG_FILE" ]]; then
        cat > "$CONFIG_FILE" << 'EOF'
# Claude Agents Pipeline Configuration
# Generated by Universal Installer

# OpenAI API Key for GPT-5 integration
# Uncomment and add your key:
# OPENAI_API_KEY=your_openai_api_key_here

# Claude API Key (optional - Claude Code handles authentication)  
# CLAUDE_API_KEY=your_claude_api_key_here

# Pipeline Settings
PIPELINE_MODE=auto
LOG_LEVEL=INFO
EOF
        print_msg "  ✓ Created .env configuration file" "$GREEN"
    else
        print_msg "  ✓ Configuration file already exists" "$GREEN"
    fi
}

# Create system-specific start script
create_start_script() {
    print_msg "Creating start script..." "$BLUE"
    
    case "$SYSTEM" in
        "windows")
            start_script="../claude-agents-start.cmd"
            cat > "$start_script" << 'EOF'
@echo off
echo Claude Agents Pipeline Ready!
echo.
echo Usage in Claude Code:
echo   1. Start Claude Code in this directory
echo   2. Use pipeline commands:
echo      - "Convert this to async" (auto-detect)
echo      - "@pipeline Implement feature X" (explicit)
echo.
pause
EOF
            ;;
        *)
            start_script="../claude-agents-start.sh"
            cat > "$start_script" << 'EOF'
#!/bin/bash
# Claude Agents Pipeline Start Script

# Load environment
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "🚀 Claude Agents Pipeline Ready!"
echo ""
echo "Usage in Claude Code:"
echo "  1. Start Claude Code in this directory"  
echo "  2. Use pipeline commands:"
echo "     - 'Convert this to async' (auto-detect)"
echo "     - '@pipeline Implement feature X' (explicit)"
echo ""
echo "Monitor pipeline: python scripts/pipeline_monitor.py"
echo ""

# Optional: Start Claude Code if available
if command -v claude-code >/dev/null 2>&1; then
    read -p "Start Claude Code now? (y/n): " -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        claude-code
    fi
fi
EOF
            chmod +x "$start_script"
            ;;
    esac
    
    print_msg "  ✓ Created start script: $start_script" "$GREEN"
}

# Verify installation
verify_installation() {
    print_msg "Verifying installation..." "$BLUE"
    
    checks=(
        "Agents directory:$CLAUDE_AGENTS_DIR"
        "Scripts directory:$SCRIPTS_DIR"  
        "Configuration file:$CONFIG_FILE"
        "Python installation:$PYTHON_CMD"
    )
    
    all_passed=true
    
    for check in "${checks[@]}"; do
        name="${check%%:*}"
        path="${check#*:}"
        
        case "$name" in
            *"directory")
                if [[ -d "$path" ]]; then
                    count=$(find "$path" -type f 2>/dev/null | wc -l)
                    print_msg "  ✓ $name ($count files)" "$GREEN"
                else
                    print_msg "  ✗ $name" "$RED"
                    all_passed=false
                fi
                ;;
            *"file")
                if [[ -f "$path" ]]; then
                    print_msg "  ✓ $name" "$GREEN"
                else
                    print_msg "  ✗ $name" "$RED"
                    all_passed=false
                fi
                ;;
            *"installation")
                if command -v "$path" >/dev/null 2>&1; then
                    print_msg "  ✓ $name ($PYTHON_VERSION)" "$GREEN"
                else
                    print_msg "  ✗ $name" "$RED"
                    all_passed=false
                fi
                ;;
        esac
    done
    
    return $([[ "$all_passed" == "true" ]] && echo 0 || echo 1)
}

# Main installation flow
main() {
    # Initialize
    detect_system
    setup_colors
    
    print_header
    
    # Pre-installation checks
    if [[ ! -d "$TARGET_DIR" ]]; then
        print_msg "Target directory does not exist, creating..." "$YELLOW"
        mkdir -p "$TARGET_DIR"
    fi
    
    if [[ ! -d "$TARGET_DIR/.git" ]]; then
        print_msg "Warning: Target directory is not a git repository" "$YELLOW"
        print_msg "Installing to: $(cd "$TARGET_DIR" && pwd)" "$YELLOW"
        echo ""
        read -p "Continue installation? (y/n): " -r
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_msg "Installation cancelled by user" "$YELLOW"
            exit 0
        fi
        echo ""
    fi
    
    # Fix line endings if needed
    fix_line_endings
    
    # Run installation steps
    if ! find_python; then
        print_msg "\n✗ Installation failed: Python requirement not met" "$RED"
        exit 1
    fi
    
    install_agents
    install_scripts
    install_dependencies
    create_config
    create_start_script
    
    # Final verification and completion
    echo ""
    print_msg "${BOLD}============================================================${NC}" "$GREEN"
    
    if verify_installation; then
        print_msg "${BOLD}✅ Installation completed successfully!${NC}" "$GREEN"
        print_msg "${BOLD}============================================================${NC}" "$GREEN"
        echo ""
        print_msg "System: $PLATFORM" "$BLUE"
        print_msg "Python: $PYTHON_VERSION" "$BLUE"
        print_msg "Location: $(cd "$TARGET_DIR" && pwd)" "$BLUE"
        echo ""
        print_msg "${BOLD}Next steps:${NC}" "$BLUE"
        print_msg "1. Add your OPENAI_API_KEY to $CONFIG_FILE" "$NC"
        print_msg "2. Start Claude Code in the target directory" "$NC"
        print_msg "3. Use '@pipeline' prefix for complex tasks" "$NC"
        print_msg "4. Use '@quick' prefix to force quick responses" "$NC"
        echo ""
        print_msg "📚 Check INSTALL_GUIDE.md for detailed usage information" "$BLUE"
        
        # Offer to start
        if [[ "$SYSTEM" != "windows" ]] && command -v claude-code >/dev/null 2>&1; then
            echo ""
            read -p "🚀 Start Claude Code now? (y/n): " -r
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                cd "$TARGET_DIR" && claude-code
            fi
        fi
        
    else
        print_msg "${BOLD}⚠️  Installation completed with warnings${NC}" "$YELLOW"
        print_msg "${BOLD}============================================================${NC}" "$YELLOW"
        print_msg "Some components may not be fully functional" "$YELLOW"
        print_msg "Check the verification results above" "$YELLOW"
    fi
}

# Handle interrupts gracefully
trap 'echo; print_msg "Installation interrupted by user" "$YELLOW"; exit 130' INT

# Run main function
main "$@"