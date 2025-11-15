#!/bin/bash

# Script pour arrêter le backend et le frontend

echo "🛑 Arrêt de Netter ATS..."

pkill -f "uvicorn app.main:app" 2>/dev/null
pkill -f "nuxt dev" 2>/dev/null

sleep 2

if pgrep -f "uvicorn|nuxt" > /dev/null; then
    echo "⚠️  Certains processus sont encore en cours d'exécution"
    echo "Pour forcer l'arrêt: pkill -9 -f 'uvicorn|nuxt'"
else
    echo "✅ Tous les services ont été arrêtés"
fi

