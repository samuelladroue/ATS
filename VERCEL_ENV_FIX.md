# 🔧 Correction de l'erreur Vercel

## ❌ Problème actuel

L'erreur `Failed to fetch` indique que `NUXT_PUBLIC_API_BASE` contient encore le placeholder :
```
https://votre-backend-deployé.com
```

## ✅ Solution : Mettre à jour la variable sur Vercel

### Si votre backend n'est PAS encore déployé

**Option A : Tester localement**
1. Sur Vercel, modifiez `NUXT_PUBLIC_API_BASE` :
   ```
   http://127.0.0.1:8000
   ```
   ⚠️ **Note :** Cela ne fonctionnera que si vous accédez au frontend depuis votre machine locale.

**Option B : Déployer le backend d'abord**
- Déployez votre backend FastAPI (Railway, Render, Cloud Run, etc.)
- Puis mettez l'URL de production dans `NUXT_PUBLIC_API_BASE`

### Si votre backend EST déployé

1. Allez sur Vercel Dashboard → Settings → Environment Variables
2. Modifiez `NUXT_PUBLIC_API_BASE` avec l'URL réelle de votre backend :
   ```
   https://votre-backend-reel.com
   ```
   (Remplacez par l'URL réelle de votre backend déployé)
3. Redéployez le frontend

## 🚀 Déployer le backend (si pas encore fait)

### Option 1 : Railway (simple et gratuit)

1. Allez sur https://railway.app
2. Créez un nouveau projet
3. Connectez votre repo GitHub
4. Sélectionnez le dossier `netter-ats-backend`
5. Railway détecte automatiquement Python/FastAPI
6. Ajoutez les variables d'environnement :
   - `DATABASE_URL` (votre URL Supabase)
   - `ADMIN_API_KEY`
7. Railway génère une URL automatiquement (ex: `https://votre-projet.railway.app`)

### Option 2 : Render (gratuit aussi)

1. Allez sur https://render.com
2. Créez un nouveau "Web Service"
3. Connectez votre repo GitHub
4. Configuration :
   - Build Command : `pip install -r requirements.txt`
   - Start Command : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Ajoutez les variables d'environnement
6. Render génère une URL (ex: `https://votre-projet.onrender.com`)

### Option 3 : Google Cloud Run

1. Utilisez `gcloud` CLI
2. Build et déployez avec Cloud Build
3. URL générée automatiquement

## 📝 Après déploiement du backend

1. **Copiez l'URL du backend** (ex: `https://votre-api.railway.app`)
2. **Sur Vercel**, mettez à jour `NUXT_PUBLIC_API_BASE` :
   ```
   https://votre-api.railway.app
   ```
3. **Redéployez** le frontend
4. **Mettez à jour CORS** dans le backend pour autoriser votre domaine Vercel

## 🔐 Mise à jour CORS backend

Dans `netter-ats-backend/app/deps.py`, ajoutez votre domaine Vercel :

```python
origins = [
    "http://localhost:3000",
    "https://votre-projet.vercel.app",  # Ajoutez votre domaine Vercel
    "https://*.vercel.app",  # Ou autoriser tous les sous-domaines
    # ...
]
```

Puis redéployez le backend.

