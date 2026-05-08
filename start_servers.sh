#!/bin/bash

# Banking Model Validation - Server Startup Script
# This script starts both backend and frontend servers

echo "=========================================="
echo "Banking Model Validation System"
echo "Server Startup Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if ports are already in use
echo "Checking ports..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}⚠️  Port 8000 is already in use. Killing existing process...${NC}"
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    sleep 1
fi

if lsof -Pi :3002 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}⚠️  Port 3002 is already in use. Killing existing process...${NC}"
    lsof -ti:3002 | xargs kill -9 2>/dev/null
    sleep 1
fi

echo -e "${GREEN}✓ Ports are clear${NC}"
echo ""

# Start Backend
echo "Starting Backend Server..."
cd backend
python main_simple.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "Waiting for backend to initialize..."
sleep 3

# Check if backend is running
if ps -p $BACKEND_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend started successfully (PID: $BACKEND_PID)${NC}"
    echo "  Backend URL: http://localhost:8000"
    echo "  API Docs: http://localhost:8000/docs"
    echo "  Logs: backend.log"
else
    echo -e "${RED}✗ Backend failed to start. Check backend.log for errors.${NC}"
    exit 1
fi

echo ""

# Start Frontend
echo "Starting Frontend Server..."
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
echo "Waiting for frontend to initialize..."
sleep 5

# Check if frontend is running
if ps -p $FRONTEND_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Frontend started successfully (PID: $FRONTEND_PID)${NC}"
    echo "  Frontend URL: http://localhost:3002"
    echo "  Logs: frontend.log"
else
    echo -e "${RED}✗ Frontend failed to start. Check frontend.log for errors.${NC}"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✓ All servers started successfully!${NC}"
echo "=========================================="
echo ""
echo "Access the application:"
echo "  🌐 Frontend: http://localhost:3002"
echo "  🔧 Backend API: http://localhost:8000"
echo "  📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "Server PIDs:"
echo "  Backend: $BACKEND_PID"
echo "  Frontend: $FRONTEND_PID"
echo ""
echo "To stop servers:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Logs:"
echo "  Backend: tail -f backend.log"
echo "  Frontend: tail -f frontend.log"
echo ""
echo "=========================================="
echo "Ready to test uploaded data integration!"
echo "=========================================="

# Made with Bob
