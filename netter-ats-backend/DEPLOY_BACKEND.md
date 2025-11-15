# 🚀 Déploiement du Backend FastAPI

## Option 1 : Railway (Recommandé - Simple et gratuit)

### Étapes

1. **Allez sur https://railway.app** et créez un compte (gratuit)

2. **Créez un nouveau projet** → "New Project"

3. **Connectez votre repo GitHub**
   - Sélectionnez le repo `ATS`
   - Railway détectera automatiquement Python

4. **Configurez le service**
   - **Root Directory** : `netter-ats-backend`
   - **Start Command** : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Railway détecte automatiquement le `Procfile`

5. **Ajoutez les variables d'environnement** dans Railway :
   - `DATABASE_URL` : Votre URL Supabase (avec le mot de passe)
   - `ADMIN_API_KEY` : `change-me-in-prod` (ou une clé sécurisée)

6. **Déployez**
   - Railway déploie automatiquement
   - Vous obtiendrez une URL comme : `https://votre-projet.railway.app`

7. **Mettez à jour CORS** dans `app/deps.py` :
   ```python
   origins = [
       "http://localhost:3000",
       "https://votre-frontend.vercel.app",  # Votre domaine Vercel
       "https://*.vercel.app",
       "*",  # Pour dev uniquement
   ]
   ```

8. **Sur Vercel**, mettez à jour `NUXT_PUBLIC_API_BASE` avec l'URL Railway

---

## Option 2 : Render (Gratuit aussi)

### Étapes

1. **Allez sur https://render.com** et créez un compte

2. **Créez un nouveau "Web Service"**

3. **Connectez votre repo GitHub**
   - Sélectionnez le repo `ATS`

4. **Configuration** :
   - **Name** : `netter-ats-backend`
   - **Root Directory** : `netter-ats-backend`
   - **Environment** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

5. **Variables d'environnement** :
   - `DATABASE_URL`
   - `ADMIN_API_KEY`

6. **Déployez**
   - Render génère une URL : `https://votre-projet.onrender.com`

7. **Mettez à jour CORS et Vercel** (comme pour Railway)

---

## Option 3 : Google Cloud Run

### Prérequis
- `gcloud` CLI installé
- Projet Google Cloud créé

### Étapes

1. **Build l'image Docker** (ou utilisez Cloud Build) :
   ```bash
   gcloud builds submit --tag gcr.io/VOTRE-PROJET/netter-ats-backend
   ```

2. **Déployez sur Cloud Run** :
   ```bash
   gcloud run deploy netter-ats-backend \
     --image gcr.io/VOTRE-PROJET/netter-ats-backend \
     --platform managed \
     --region europe-west1 \
     --allow-unauthenticated \
     --set-env-vars DATABASE_URL="...",ADMIN_API_KEY="..."
   ```

3. **Récupérez l'URL** et mettez à jour Vercel

---

## ⚠️ Important après déploiement

1. **Testez l'endpoint de santé** :
   ```
   https://votre-backend.com/health
   ```
   Devrait retourner : `{"status": "ok", "db": true}`

2. **Mettez à jour CORS** dans le backend pour autoriser votre domaine Vercel

3. **Mettez à jour `NUXT_PUBLIC_API_BASE`** sur Vercel avec l'URL du backend

4. **Redéployez le frontend** sur Vercel

---

## 🔐 Sécurité

- **Changez `ADMIN_API_KEY`** en production avec une clé forte
- **Ne commitez JAMAIS** le fichier `.env` (déjà dans `.gitignore`)
- **Restreignez CORS** en production (enlevez `"*"`)

