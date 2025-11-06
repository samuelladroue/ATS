# 🚀 Guide de déploiement sur Vercel

## Prérequis

1. Un compte Vercel (gratuit) : https://vercel.com
2. Le projet Git initialisé (optionnel mais recommandé)

## Méthode 1 : Déploiement via l'interface Vercel (Recommandé)

### Étape 1 : Préparer le projet

```bash
cd netter-ats-frontend

# Vérifier que le build fonctionne localement
npm run build
```

### Étape 2 : Connecter le projet à Vercel

1. Allez sur https://vercel.com
2. Cliquez sur "Add New..." → "Project"
3. Importez votre repository Git (GitHub, GitLab, Bitbucket)
   - Ou utilisez "Import Git Repository" si vous avez déjà un repo
   - Ou utilisez "Deploy" pour uploader directement

### Étape 3 : Configurer le projet

**Settings du projet :**
- **Framework Preset** : Nuxt.js (détecté automatiquement)
- **Root Directory** : `netter-ats-frontend` (si votre repo contient plusieurs dossiers)
- **Build Command** : `npm run build` (ou laisser par défaut)
- **Output Directory** : `.output/public` (ou laisser par défaut)

### Étape 4 : Configurer les variables d'environnement

Dans les **Settings** → **Environment Variables**, ajoutez :

```
NUXT_PUBLIC_API_BASE=https://votre-api-backend.com
NUXT_ADMIN_API_KEY=votre-clé-admin-secrète
```

**Important :**
- `NUXT_PUBLIC_API_BASE` : URL de votre backend FastAPI déployé (ex: `https://api.example.com`)
- `NUXT_ADMIN_API_KEY` : La même clé que dans votre backend (server-only, ne sera pas exposée au client)

### Étape 5 : Déployer

Cliquez sur "Deploy" et attendez la fin du build.

## Méthode 2 : Déploiement via CLI Vercel

### Étape 1 : Installer Vercel CLI

```bash
npm install -g vercel
```

### Étape 2 : Se connecter

```bash
vercel login
```

### Étape 3 : Déployer

```bash
cd netter-ats-frontend

# Premier déploiement (prévisualisation)
vercel

# Déploiement en production
vercel --prod
```

### Étape 4 : Configurer les variables d'environnement

```bash
# Ajouter les variables d'environnement
vercel env add NUXT_PUBLIC_API_BASE
# Entrez la valeur : https://votre-api-backend.com

vercel env add NUXT_ADMIN_API_KEY
# Entrez la valeur : votre-clé-admin-secrète

# Redéployer pour appliquer les variables
vercel --prod
```

## Configuration des variables d'environnement

### Variables requises

| Variable | Description | Exemple |
|----------|-------------|---------|
| `NUXT_PUBLIC_API_BASE` | URL de l'API FastAPI (exposée au client) | `https://api.example.com` |
| `NUXT_ADMIN_API_KEY` | Clé API admin (server-only) | `change-me-in-prod` |

### Où les configurer

1. **Interface Vercel** : Settings → Environment Variables
2. **CLI** : `vercel env add NOM_VARIABLE`

### Environnements

Vous pouvez définir des variables différentes pour :
- **Production** : `vercel --prod`
- **Preview** : `vercel` (déploiements de branches)
- **Development** : Variables locales dans `.env`

## Vérification après déploiement

1. **Test de la page d'accueil** : `https://votre-projet.vercel.app`
2. **Test des routes publiques** : Vérifier que les offres s'affichent
3. **Test des routes admin** : Vérifier que les server routes fonctionnent

## Problèmes courants

### Erreur : "Cannot find module"
```bash
# Solution : Vérifier que toutes les dépendances sont dans package.json
npm install --legacy-peer-deps
```

### Erreur : Variables d'environnement non définies
- Vérifiez que les variables sont bien configurées dans Vercel
- Redéployez après avoir ajouté les variables

### Erreur : API calls échouent
- Vérifiez que `NUXT_PUBLIC_API_BASE` pointe vers votre backend déployé
- Vérifiez les CORS sur le backend pour autoriser le domaine Vercel

## Mise à jour du backend pour CORS

Si votre backend est déployé, ajoutez le domaine Vercel dans `app/deps.py` :

```python
origins = [
    "http://localhost:3000",
    "https://votre-projet.vercel.app",  # Ajoutez votre domaine Vercel
    # ...
]
```

## Commandes utiles

```bash
# Voir les logs de déploiement
vercel logs

# Voir les variables d'environnement
vercel env ls

# Ouvrir le dashboard
vercel dashboard
```

## URLs après déploiement

- **Production** : `https://votre-projet.vercel.app`
- **Preview** : `https://votre-projet-git-branch.vercel.app`

