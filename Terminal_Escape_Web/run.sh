#!/bin/bash
# run.sh - Terminal Escape Web Game

echo "========================================"
echo "🚀 Mankind vs AI: Terminal Escape - Web"
echo "========================================"

cd backend

if [ -d "venv" ]; then
    echo "✅ Activating virtual environment..."
    source venv/bin/activate 2>/dev/null || venv\Scripts\activate
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found!"
    exit 1
fi

echo "📦 Installing dependencies if needed..."
pip install -r requirements.txt --quiet

echo ""
echo "🌐 Starting the game server..."
echo "Open your browser and go to: http://127.0.0.1:5000"
echo "========================================"

python app.py