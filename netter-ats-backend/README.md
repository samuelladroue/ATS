# Netter ATS Backend

Backend FastAPI pour un système de suivi des candidatures (Applicant Tracking System) connecté à PostgreSQL sur Supabase.

## 🚀 Installation

### 1. Configuration de l'environnement

Assurez-vous que le fichier `.env` contient vos identifiants Supabase :

```env
DATABASE_URL="postgresql://postgres:TON_MOT_DE_PASSE@db.xmzblszpxxdirhknreut.supabase.co:5432/postgres?sslmode=require"
ADMIN_API_KEY="change-me-in-prod"
```

**⚠️ Important :** Remplacez `TON_MOT_DE_PASSE` par votre vrai mot de passe Supabase dans le fichier `.env`.

### 2. Initialisation de la base de données

Exécutez le script SQL `init_db.sql` sur votre base Supabase pour créer les tables :

1. Connectez-vous à votre dashboard Supabase
2. Allez dans "SQL Editor"
3. Copiez-collez le contenu de `init_db.sql`
4. Exécutez le script

### 3. Installation des dépendances

```bash
cd netter-ats-backend
source .venv/bin/activate  # macOS/Linux
# ou: .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## 🧪 Tests

### Tester la connexion à la base de données

```bash
python test_db.py
```

Ce script vérifie que la connexion PostgreSQL fonctionne en exécutant `SELECT now();`.

### Démarrer le serveur FastAPI

```bash
uvicorn app.main:app --reload --port 8000
```

Le serveur sera accessible sur :
- API : http://127.0.0.1:8000
- Documentation Swagger : http://127.0.0.1:8000/docs
- Documentation ReDoc : http://127.0.0.1:8000/redoc

## 📡 Routes API

### Routes publiques (sans authentification)

- `GET /health` - Vérifie le statut de l'API et de la base de données
- `GET /api/jobs/{slug}` - Récupère une offre d'emploi par son slug
- `POST /api/jobs/{slug}/apply` - Postule à une offre d'emploi

### Routes admin (nécessitent l'API key)

Toutes les routes admin nécessitent le header `X-API-Key` avec la valeur définie dans `ADMIN_API_KEY`.

- `POST /api/jobs` - Crée une nouvelle offre d'emploi
- `GET /api/jobs` - Liste toutes les offres d'emploi
- `GET /api/jobs/{job_id}/applications` - Liste les candidatures pour une offre
- `PATCH /api/applications/{application_id}` - Met à jour une candidature (stage, notes)

## 🔐 Authentification Admin

Pour utiliser les routes admin, ajoutez le header suivant à vos requêtes :

```
X-API-Key: change-me-in-prod
```

**⚠️ Important :** Changez la valeur de `ADMIN_API_KEY` dans `.env` en production !

## 📝 Exemples d'utilisation

### Créer une offre (admin)

```bash
curl -X POST http://127.0.0.1:8000/api/jobs \
  -H "Content-Type: application/json" \
  -H "X-API-Key: change-me-in-prod" \
  -d '{
    "slug": "software-engineer",
    "title": "Software Engineer",
    "description_md": "## Missions\n- Développer des APIs\n- Travailler avec FastAPI",
    "location": "Paris",
    "department": "Engineering",
    "status": "open"
  }'
```

### Postuler à une offre (public)

```bash
curl -X POST http://127.0.0.1:8000/api/jobs/software-engineer/apply \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Alice Dupont",
    "email": "alice@example.com",
    "linkedin_url": "https://www.linkedin.com/in/alice"
  }'
```

### Lister les candidatures (admin)

```bash
curl http://127.0.0.1:8000/api/jobs/1/applications \
  -H "X-API-Key: change-me-in-prod"
```

## 🗄️ Structure de la base de données

- **jobs** : Offres d'emploi
- **candidates** : Candidats (UPSERT par email)
- **applications** : Candidatures (lien entre jobs et candidates)

Voir `init_db.sql` pour le schéma complet.

## 🔧 Développement

Le serveur utilise le mode `--reload` pour recharger automatiquement les modifications.

Pour arrêter le serveur, utilisez `Ctrl+C` dans le terminal.

