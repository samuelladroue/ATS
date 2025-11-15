#!/bin/bash
# Script pour redémarrer le backend avec les nouveaux endpoints

echo "🔄 Redémarrage du backend FastAPI..."

# Activer l'environnement virtuel
source .venv/bin/activate

# Vérifier que les endpoints sont bien dans le code
echo "📋 Vérification des endpoints..."
if grep -q "@app.post.*notes" app/main.py && grep -q "@app.get.*notes" app/main.py; then
    echo "✅ Les endpoints notes sont présents dans le code"
else
    echo "❌ ERREUR: Les endpoints notes ne sont pas trouvés dans app/main.py"
    exit 1
fi

# Démarrer le serveur
echo "🚀 Démarrage du serveur sur http://127.0.0.1:8000"
echo "📖 Documentation disponible sur http://127.0.0.1:8000/docs"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

