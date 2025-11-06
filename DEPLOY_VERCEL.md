# 🚀 Déploiement sur Vercel - Guide rapide

## ✅ Prérequis

- ✅ Le build fonctionne localement (`npm run build`)
- ✅ Un compte Vercel (gratuit) : https://vercel.com/signup

## 🎯 Méthode rapide : Interface Vercel (Recommandé)

### 1. Préparer le projet Git (si pas déjà fait)

```bash
cd netter-ats-frontend

# Initialiser Git si nécessaire
git init
git add .
git commit -m "Initial commit"

# Créer un repo sur GitHub/GitLab/Bitbucket et push
git remote add origin https://github.com/votre-username/netter-ats-frontend.git
git push -u origin main
```

### 2. Déployer sur Vercel

1. **Allez sur** https://vercel.com/new
2. **Importez votre repository** (GitHub/GitLab/Bitbucket)
   - Ou cliquez sur "Deploy" pour uploader directement
3. **Configuration automatique** :
   - Framework : Nuxt.js (détecté automatiquement)
   - Root Directory : `netter-ats-frontend` (si repo à la racine)
   - Build Command : `npm run build` (par défaut)
   - Output Directory : `.output/public` (par défaut)
   - Install Command : `npm install --legacy-peer-deps` (déjà configuré dans `vercel.json`)

### 3. Configurer les variables d'environnement

Dans **Settings** → **Environment Variables**, ajoutez :

| Variable | Valeur | Environnement |
|----------|--------|----------------|
| `NUXT_PUBLIC_API_BASE` | `https://votre-api-backend.com` | Production, Preview, Development |
| `NUXT_ADMIN_API_KEY` | `votre-clé-admin-secrète` | Production, Preview, Development |

**Important :**
- Remplacez `https://votre-api-backend.com` par l'URL réelle de votre backend FastAPI déployé
- `NUXT_ADMIN_API_KEY` doit correspondre à `ADMIN_API_KEY` de votre backend

### 4. Déployer

Cliquez sur **"Deploy"** et attendez 1-2 minutes.

### 5. Vérifier

Une fois déployé, vous obtiendrez une URL comme : `https://netter-ats-frontend.vercel.app`

Testez :
- ✅ Page d'accueil : `https://votre-projet.vercel.app`
- ✅ Page offre : `https://votre-projet.vercel.app/jobs/software-engineer`
- ✅ Admin : `https://votre-projet.vercel.app/admin/jobs`

---

## 🛠️ Méthode alternative : CLI Vercel

### 1. Installer Vercel CLI

```bash
npm install -g vercel
```

### 2. Se connecter

```bash
vercel login
```

### 3. Déployer

```bash
cd netter-ats-frontend

# Premier déploiement (prévisualisation)
vercel

# Déploiement en production
vercel --prod
```

### 4. Configurer les variables d'environnement

```bash
# Ajouter les variables
vercel env add NUXT_PUBLIC_API_BASE production
# Entrez : https://votre-api-backend.com

vercel env add NUXT_ADMIN_API_KEY production
# Entrez : votre-clé-admin-secrète

# Redéployer
vercel --prod
```

---

## ⚙️ Configuration importante

### Variables d'environnement requises

**Production :**
```
NUXT_PUBLIC_API_BASE=https://votre-backend-deployé.com
NUXT_ADMIN_API_KEY=votre-clé-secrète
```

**Développement local :**
```
NUXT_PUBLIC_API_BASE=http://127.0.0.1:8000
NUXT_ADMIN_API_KEY=change-me-in-prod
```

### Mise à jour du backend pour CORS

Si votre backend est déployé, ajoutez votre domaine Vercel dans `netter-ats-backend/app/deps.py` :

```python
origins = [
    "http://localhost:3000",
    "https://votre-projet.vercel.app",  # Ajoutez votre domaine Vercel
    "https://*.vercel.app",  # Ou autoriser tous les sous-domaines Vercel
    # ...
]
```

---

## 🔍 Vérification après déploiement

1. **Page d'accueil** : Vérifier que les offres s'affichent
2. **Page offre** : Tester le formulaire de candidature
3. **Admin** : Vérifier que les routes admin fonctionnent
4. **Console navigateur** : Vérifier qu'il n'y a pas d'erreurs CORS

---

## 🐛 Dépannage

### Erreur : Build failed
```bash
# Vérifier localement
cd netter-ats-frontend
npm run build
```

### Erreur : Variables d'environnement non définies
- Vérifiez dans Vercel Dashboard → Settings → Environment Variables
- Redéployez après avoir ajouté les variables

### Erreur : API calls échouent
- Vérifiez que `NUXT_PUBLIC_API_BASE` est correct
- Vérifiez les CORS sur le backend
- Vérifiez les logs Vercel : `vercel logs`

---

## 📝 Commandes utiles

```bash
# Voir les logs
vercel logs

# Voir les variables d'environnement
vercel env ls

# Ouvrir le dashboard
vercel dashboard

# Redéployer
vercel --prod
```

---

## 🎉 C'est tout !

Une fois déployé, votre ATS sera accessible publiquement sur Vercel !

**Prochaines étapes :**
1. Déployer le backend FastAPI (Cloud Run, Railway, Render, etc.)
2. Mettre à jour `NUXT_PUBLIC_API_BASE` avec l'URL du backend déployé
3. Redéployer le frontend

