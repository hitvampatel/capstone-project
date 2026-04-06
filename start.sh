#!/bin/bash
echo "============================================"
echo " Karnavati University Event Registration"
echo "============================================"
echo ""
echo "Installing Flask if needed..."
pip3 install flask --quiet 2>/dev/null || pip install flask --quiet
echo ""
echo "Starting server..."
echo "Open browser at: http://localhost:5000"
echo "Admin panel at:  http://localhost:5000/admin"
echo ""
echo "Press Ctrl+C to stop."
echo ""
cd "$(dirname "$0")"
python3 app.py || python app.py
