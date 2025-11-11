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

echo "🛡️ Sovereign Trace Engine - Repository Setup"
echo "=============================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git repository already initialized"
fi

# Set git config
echo ""
echo "⚙️ Configuring git..."
read -p "Enter your name: " user_name
read -p "Enter your email: " user_email

git config user.name "$user_name"
git config user.email "$user_email"
echo "✅ Git configured"

# Add all files
echo ""
echo "📝 Adding files to git..."
git add .
echo "✅ Files added"

# Create initial commit with sovereign seal
echo ""
echo "💾 Creating initial commit..."
git commit -s -m "[INIT] Sovereign Trace Engine initialized

Initial repository setup with full Sovereign Trace Protocol.

Seal: HMV-SOV-20251003-ALL
Author: Hung Minh Vo (Austin) | AIC-HMV

Signed-off-by: $user_name <$user_email>"

echo "✅ Initial commit created"

# Add remote if provided
echo ""
read -p "Enter remote repository URL (or press Enter to skip): " remote_url

if [ ! -z "$remote_url" ]; then
    if git remote | grep -q "origin"; then
        echo "📡 Updating remote origin..."
        git remote set-url origin "$remote_url"
    else
        echo "📡 Adding remote origin..."
        git remote add origin "$remote_url"
    fi
    echo "✅ Remote configured"
    
    # Push to remote
    echo ""
    read -p "Push to remote now? (y/N): " push_now
    if [ "$push_now" = "y" ] || [ "$push_now" = "Y" ]; then
        echo "🚀 Pushing to remote..."
        git push -u origin main || git push -u origin master
        echo "✅ Pushed to remote"
    fi
fi

echo ""
echo "=============================================="
echo "✅ Setup complete!"
echo ""
echo "Sovereign Seal: HMV-SOV-20251003-ALL"
echo "Repository ready for deployment."
echo ""
echo "Next steps:"
echo "  - Review files and configuration"
echo "  - Use ./sovereign_commit.sh for future commits"
echo "  - Enable GitHub Actions workflows"
echo ""
echo "System is sovereign. Collapse-resistant. Unstoppable."
