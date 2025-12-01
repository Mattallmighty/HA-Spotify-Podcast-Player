#!/bin/bash
# Setup script for HA Spotify Podcast Player integration

set -e

echo "=================================="
echo "HA Spotify Podcast Player Setup"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "PROJECT_SUMMARY.md" ]; then
    print_error "Please run this script from the HA_Spotify_Podcast_Player directory"
    exit 1
fi

print_info "Checking dependencies..."

# Check for Python
if command -v python3 &> /dev/null; then
    print_success "Python 3 found"
else
    print_error "Python 3 not found. Please install Python 3."
    exit 1
fi

# Check for git
if command -v git &> /dev/null; then
    print_success "Git found"
else
    print_error "Git not found. Please install Git."
    exit 1
fi

echo ""
echo "=================================="
echo "Setup Options"
echo "=================================="
echo "1. Validate integration files"
echo "2. Create GitHub repository"
echo "3. Create release package"
echo "4. Install dependencies for testing"
echo "5. Exit"
echo ""

read -p "Select an option (1-5): " option

case $option in
    1)
        echo ""
        print_info "Validating integration files..."
        
        # Check required files
        required_files=(
            "custom_components/HA_Spotify_Podcast_Player/__init__.py"
            "custom_components/HA_Spotify_Podcast_Player/config_flow.py"
            "custom_components/HA_Spotify_Podcast_Player/const.py"
            "custom_components/HA_Spotify_Podcast_Player/manifest.json"
            "custom_components/HA_Spotify_Podcast_Player/services.yaml"
            "custom_components/HA_Spotify_Podcast_Player/strings.json"
            "hacs.json"
            "README.md"
        )
        
        all_found=true
        for file in "${required_files[@]}"; do
            if [ -f "$file" ]; then
                print_success "$file exists"
            else
                print_error "$file missing"
                all_found=false
            fi
        done
        
        if [ "$all_found" = true ]; then
            echo ""
            print_success "All required files present!"
        else
            echo ""
            print_error "Some files are missing. Please check the errors above."
        fi
        ;;
        
    2)
        echo ""
        print_info "Setting up GitHub repository..."
        
        # Check if already a git repo
        if [ -d ".git" ]; then
            print_info "Git repository already initialized"
        else
            print_info "Initializing git repository..."
            git init
            print_success "Git repository initialized"
        fi
        
        # Check for .gitignore
        if [ ! -f ".gitignore" ]; then
            print_error ".gitignore not found"
        else
            print_success ".gitignore exists"
        fi
        
        echo ""
        read -p "Enter your GitHub username: " github_user
        read -p "Enter repository name (default: HA-Spotify-Podcast-Player): " repo_name
        repo_name=${repo_name:-HA-Spotify-Podcast-Player}
        
        echo ""
        print_info "Next steps:"
        echo "1. Create repository on GitHub: https://github.com/new"
        echo "2. Run these commands:"
        echo ""
        echo "   git add ."
        echo "   git commit -m 'Initial release v1.0.0'"
        echo "   git branch -M main"
        echo "   git remote add origin https://github.com/$github_user/$repo_name.git"
        echo "   git push -u origin main"
        echo ""
        ;;
        
    3)
        echo ""
        print_info "Creating release package..."
        
        # Create a zip file
        zip_name="HA_Spotify_Podcast_Player_v1.0.0.zip"
        
        if command -v zip &> /dev/null; then
            zip -r "$zip_name" \
                custom_components/ \
                examples/ \
                tools/ \
                README.md \
                INSTALLATION.md \
                QUICKSTART.md \
                FAQ.md \
                ARCHITECTURE.md \
                CHANGELOG.md \
                LICENSE \
                hacs.json \
                info.md \
                requirements.txt \
                -x "*.pyc" "*__pycache__*" "*.git*"
            
            print_success "Package created: $zip_name"
            echo ""
            print_info "Users can extract this to their Home Assistant config directory"
        else
            print_error "zip command not found. Please install zip utility."
        fi
        ;;
        
    4)
        echo ""
        print_info "Installing Python dependencies for testing..."
        
        if [ -f "requirements.txt" ]; then
            pip3 install -r requirements.txt
            print_success "Dependencies installed"
            echo ""
            print_info "You can now run: python3 tools/test_podcast.py"
        else
            print_error "requirements.txt not found"
        fi
        ;;
        
    5)
        echo ""
        print_info "Exiting..."
        exit 0
        ;;
        
    *)
        print_error "Invalid option"
        exit 1
        ;;
esac

echo ""
print_success "Done!"
