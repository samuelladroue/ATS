# 🚀 Déploiement Backend sur Railway - Guide Étape par Étape

## ✅ Prérequis

- ✅ Compte GitHub avec le repo `ATS` (déjà fait)
- ✅ Compte Railway (gratuit) : https://railway.app
- ✅ URL Supabase avec mot de passe (déjà configuré)

---

## 📋 Étape 1 : Créer un compte Railway

1. Allez sur **https://railway.app**
2. Cliquez sur **"Start a New Project"** ou **"Login"**
3. Connectez-vous avec **GitHub** (recommandé)

---

## 📋 Étape 2 : Créer un nouveau projet

1. Dans le dashboard Railway, cliquez sur **"New Project"**
2. Sélectionnez **"Deploy from GitHub repo"**
3. Autorisez Railway à accéder à vos repos GitHub si demandé
4. Sélectionnez le repo **`samuelladroue/ATS`**

---

## 📋 Étape 3 : Configurer le service

Railway va détecter automatiquement Python, mais il faut configurer le dossier :

1. **Cliquez sur le service** créé (ou "Add Service" → "GitHub Repo")
2. Allez dans **Settings** (⚙️)
3. Dans **"Root Directory"**, entrez :
   ```
   netter-ats-backend
   ```
4. Railway détectera automatiquement :
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : Détecté depuis le `Procfile` : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

## 📋 Étape 4 : Ajouter les variables d'environnement

1. Dans le service, allez dans l'onglet **"Variables"**
2. Cliquez sur **"+ New Variable"**
3. Ajoutez ces **2 variables** :

### Variable 1 : `DATABASE_URL`
- **Key** : `DATABASE_URL`
- **Value** : Votre URL Supabase complète :
  ```
  postgresql://postgres.xmzblszpxxdirhknreut:QAGv4pNqgnmGCtTw@aws-1-eu-north-1.pooler.supabase.com:5432/postgres?sslmode=require
  ```
  ⚠️ **Remplacez le mot de passe si nécessaire**

### Variable 2 : `ADMIN_API_KEY`
- **Key** : `ADMIN_API_KEY`
- **Value** : `change-me-in-prod`
  ⚠️ **Changez cette valeur en production avec une clé forte !**

---

## 📋 Étape 5 : Déployer

1. Railway va **automatiquement** :
   - Détecter les changements
   - Builder l'application
   - Déployer le service

2. **Attendez** que le build soit terminé (2-3 minutes)
   - Vous verrez les logs en temps réel
   - Cherchez : `Application startup complete`

3. Une fois déployé, Railway génère automatiquement une **URL publique**
   - Exemple : `https://votre-projet-production.up.railway.app`
   - Cliquez sur **"Settings"** → **"Generate Domain"** si besoin

---

## 📋 Étape 6 : Tester le déploiement

1. **Testez l'endpoint de santé** :
   ```
   https://votre-projet-production.up.railway.app/health
   ```
   Devrait retourner :
   ```json
   {"status": "ok", "db": true}
   ```

2. **Testez une route publique** :
   ```
   https://votre-projet-production.up.railway.app/api/jobs/public
   ```
   Devrait retourner une liste vide `[]` (ou vos offres si vous en avez créé)

---

## 📋 Étape 7 : Mettre à jour Vercel

1. **Copiez l'URL Railway** (ex: `https://votre-projet-production.up.railway.app`)

2. **Sur Vercel** :
   - Allez dans votre projet frontend
   - **Settings** → **Environment Variables**
   - Modifiez `NUXT_PUBLIC_API_BASE` :
     ```
     https://votre-projet-production.up.railway.app
     ```
     (Remplacez par votre URL Railway réelle)

3. **Redéployez le frontend** :
   - Allez dans **Deployments**
   - Cliquez sur **"Redeploy"** sur le dernier déploiement
   - Ou faites un commit/push pour déclencher un nouveau déploiement

---

## 📋 Étape 8 : Mettre à jour CORS (si nécessaire)

Le CORS autorise déjà `"*"` en dev, donc ça devrait fonctionner. Si vous voulez restreindre :

1. Dans `netter-ats-backend/app/deps.py`, modifiez :
   ```python
   origins = [
       "http://localhost:3000",
       "https://votre-frontend.vercel.app",  # Votre domaine Vercel
       "https://*.vercel.app",  # Tous les sous-domaines Vercel
   ]
   ```

2. **Committez et pushez** :
   ```bash
   cd /Users/sam/ATS
   git add netter-ats-backend/app/deps.py
   git commit -m "Update CORS for production"
   git push
   ```

3. Railway redéploiera automatiquement

---

## ✅ Vérification finale

1. ✅ Backend déployé sur Railway
2. ✅ URL Railway copiée
3. ✅ `NUXT_PUBLIC_API_BASE` mis à jour sur Vercel
4. ✅ Frontend redéployé
5. ✅ Test de `/health` fonctionne
6. ✅ Frontend peut appeler le backend

---

## 🐛 Dépannage

### Erreur : "Application failed to respond"
- Vérifiez les logs Railway
- Vérifiez que `DATABASE_URL` est correct
- Vérifiez que le port est bien `$PORT`

### Erreur : "Database connection failed"
- Vérifiez que `DATABASE_URL` est correct dans Railway
- Vérifiez que Supabase accepte les connexions externes
- Testez la connexion avec `test_db.py` en local

### Erreur CORS sur le frontend
- Vérifiez que l'URL dans `NUXT_PUBLIC_API_BASE` est correcte
- Vérifiez que CORS autorise votre domaine Vercel

---

## 📞 Support

- **Railway Docs** : https://docs.railway.app
- **Railway Discord** : https://discord.gg/railway

