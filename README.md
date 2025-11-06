# Netter ATS Frontend

Frontend Nuxt 3 pour le système de suivi des candidatures (ATS) Netter.

## 🚀 Démarrage rapide

### Installation

```bash
npm install --legacy-peer-deps
```

### Développement

```bash
npm run dev
```

L'application sera accessible sur http://localhost:3000

### Build

```bash
npm run build
```

## ⚙️ Configuration

Créez un fichier `.env` à la racine :

```env
NUXT_PUBLIC_API_BASE="http://127.0.0.1:8000"
NUXT_ADMIN_API_KEY="change-me-in-prod"
```

**Important :** 
- `NUXT_PUBLIC_API_BASE` est exposé au client (pour les appels API publics)
- `NUXT_ADMIN_API_KEY` est **server-only** et ne doit jamais être exposé au client
- Les routes admin passent par les server routes Nuxt qui injectent la clé côté serveur

## 📄 Pages

### Publiques
- `/` - Liste des offres d'emploi ouvertes
- `/jobs/[slug]` - Détail d'une offre + formulaire de candidature
- `/apply/success` - Page de confirmation après candidature

### Admin
- `/admin/jobs` - Liste des offres + création
- `/admin/jobs/[id]` - Vue kanban des candidatures par stage

## 🔐 Sécurité

- Les routes admin utilisent des **server routes Nuxt** qui injectent `X-API-Key` côté serveur
- La clé admin n'est jamais exposée au client
- Les appels publics (liste offres, candidature) appellent directement l'API FastAPI

## 🚢 Déploiement

Voir `DEPLOY_SIMPLE.md` pour le déploiement sur Vercel.

## 🛠️ Stack

- **Framework** : Nuxt 3
- **UI** : Tailwind CSS (via CDN)
- **Composables** : @vueuse/nuxt
- **TypeScript** : Oui

## 📝 Notes

- Tailwind CSS est chargé via CDN (voir `app.vue`)
- Les classes Tailwind sont utilisées dans tous les composants
- Aucune authentification pour l'instant (pages admin non protégées)
