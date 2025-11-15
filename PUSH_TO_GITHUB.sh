#!/bin/bash
# Script pour push vers GitHub

echo "📦 Préparation du push vers GitHub..."
echo ""

# Vérifier si un remote existe déjà
if git remote | grep -q origin; then
    echo "⚠️  Remote 'origin' existe déjà"
    echo "Pour le changer : git remote set-url origin VOTRE_URL"
    git remote -v
else
    echo "✅ Pas de remote configuré"
    echo ""
    echo "📋 Pour connecter à GitHub :"
    echo "   1. Créez un repo sur https://github.com/new"
    echo "   2. Exécutez :"
    echo "      git remote add origin https://github.com/VOTRE-USERNAME/netter-ats-frontend.git"
    echo "      git push -u origin main"
fi

echo ""
echo "📊 État actuel :"
git status --short | head -10

