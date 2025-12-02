#!/bin/bash
# Version bump script for HA Spotify Podcast Player
# Usage: ./version_bump.sh [major|minor|patch]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "custom_components/HA_Spotify_Podcast_Player/manifest.json" ]; then
    print_error "Please run this script from the repository root"
    exit 1
fi

# Get current version from manifest.json
CURRENT_VERSION=$(jq -r '.version' custom_components/HA_Spotify_Podcast_Player/manifest.json)

if [ -z "$CURRENT_VERSION" ] || [ "$CURRENT_VERSION" = "null" ]; then
    print_error "Could not read current version from manifest.json"
    exit 1
fi

print_info "Current version: $CURRENT_VERSION"

# Parse version components
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"

# Determine bump type
BUMP_TYPE=${1:-patch}

case $BUMP_TYPE in
    major)
        MAJOR=$((MAJOR + 1))
        MINOR=0
        PATCH=0
        ;;
    minor)
        MINOR=$((MINOR + 1))
        PATCH=0
        ;;
    patch)
        PATCH=$((PATCH + 1))
        ;;
    *)
        print_error "Invalid bump type: $BUMP_TYPE"
        echo "Usage: $0 [major|minor|patch]"
        exit 1
        ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"

echo ""
print_warning "Version bump: $CURRENT_VERSION → $NEW_VERSION ($BUMP_TYPE)"
echo ""

# Confirm with user
read -p "Continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Aborted"
    exit 0
fi

echo ""
print_info "Updating files..."

# Update manifest.json
jq --arg version "$NEW_VERSION" '.version = $version' \
    custom_components/HA_Spotify_Podcast_Player/manifest.json > /tmp/manifest.json
mv /tmp/manifest.json custom_components/HA_Spotify_Podcast_Player/manifest.json
print_success "Updated manifest.json"

# Check if CHANGELOG.md exists and has the right format
if [ ! -f "CHANGELOG.md" ]; then
    print_warning "CHANGELOG.md not found, creating one"
    cat > CHANGELOG.md << EOF
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [$NEW_VERSION] - $(date +%Y-%m-%d)

### Added
- Initial release

EOF
    print_success "Created CHANGELOG.md"
else
    # Add new version section to CHANGELOG.md
    DATE=$(date +%Y-%m-%d)
    
    # Insert new version after the header
    sed -i "/^## \[Unreleased\]/a\\
\\
## [$NEW_VERSION] - $DATE\\
\\
### Added\\
- \\
\\
### Changed\\
- \\
\\
### Fixed\\
- " CHANGELOG.md 2>/dev/null || {
        # If no Unreleased section, add after the first ## heading
        sed -i "0,/^## \[/s//## [$NEW_VERSION] - $DATE\n\n### Added\n- \n\n### Changed\n- \n\n### Fixed\n- \n\n&/" CHANGELOG.md
    }
    
    print_success "Updated CHANGELOG.md"
    print_warning "Please edit CHANGELOG.md to add release notes"
fi

echo ""
print_info "Git operations..."

# Stage changes
git add custom_components/HA_Spotify_Podcast_Player/manifest.json CHANGELOG.md
print_success "Staged changes"

# Show what will be committed
echo ""
print_info "Changes to be committed:"
git diff --cached --stat

echo ""
read -p "Commit these changes? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    git reset HEAD custom_components/HA_Spotify_Podcast_Player/manifest.json CHANGELOG.md
    print_info "Changes unstaged"
    exit 0
fi

# Commit
git commit -m "chore: bump version to $NEW_VERSION"
print_success "Committed changes"

# Create tag
git tag -a "v$NEW_VERSION" -m "Release version $NEW_VERSION"
print_success "Created tag v$NEW_VERSION"

echo ""
print_success "Version bumped to $NEW_VERSION!"
echo ""
print_info "Next steps:"
echo "  1. Edit CHANGELOG.md to add release notes for v$NEW_VERSION"
echo "  2. Commit the changelog: git add CHANGELOG.md && git commit --amend --no-edit"
echo "  3. Update the tag: git tag -d v$NEW_VERSION && git tag -a v$NEW_VERSION -m 'Release version $NEW_VERSION'"
echo "  4. Push changes: git push origin main"
echo "  5. Push tag: git push origin v$NEW_VERSION"
echo ""
print_warning "The GitHub Action will automatically create the release when you push the tag!"
echo ""
