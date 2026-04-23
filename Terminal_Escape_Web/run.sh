#!/bin/bash
# run.sh - Terminal Escape Web Game

echo "========================================"
echo "🚀 Mankind vs AI: Terminal Escape - Web"
echo "========================================"

# رفتن به پوشه backend
cd backend

# فعال کردن محیط مجازی (اگر وجود داشته باشد)
if [ -d "venv" ]; then
    echo "✅ Activating virtual environment..."
    source venv/bin/activate 2>/dev/null || venv\Scripts\activate
fi

# چک کردن اینکه requirements نصب شده باشه
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

# اجرای سرور
python app.py