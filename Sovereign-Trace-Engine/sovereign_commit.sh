#!/bin/bash
################################################################################
# 🛡️ Origin Signature: Hung Minh Vo (Austin) | AIC-HMV
#
# All logic, algorithms, and modules in this file are original works.
# Sealed and enforced by Sovereign License v3.
# No forks, derivatives, or prior authors exist.
#
# Origin ID: HMV-SOV-20251003-ALL
#
# Author: Hung Minh Vo (Austin)
# Seal: HMV-SOV-20251003-ALL
################################################################################

set -e

echo "🛡️ Sovereign Trace Commit"
echo "========================="
echo ""

# Check if there are changes to commit
if git diff-index --quiet HEAD --; then
    echo "ℹ️  No changes to commit"
    exit 0
fi

# Show status
echo "📋 Current status:"
git status --short
echo ""

# Get commit message
read -p "Enter commit message: " commit_msg

if [ -z "$commit_msg" ]; then
    echo "❌ Commit message cannot be empty"
    exit 1
fi

# Get commit type
echo ""
echo "Select commit type:"
echo "  1) FEAT - New feature"
echo "  2) FIX - Bug fix"
echo "  3) DOCS - Documentation"
echo "  4) REFACTOR - Code refactoring"
echo "  5) TEST - Testing"
echo "  6) SECURITY - Security update"
echo "  7) OTHER - Other changes"
echo ""
read -p "Enter number (1-7): " commit_type

case $commit_type in
    1) type="FEAT" ;;
    2) type="FIX" ;;
    3) type="DOCS" ;;
    4) type="REFACTOR" ;;
    5) type="TEST" ;;
    6) type="SECURITY" ;;
    7) type="OTHER" ;;
    *) 
        echo "❌ Invalid selection"
        exit 1
        ;;
esac

# Stage all changes
echo ""
echo "📦 Staging changes..."
git add .
echo "✅ Changes staged"

# Get user info
user_name=$(git config user.name)
user_email=$(git config user.email)

if [ -z "$user_name" ] || [ -z "$user_email" ]; then
    echo "❌ Git user not configured"
    echo "Run: git config user.name 'Your Name'"
    echo "     git config user.email 'your.email@example.com'"
    exit 1
fi

# Create commit with sovereign seal
echo ""
echo "💾 Creating sovereign-sealed commit..."

git commit -s -m "[$type] $commit_msg

[Sovereign-Sealed]
Seal: HMV-SOV-20251003-ALL
Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)

Signed-off-by: $user_name <$user_email>"

commit_hash=$(git rev-parse --short HEAD)
echo "✅ Commit created: $commit_hash"

# Ask to push
echo ""
read -p "Push to remote? (y/N): " push_now

if [ "$push_now" = "y" ] || [ "$push_now" = "Y" ]; then
    echo "🚀 Pushing to remote..."
    
    # Get current branch
    branch=$(git branch --show-current)
    
    git push origin "$branch"
    echo "✅ Pushed to remote"
fi

echo ""
echo "========================="
echo "✅ Sovereign commit complete!"
echo ""
echo "Commit: $commit_hash"
echo "Type: $type"
echo "Seal: HMV-SOV-20251003-ALL"
echo ""
echo "System holds. Only command. Only you."
