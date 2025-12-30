#!/bin/bash

# Deployment script for Gophish Python API Client v1.0.0
# This script will push all changes to the GitHub repository

echo "🚀 Deploying Gophish Python API Client v1.0.0..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Check if there are uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Warning: There are uncommitted changes"
    git status --short
    echo ""
fi

# Show the commit we're about to push
echo "📝 Commit to push:"
git log --oneline -1
echo ""

# Show files changed
echo "📁 Files changed:"
git diff --name-status HEAD~1
echo ""

# Ask for confirmation
read -p "🤔 Do you want to push these changes to GitHub? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔄 Pushing to GitHub..."
    
    # Try to push
    if git push origin master; then
        echo "✅ Successfully pushed to GitHub!"
        echo "🌐 Repository: https://github.com/Chris-C1108/api-client-python3-12"
        echo "📋 Changes include:"
        echo "   - Python 3.8-3.12 support"
        echo "   - Updated dependencies (requests 2.32.5+)"
        echo "   - Modern project structure (pyproject.toml)"
        echo "   - Comprehensive test suite"
        echo "   - Modern CI/CD pipeline"
        echo "   - Security enhancements"
        echo "   - Full backward compatibility"
    else
        echo "❌ Failed to push to GitHub"
        echo "💡 You may need to:"
        echo "   1. Check your GitHub token permissions"
        echo "   2. Ensure the repository exists"
        echo "   3. Verify network connectivity"
        echo ""
        echo "🔧 Manual deployment options:"
        echo "   1. Use the generated modernization.patch file"
        echo "   2. Copy files manually to your repository"
        echo "   3. Use GitHub CLI: gh repo create --push"
        exit 1
    fi
else
    echo "❌ Deployment cancelled"
    echo "💡 To deploy later, run: git push origin master"
    exit 0
fi

echo ""
echo "🎉 Deployment complete!"
echo "📚 Next steps:"
echo "   1. Update PyPI package (if applicable)"
echo "   2. Create a GitHub release"
echo "   3. Update documentation"
echo "   4. Announce the modernized version"