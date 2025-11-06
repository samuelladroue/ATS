# 🚀 Déploiement Vercel - Méthode simple (sans CLI)

## ✅ Étape 1 : Préparer le projet Git (optionnel mais recommandé)

```bash
cd netter-ats-frontend

# Si pas déjà fait, initialiser Git
git init
git add .
git commit -m "Ready for Vercel deployment"

# Créer un repo sur GitHub et push (ou utiliser GitLab/Bitbucket)
# git remote add origin https://github.com/votre-username/netter-ats-frontend.git
# git push -u origin main
```

**Note :** Vous pouvez aussi déployer directement depuis votre dossier local sans Git.

## ✅ Étape 2 : Déployer via l'interface Vercel

### Option A : Avec Git (recommandé)

1. **Allez sur** https://vercel.com/new
2. **Connectez votre compte** (GitHub/GitLab/Bitbucket)
3. **Importez votre repository** contenant `netter-ats-frontend`
4. **Configuration automatique** :
   - Vercel détecte automatiquement Nuxt.js
   - Framework : Nuxt.js
   - Root Directory : `netter-ats-frontend` (si votre repo est à la racine)
   - Build Command : `npm run build` (par défaut)
   - Output Directory : `.output/public` (par défaut)
   - Install Command : `npm install --legacy-peer-deps` (déjà dans vercel.json)

### Option B : Sans Git (upload direct)

1. **Allez sur** https://vercel.com/new
2. **Cliquez sur "Deploy"** (sans importer de repo)
3. **Glissez-déposez** le dossier `netter-ats-frontend` ou utilisez "Browse"
4. Vercel détecte automatiquement Nuxt.js

## ✅ Étape 3 : Configurer les variables d'environnement

**AVANT de cliquer sur "Deploy"**, allez dans **"Environment Variables"** et ajoutez :

| Variable | Valeur | Environnements |
|----------|--------|----------------|
| `NUXT_PUBLIC_API_BASE` | `https://votre-backend.com` | Production, Preview, Development |
| `NUXT_ADMIN_API_KEY` | `votre-clé-secrète` | Production, Preview, Development |

**Important :**
- Pour le moment, mettez `http://127.0.0.1:8000` pour `NUXT_PUBLIC_API_BASE` si votre backend n'est pas encore déployé
- Vous pourrez changer cette valeur plus tard dans les Settings

## ✅ Étape 4 : Déployer

Cliquez sur **"Deploy"** et attendez 1-2 minutes.

## ✅ Étape 5 : Vérifier

Une fois déployé, vous obtiendrez une URL comme :
- `https://netter-ats-frontend.vercel.app`

Testez :
- ✅ Page d'accueil
- ✅ Page offre
- ✅ Admin

## 🔄 Mettre à jour les variables plus tard

1. Allez sur votre projet dans Vercel Dashboard
2. **Settings** → **Environment Variables**
3. Modifiez `NUXT_PUBLIC_API_BASE` avec l'URL de votre backend déployé
4. **Redeploy** (ou attendez le prochain push Git)

## 📝 Alternative : CLI sans sudo

Si vous voulez utiliser le CLI sans sudo :

```bash
# Utiliser npx (pas besoin d'installer globalement)
npx vercel

# Ou installer localement dans le projet
cd netter-ats-frontend
npm install vercel --save-dev
npx vercel --prod
```

## 🎉 C'est tout !

Votre app sera en ligne sur Vercel !

