#!/bin/bash

# Script pour démarrer et maintenir Netter ATS automatiquement

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

BACKEND_DIR="/Users/sam/ATS/netter-ats-backend"
FRONTEND_DIR="/Users/sam/ATS/netter-ats-frontend"
BACKEND_PORT=8000
FRONTEND_PORT=3000

# Fonction pour tuer les processus sur un port
kill_port() {
    local port=$1
    lsof -ti:$port 2>/dev/null | xargs kill -9 2>/dev/null || true
}

# Fonction pour vérifier si un port est utilisé
check_port() {
    lsof -i :$1 > /dev/null 2>&1
}

# Fonction pour démarrer le backend
start_backend() {
    echo -e "${YELLOW}📦 Démarrage du backend...${NC}"
    cd "$BACKEND_DIR"
    if [ ! -d ".venv" ]; then
        echo -e "${RED}❌ Virtualenv non trouvé${NC}"
        return 1
    fi
    
    source .venv/bin/activate
    nohup uvicorn app.main:app --reload --host 127.0.0.1 --port $BACKEND_PORT > /tmp/netter-backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > /tmp/netter-backend.pid
    
    # Attendre que le backend démarre
    for i in {1..15}; do
        sleep 1
        if curl -s http://127.0.0.1:$BACKEND_PORT/health > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Backend démarré (PID: $BACKEND_PID)${NC}"
            return 0
        fi
    done
    
    echo -e "${RED}❌ Le backend n'a pas démarré${NC}"
    return 1
}

# Fonction pour démarrer le frontend
start_frontend() {
    echo -e "${YELLOW}🎨 Démarrage du frontend...${NC}"
    cd "$FRONTEND_DIR"
    
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}⚠️  Installation des dépendances...${NC}"
        npm install
    fi
    
    nohup npm run dev > /tmp/netter-frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > /tmp/netter-frontend.pid
    
    # Attendre que le frontend démarre
    for i in {1..30}; do
        sleep 1
        if curl -s http://localhost:$FRONTEND_PORT > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Frontend démarré (PID: $FRONTEND_PID)${NC}"
            return 0
        fi
    done
    
    echo -e "${YELLOW}⚠️  Le frontend prend du temps à démarrer${NC}"
    return 0
}

# Fonction pour vérifier et redémarrer si nécessaire
check_and_restart() {
    # Vérifier le backend
    if ! check_port $BACKEND_PORT; then
        echo -e "${YELLOW}⚠️  Backend arrêté, redémarrage...${NC}"
        kill_port $BACKEND_PORT
        sleep 2
        start_backend
    fi
    
    # Vérifier le frontend
    if ! check_port $FRONTEND_PORT; then
        echo -e "${YELLOW}⚠️  Frontend arrêté, redémarrage...${NC}"
        kill_port $FRONTEND_PORT
        sleep 2
        start_frontend
    fi
}

# Nettoyer les processus existants
echo -e "${YELLOW}🛑 Arrêt des processus existants...${NC}"
kill_port $BACKEND_PORT
kill_port $FRONTEND_PORT
pkill -f "uvicorn app.main:app" 2>/dev/null || true
pkill -f "nuxt dev" 2>/dev/null || true
sleep 2

# Démarrer les services
start_backend
start_frontend

echo ""
echo -e "${GREEN}✨ Netter ATS est en cours d'exécution !${NC}"
echo ""
echo "📍 Backend:  http://127.0.0.1:$BACKEND_PORT"
echo "📍 Frontend: http://localhost:$FRONTEND_PORT"
echo "📍 API Docs: http://127.0.0.1:$BACKEND_PORT/docs"
echo ""
echo "📋 Logs backend:  tail -f /tmp/netter-backend.log"
echo "📋 Logs frontend: tail -f /tmp/netter-frontend.log"
echo ""
echo "💡 Les services redémarreront automatiquement s'ils s'arrêtent"
echo "   Pour arrêter: ./stop_ats.sh"
echo ""

# Mode surveillance (optionnel - décommentez pour activer)
# while true; do
#     sleep 30
#     check_and_restart
# done


