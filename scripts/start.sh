#!/bin/bash

# Factory Inventory Management System - Startup Script
# Starts both the backend (FastAPI) and frontend (Vue + Vite) servers.

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}Starting Factory Inventory Management System...${NC}\n"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Per-user runtime directory so PID/log files don't collide between users.
RUN_DIR="${TMPDIR:-/tmp}/inventory-mgmt-$(id -u)"
mkdir -p "$RUN_DIR"
BACKEND_PID_FILE="$RUN_DIR/backend.pid"
FRONTEND_PID_FILE="$RUN_DIR/frontend.pid"
BACKEND_LOG="$RUN_DIR/backend.log"
FRONTEND_LOG="$RUN_DIR/frontend.log"

BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
    echo -e "\n${YELLOW}Shutting down servers...${NC}"
    [ -n "$BACKEND_PID" ] && kill "$BACKEND_PID" 2>/dev/null || true
    [ -n "$FRONTEND_PID" ] && kill "$FRONTEND_PID" 2>/dev/null || true
    rm -f "$BACKEND_PID_FILE" "$FRONTEND_PID_FILE"
}
trap cleanup EXIT INT TERM

# Install backend dependencies if missing
if [ ! -d "$PROJECT_ROOT/server/.venv" ]; then
    echo -e "${YELLOW}Backend dependencies not found. Installing...${NC}"
    cd "$PROJECT_ROOT/server"
    uv venv
    uv sync
fi

# Install frontend dependencies if missing
if [ ! -d "$PROJECT_ROOT/client/node_modules" ]; then
    echo -e "${YELLOW}Frontend dependencies not found. Installing...${NC}"
    cd "$PROJECT_ROOT/client"
    npm install
fi

# Start backend server
echo -e "${GREEN}Starting backend server on http://localhost:8001${NC}"
cd "$PROJECT_ROOT/server"
uv run python3 main.py > "$BACKEND_LOG" 2>&1 &
BACKEND_PID=$!
echo "$BACKEND_PID" > "$BACKEND_PID_FILE"

# Wait for backend readiness (up to ~20s) instead of a blind sleep
echo -e "${YELLOW}Waiting for backend to be ready...${NC}"
for i in $(seq 1 40); do
    if curl -sf http://localhost:8001/ >/dev/null 2>&1; then
        break
    fi
    if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo -e "${RED}Backend exited during startup. See $BACKEND_LOG${NC}"
        exit 1
    fi
    sleep 0.5
done

# Start frontend server
echo -e "${GREEN}Starting frontend server on http://localhost:3000${NC}"
cd "$PROJECT_ROOT/client"
npm run dev > "$FRONTEND_LOG" 2>&1 &
FRONTEND_PID=$!
echo "$FRONTEND_PID" > "$FRONTEND_PID_FILE"

sleep 2

echo -e "\n${GREEN}✓ Application started successfully!${NC}"
echo -e "${BLUE}Frontend:${NC} http://localhost:3000"
echo -e "${BLUE}Backend API:${NC} http://localhost:8001"
echo -e "${BLUE}API Docs:${NC} http://localhost:8001/docs"
echo -e "\n${YELLOW}Logs:${NC}"
echo -e "  Backend: $BACKEND_LOG"
echo -e "  Frontend: $FRONTEND_LOG"
echo -e "\n${GREEN}Press Ctrl+C to stop all servers${NC}"

wait
