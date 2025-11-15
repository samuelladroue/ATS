#!/bin/bash

# Script pour démarrer le backend et le frontend de Netter ATS

echo "🚀 Démarrage de Netter ATS..."
echo ""

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fonction pour vérifier si un port est utilisé
check_port() {
    lsof -i :$1 > /dev/null 2>&1
}

# Arrêter les processus existants
echo "🛑 Arrêt des processus existants..."
pkill -f "uvicorn app.main:app" 2>/dev/null
pkill -f "nuxt dev" 2>/dev/null
sleep 2

# Démarrer le backend
echo ""
echo "${YELLOW}📦 Démarrage du backend (port 8000)...${NC}"
cd "$(dirname "$0")/netter-ats-backend"
if [ ! -d ".venv" ]; then
    echo "${RED}❌ Virtualenv non trouvé. Créez-le d'abord avec: python3 -m venv .venv${NC}"
    exit 1
fi

source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 > /tmp/netter-backend.log 2>&1 &
BACKEND_PID=$!

# Attendre que le backend démarre
echo "⏳ Attente du démarrage du backend..."
for i in {1..10}; do
    sleep 1
    if curl -s http://127.0.0.1:8000/health > /dev/null 2>&1; then
        echo "${GREEN}✅ Backend démarré sur http://127.0.0.1:8000${NC}"
        break
    fi
    if [ $i -eq 10 ]; then
        echo "${RED}❌ Le backend n'a pas démarré. Vérifiez les logs: tail -f /tmp/netter-backend.log${NC}"
        exit 1
    fi
done

# Démarrer le frontend
echo ""
echo "${YELLOW}🎨 Démarrage du frontend (port 3000)...${NC}"
cd "$(dirname "$0")/netter-ats-frontend"

# Vérifier si node_modules existe
if [ ! -d "node_modules" ]; then
    echo "${YELLOW}⚠️  node_modules non trouvé. Installation des dépendances...${NC}"
    npm install
fi

npm run dev > /tmp/netter-frontend.log 2>&1 &
FRONTEND_PID=$!

# Attendre que le frontend démarre
echo "⏳ Attente du démarrage du frontend..."
for i in {1..30}; do
    sleep 1
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo "${GREEN}✅ Frontend démarré sur http://localhost:3000${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "${YELLOW}⚠️  Le frontend prend du temps à démarrer. Vérifiez les logs: tail -f /tmp/netter-frontend.log${NC}"
    fi
done

echo ""
echo "${GREEN}✨ Netter ATS est en cours d'exécution !${NC}"
echo ""
echo "📍 Backend:  http://127.0.0.1:8000"
echo "📍 Frontend: http://localhost:3000"
echo "📍 API Docs: http://127.0.0.1:8000/docs"
echo ""
echo "📋 Logs backend:  tail -f /tmp/netter-backend.log"
echo "📋 Logs frontend: tail -f /tmp/netter-frontend.log"
echo ""
echo "Pour arrêter les services, utilisez: pkill -f 'uvicorn|nuxt'"
echo ""

# Garder le script actif pour voir les logs
wait

