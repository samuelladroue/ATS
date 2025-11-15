#!/bin/bash

# Script pour arrêter Netter ATS

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🛑 Arrêt de Netter ATS..."

# Arrêter via les PIDs sauvegardés
if [ -f /tmp/netter-backend.pid ]; then
    kill $(cat /tmp/netter-backend.pid) 2>/dev/null || true
    rm /tmp/netter-backend.pid
fi

if [ -f /tmp/netter-frontend.pid ]; then
    kill $(cat /tmp/netter-frontend.pid) 2>/dev/null || true
    rm /tmp/netter-frontend.pid
fi

# Arrêter par port
lsof -ti:8000 2>/dev/null | xargs kill -9 2>/dev/null || true
lsof -ti:3000 2>/dev/null | xargs kill -9 2>/dev/null || true

# Arrêter par processus
pkill -f "uvicorn app.main:app" 2>/dev/null || true
pkill -f "nuxt dev" 2>/dev/null || true

sleep 2

if pgrep -f "uvicorn|nuxt" > /dev/null; then
    echo -e "${YELLOW}⚠️  Certains processus sont encore en cours${NC}"
    echo "Pour forcer: pkill -9 -f 'uvicorn|nuxt'"
else
    echo -e "${GREEN}✅ Tous les services ont été arrêtés${NC}"
fi


