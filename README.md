# Netter ATS

Système de suivi des candidatures (ATS) complet avec frontend Nuxt 3 et backend FastAPI.

## 📦 Structure du projet

```
ATS/
├── netter-ats-frontend/    # Frontend Nuxt 3
├── netter-ats-backend/     # Backend FastAPI
├── start_ats.sh            # Script de démarrage (front + back)
├── stop_ats.sh              # Script d'arrêt
└── watch_ats.sh             # Script de monitoring
```

## 🚀 Démarrage rapide

### Prérequis

- Node.js 18+ et npm
- Python 3.11+
- PostgreSQL (Supabase recommandé)

### Installation et démarrage

1. **Backend** :
```bash
cd netter-ats-backend
python -m venv .venv
source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. **Frontend** :
```bash
cd netter-ats-frontend
npm install --legacy-peer-deps
```

3. **Démarrer les deux services** :
```bash
# Depuis la racine du projet
./start_ats.sh
```

Ou manuellement :
- Backend : `cd netter-ats-backend && source .venv/bin/activate && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
- Frontend : `cd netter-ats-frontend && npm run dev`

L'application sera accessible sur :
- Frontend : http://localhost:3000
- Backend API : http://localhost:8000
- API Docs : http://localhost:8000/docs

## ⚙️ Configuration

### Backend

Créez un fichier `.env` dans `netter-ats-backend/` :

```env
DATABASE_URL=postgresql://user:password@host:port/dbname
ADMIN_API_KEY=change-me-in-prod
RESEND_API_KEY=re_xxxxxxxxx
RESEND_FROM_EMAIL=onboarding@resend.dev
RESEND_FROM_NAME=Netter ATS
```

### Frontend

Créez un fichier `.env` dans `netter-ats-frontend/` :

```env
NUXT_PUBLIC_API_BASE=http://127.0.0.1:8000
NUXT_ADMIN_API_KEY=change-me-in-prod
```

**Important :** 
- `NUXT_PUBLIC_API_BASE` est exposé au client (pour les appels API publics)
- `NUXT_ADMIN_API_KEY` est **server-only** et ne doit jamais être exposé au client
- Les routes admin passent par les server routes Nuxt qui injectent la clé côté serveur

## 📄 Pages

### Publiques
- `/` - Liste des offres d'emploi ouvertes
- `/jobs/[slug]` - Détail d'une offre + formulaire de candidature
- `/apply/success` - Page de confirmation après candidature

### Admin
- `/admin/jobs` - Liste des offres + création/suppression
- `/admin/jobs/[id]` - Vue kanban des candidatures par stage
- `/admin/candidates` - Liste de tous les candidats avec leurs candidatures
- `/admin/email-templates` - Gestion des templates d'email

## ✨ Fonctionnalités

### Gestion des candidatures
- ✅ Création et gestion des offres d'emploi
- ✅ Suivi des candidatures par stage (New applicants, Screening interview, Technical interview, Offer sent, Hired, Refused)
- ✅ Vue kanban pour gérer les candidatures
- ✅ Notes par candidature
- ✅ Suppression de candidats et d'offres

### Module Email
- ✅ Envoi d'emails via Resend
- ✅ Templates d'email avec variables (ex: `{{candidate_name}}`)
- ✅ Historique des emails par candidat
- ✅ Gestion complète des templates (CRUD)

### Interface Admin
- ✅ Table des candidats avec colonnes Offre/Stage séparées
- ✅ Navigation admin unifiée
- ✅ Design responsive avec Tailwind CSS

## 🔐 Sécurité

- Les routes admin utilisent des **server routes Nuxt** qui injectent `X-API-Key` côté serveur
- La clé admin n'est jamais exposée au client
- Les appels publics (liste offres, candidature) appellent directement l'API FastAPI
- Protection des routes admin avec vérification de la clé API

## 🗄️ Base de données

Le schéma de base de données inclut :
- `jobs` - Offres d'emploi
- `candidates` - Candidats
- `applications` - Candidatures (relation entre jobs et candidates)
- `email_templates` - Templates d'email
- `emails` - Historique des emails envoyés

Voir `netter-ats-backend/init_db.sql` pour le schéma complet.

## 🚢 Déploiement

### Backend (Railway)
Voir `netter-ats-backend/DEPLOY_RAILWAY_STEP_BY_STEP.md`

### Frontend (Vercel)
Voir `netter-ats-frontend/DEPLOY_VERCEL.md`

## 🛠️ Stack

### Backend
- **Framework** : FastAPI
- **Base de données** : PostgreSQL (via Supabase)
- **ORM** : psycopg (async)
- **Email** : Resend
- **Python** : 3.11+

### Frontend
- **Framework** : Nuxt 3
- **UI** : Tailwind CSS
- **Composables** : @vueuse/nuxt
- **TypeScript** : Oui

## 📝 Scripts utiles

- `./start_ats.sh` - Démarre frontend et backend
- `./stop_ats.sh` - Arrête les services
- `./watch_ats.sh` - Surveille les logs des deux services

## 📚 Documentation

- `NETTER_ATS_FEATURES.md` - Liste complète des fonctionnalités
- `netter-ats-backend/README.md` - Documentation backend
- `netter-ats-frontend/README.md` - Documentation frontend

## 📄 Licence

Propriétaire - Netter AI
