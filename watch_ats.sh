#!/bin/bash

# Script de surveillance qui redémarre automatiquement les services s'ils s'arrêtent

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

BACKEND_DIR="/Users/sam/ATS/netter-ats-backend"
FRONTEND_DIR="/Users/sam/ATS/netter-ats-frontend"

check_port() {
    lsof -i :$1 > /dev/null 2>&1
}

start_backend() {
    cd "$BACKEND_DIR"
    source .venv/bin/activate
    nohup uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 > /tmp/netter-backend.log 2>&1 &
    echo $! > /tmp/netter-backend.pid
}

start_frontend() {
    cd "$FRONTEND_DIR"
    nohup npm run dev > /tmp/netter-frontend.log 2>&1 &
    echo $! > /tmp/netter-frontend.pid
}

echo -e "${GREEN}👀 Surveillance active - Les services redémarreront automatiquement${NC}"
echo "Appuyez sur Ctrl+C pour arrêter"
echo ""

while true; do
    sleep 10
    
    if ! check_port 8000; then
        echo -e "${YELLOW}[$(date +%H:%M:%S)] Backend arrêté, redémarrage...${NC}"
        start_backend
        sleep 5
    fi
    
    if ! check_port 3000; then
        echo -e "${YELLOW}[$(date +%H:%M:%S)] Frontend arrêté, redémarrage...${NC}"
        start_frontend
        sleep 5
    fi
done


