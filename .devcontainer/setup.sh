#!/bin/bash

# Multi-Skills Agent - Codespace Setup Script
# This script runs automatically when the Codespace is created

echo "🚀 Setting up Multi-Skills Agent environment..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create logs directory if it doesn't exist
mkdir -p logs

# Rename .env.example to .env if .env doesn't exist
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        echo "📝 Renaming .env.example to .env..."
        mv .env.example .env
    fi
fi

# Add activation to bashrc and zshrc for convenience
echo "source $(pwd)/venv/bin/activate" >> ~/.bashrc
echo "source $(pwd)/venv/bin/activate" >> ~/.zshrc

echo ""
echo "✅ Setup complete!"
echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                   MULTI-SKILLS AGENT                              ║"
echo "╠═══════════════════════════════════════════════════════════════════╣"
echo "║                                                                   ║"
echo "║  To get started:                                                  ║"
echo "║                                                                   ║"
echo "║  1. Edit .env file and add your OpenAI API key:                   ║"
echo "║     - Open .env in the editor                                     ║"
echo "║     - Replace 'sk-your-api-key-here' with your actual key         ║"
echo "║                                                                   ║"
echo "║  2. Run the agent:                                                ║"
echo "║     python main.py                                                ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

