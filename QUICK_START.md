# 🚀 Démarrage rapide

## Commandes à exécuter

### 1. Installer les dépendances (déjà fait)
```bash
cd netter-ats-frontend
npm install --legacy-peer-deps
```

### 2. Vérifier la configuration

Assurez-vous que le fichier `.env` contient :
```env
NUXT_PUBLIC_API_BASE="http://127.0.0.1:8000"
NUXT_ADMIN_API_KEY="change-me-in-prod"
```

**Important :** `NUXT_ADMIN_API_KEY` doit correspondre à `ADMIN_API_KEY` dans le `.env` du backend.

### 3. Démarrer le serveur de développement

```bash
npm run dev
```

Le frontend sera accessible sur **http://localhost:3000**

## ✅ Tests rapides

### Test 1 : Page d'accueil
- Ouvrir http://localhost:3000
- Vérifier que les offres s'affichent

### Test 2 : Postuler
- Cliquer sur une offre
- Remplir le formulaire et soumettre
- Vérifier la redirection vers `/apply/success`

### Test 3 : Admin - Créer une offre
- Aller sur http://localhost:3000/admin/jobs
- Créer une nouvelle offre
- Vérifier qu'elle apparaît dans la liste

### Test 4 : Admin - Gérer les candidatures
- Cliquer sur "Voir candidatures" pour une offre
- Déplacer une candidature d'un stage à un autre
- Vérifier que le changement est sauvegardé

## 📋 Prérequis

- Le backend FastAPI doit tourner sur http://127.0.0.1:8000
- La base de données doit être connectée
- Node.js 18+ installé

