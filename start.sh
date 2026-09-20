#!/bin/bash
echo "Starting ExecBrief Services..."

# Ensure we're in the right directory
cd "$(dirname "$0")"

# Start FastAPI backend (Port 8000)
echo "Starting FastAPI Backend..."
source venv/bin/activate
uvicorn api:app --port 8000 &
BACKEND_PID=$!

# Start Vite React frontend (Port 5173)
echo "Starting React Frontend..."
cd frontend
npm run dev -- --host &
FRONTEND_PID=$!

# Trap Ctrl+C to kill both servers cleanly
trap "echo 'Shutting down services...'; kill $BACKEND_PID $FRONTEND_PID; exit 0" SIGINT SIGTERM

echo "========================================="
echo "✅ Frontend running at: http://localhost:5173"
echo "✅ Backend API running at: http://localhost:8000"
echo "Press Ctrl+C to stop both servers."
echo "========================================="

# Keep the script running to hold the trap
wait $FRONTEND_PID
wait $BACKEND_PID
