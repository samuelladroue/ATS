# Note sur Tailwind CSS

## Problème rencontré

Le module `@nuxtjs/tailwindcss` causait une erreur 500 lors du démarrage :
```
[postcss] Cannot use 'import.meta' outside a module
```

## Solution temporaire

Tailwind a été **désactivé temporairement** pour permettre à l'application de fonctionner. Le CSS est maintenant géré via `assets/css/main.css` avec du CSS simple.

## Options pour réactiver Tailwind

### Option 1 : Utiliser Tailwind via CDN (rapide)
Ajouter dans `app.vue` ou un layout :
```html
<script src="https://cdn.tailwindcss.com"></script>
```

### Option 2 : Réinstaller @nuxtjs/tailwindcss
```bash
npm uninstall @nuxtjs/tailwindcss
npm install @nuxtjs/tailwindcss@latest --legacy-peer-deps
```

### Option 3 : Utiliser Tailwind CLI
Installer Tailwind en standalone et compiler le CSS manuellement.

## Classes Tailwind dans le code

Les composants Vue utilisent des classes Tailwind (ex: `bg-blue-600`, `rounded-lg`). Ces classes ne fonctionneront pas sans Tailwind activé.

**Solutions :**
1. Remplacer par du CSS inline dans les composants
2. Ajouter les styles dans `assets/css/main.css`
3. Réactiver Tailwind avec une des options ci-dessus

## Fichiers concernés

- `pages/jobs/[slug].vue` - Utilise beaucoup de classes Tailwind
- `pages/admin/jobs/index.vue` - Utilise des classes Tailwind
- `pages/admin/jobs/[id].vue` - Utilise des classes Tailwind
- `pages/index.vue` - Utilise des classes Tailwind
- `pages/apply/success.vue` - Utilise des classes Tailwind

