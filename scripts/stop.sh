#!/bin/bash

# Factory Inventory Management System - Stop Script
# Best-effort teardown — runs to completion even if individual kills fail.

YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${YELLOW}Stopping Factory Inventory Management System...${NC}\n"

RUN_DIR="${TMPDIR:-/tmp}/inventory-mgmt-$(id -u)"
BACKEND_PID_FILE="$RUN_DIR/backend.pid"
FRONTEND_PID_FILE="$RUN_DIR/frontend.pid"

stop_pid() {
    local pid_file="$1"
    local label="$2"
    if [ -f "$pid_file" ]; then
        local pid
        pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            echo -e "${YELLOW}Stopping $label server (PID: $pid)${NC}"
            kill "$pid" 2>/dev/null || true
        fi
        rm -f "$pid_file"
    fi
}

stop_pid "$BACKEND_PID_FILE" "backend"
stop_pid "$FRONTEND_PID_FILE" "frontend"

# Fallback: kill any remaining processes on the ports
echo -e "${YELLOW}Cleaning up any remaining processes...${NC}"

BACKEND_PIDS=$(lsof -ti:8001 2>/dev/null || true)
if [ -n "$BACKEND_PIDS" ]; then
    echo "$BACKEND_PIDS" | xargs kill 2>/dev/null || true
fi

FRONTEND_PIDS=$(lsof -ti:3000 2>/dev/null || true)
if [ -n "$FRONTEND_PIDS" ]; then
    echo "$FRONTEND_PIDS" | xargs kill 2>/dev/null || true
fi

rm -f "$RUN_DIR/backend.log" "$RUN_DIR/frontend.log"

echo -e "\n${GREEN}✓ All servers stopped successfully!${NC}"
