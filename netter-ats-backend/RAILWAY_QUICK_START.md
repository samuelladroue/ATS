# 🚀 Déploiement Railway - Guide Rapide

## ✅ Étape 1 : Créer le projet

1. Sur Railway, cliquez sur **"New Project"**
2. Sélectionnez **"Deploy from GitHub repo"**
3. Autorisez Railway à accéder à vos repos si demandé
4. Sélectionnez le repo : **`samuelladroue/ATS`**

---

## ✅ Étape 2 : Configurer le service

1. Railway va créer un service automatiquement
2. **Cliquez sur le service** créé
3. Allez dans **Settings** (⚙️ en haut à droite)
4. Dans **"Root Directory"**, entrez :
   ```
   netter-ats-backend
   ```
5. Railway détectera automatiquement :
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

## ✅ Étape 3 : Ajouter les variables d'environnement

1. Dans le service, allez dans l'onglet **"Variables"** (ou cliquez sur **"+ New"** → **"Variable"**)
2. Ajoutez ces **2 variables** :

### Variable 1 : `DATABASE_URL`
- **Key** : `DATABASE_URL`
- **Value** : 
  ```
  postgresql://postgres.xmzblszpxxdirhknreut:QAGv4pNqgnmGCtTw@aws-1-eu-north-1.pooler.supabase.com:5432/postgres?sslmode=require
  ```

### Variable 2 : `ADMIN_API_KEY`
- **Key** : `ADMIN_API_KEY`
- **Value** : 
  ```
  change-me-in-prod
  ```

3. Cliquez sur **"Add"** pour chaque variable

---

## ✅ Étape 4 : Déployer

1. Railway va **automatiquement** détecter les changements et déployer
2. Allez dans l'onglet **"Deployments"** pour voir les logs
3. Attendez 2-3 minutes que le build se termine
4. Cherchez dans les logs : `Application startup complete`

---

## ✅ Étape 5 : Récupérer l'URL

1. Une fois déployé, Railway génère automatiquement une **URL publique**
2. Allez dans **Settings** → **"Generate Domain"** si l'URL n'apparaît pas
3. L'URL ressemble à : `https://votre-projet-production.up.railway.app`
4. **Copiez cette URL** 📋

---

## ✅ Étape 6 : Tester

1. Testez l'endpoint de santé :
   ```
   https://votre-url-railway.app/health
   ```
   Devrait retourner : `{"status": "ok", "db": true}`

2. Si ça fonctionne, ✅ **le backend est déployé !**

---

## ✅ Étape 7 : Mettre à jour Vercel

1. **Sur Vercel** → Votre projet frontend
2. **Settings** → **Environment Variables**
3. Modifiez `NUXT_PUBLIC_API_BASE` :
   ```
   https://votre-url-railway.app
   ```
   (Remplacez par votre URL Railway réelle)

4. **Redéployez** le frontend sur Vercel

---

## 🐛 Dépannage

### Erreur : "No module named 'app'"
- Vérifiez que **Root Directory** est bien `netter-ats-backend`

### Erreur : "Database connection failed"
- Vérifiez que `DATABASE_URL` est correct dans les variables
- Vérifiez que le mot de passe Supabase est correct

### Erreur : "Port already in use"
- Railway gère automatiquement le port avec `$PORT`, normalement pas de problème

### Build échoue
- Vérifiez les logs dans l'onglet **"Deployments"**
- Vérifiez que `requirements.txt` est présent dans `netter-ats-backend/`

