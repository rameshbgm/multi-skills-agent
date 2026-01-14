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

# Create .env file from example if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please add your OPENAI_API_KEY to the .env file!"
    echo "   Run: echo 'OPENAI_API_KEY=your-key-here' > .env"
    echo ""
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
echo "║  1. Add your OpenAI API key:                                      ║"
echo "║     echo 'OPENAI_API_KEY=sk-...' > .env                           ║"
echo "║                                                                   ║"
echo "║  2. Run the agent:                                                ║"
echo "║     python main.py                                                ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""
