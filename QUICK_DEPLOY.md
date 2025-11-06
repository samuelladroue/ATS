# ⚡ Déploiement Vercel - Guide ultra-rapide

## 🚀 En 3 étapes

### 1. Préparer (si pas déjà fait)

```bash
cd netter-ats-frontend
git init
git add .
git commit -m "Ready for Vercel"
# Push vers GitHub/GitLab/Bitbucket
```

### 2. Déployer sur Vercel

**Option A : Interface web (le plus simple)**
1. Allez sur https://vercel.com/new
2. Importez votre repo Git
3. Vercel détecte automatiquement Nuxt.js
4. Cliquez sur "Deploy"

**Option B : CLI**
```bash
npm install -g vercel
vercel login
cd netter-ats-frontend
vercel --prod
```

### 3. Configurer les variables

Dans Vercel Dashboard → Settings → Environment Variables :

```
NUXT_PUBLIC_API_BASE = https://votre-backend.com
NUXT_ADMIN_API_KEY = votre-clé-secrète
```

Puis redéployez.

## ✅ C'est tout !

Votre app sera sur `https://votre-projet.vercel.app`

