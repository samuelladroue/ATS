# 📦 Mettre le projet sur GitHub

## ✅ Étape 1 : Créer le repository GitHub

1. Allez sur https://github.com/new
2. **Repository name** : `netter-ats-frontend` (ou le nom de votre choix)
3. **Description** : "Frontend Nuxt 3 pour le système ATS Netter"
4. **Visibility** : Public ou Private (selon votre préférence)
5. **NE PAS** cocher "Initialize with README" (on a déjà un README)
6. Cliquez sur **"Create repository"**

## ✅ Étape 2 : Connecter et push

Git est déjà initialisé et le premier commit est fait. Il suffit de connecter au repo GitHub :

```bash
cd netter-ats-frontend

# Ajouter le remote (remplacez par votre URL GitHub)
git remote add origin https://github.com/VOTRE-USERNAME/netter-ats-frontend.git

# Push vers GitHub
git branch -M main
git push -u origin main
```

**Note :** Remplacez `VOTRE-USERNAME` par votre nom d'utilisateur GitHub.

## 🔐 Variables d'environnement sur GitHub

Si vous voulez utiliser GitHub Actions ou garder les secrets :

1. Allez sur votre repo GitHub
2. **Settings** → **Secrets and variables** → **Actions**
3. Ajoutez les secrets (pour CI/CD si besoin) :
   - `NUXT_PUBLIC_API_BASE`
   - `NUXT_ADMIN_API_KEY`

**Important :** Ne commitez JAMAIS le fichier `.env` (déjà dans `.gitignore`)

## 📋 Fichiers inclus dans le repo

✅ **Inclus :**
- Code source (pages, components, server routes)
- Configuration (nuxt.config.ts, vercel.json)
- Documentation (README.md, DEPLOY*.md)
- package.json, tsconfig.json

❌ **Exclus (via .gitignore) :**
- `node_modules/`
- `.nuxt/`, `.output/`
- `.env`, `.env.local`
- Logs et fichiers temporaires

## 🚀 Après le push

Une fois sur GitHub, vous pouvez :
1. Déployer directement depuis GitHub sur Vercel
2. Partager le code avec votre équipe
3. Utiliser GitHub Actions pour CI/CD

## 📝 Commandes utiles

```bash
# Voir l'état
git status

# Ajouter des changements
git add .
git commit -m "Description des changements"

# Push vers GitHub
git push

# Voir les remotes
git remote -v
```

