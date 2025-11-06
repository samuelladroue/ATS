# Guide de démarrage rapide - Netter ATS Frontend

## 🚀 Installation et démarrage

### 1. Installer les dépendances

```bash
cd netter-ats-frontend
npm install --legacy-peer-deps
```

### 2. Configurer l'environnement

Le fichier `.env` est déjà créé avec les valeurs par défaut. Vérifiez qu'il correspond à votre backend :

```env
NUXT_PUBLIC_API_BASE="http://127.0.0.1:8000"
NUXT_ADMIN_API_KEY="change-me-in-prod"
```

**Important :** Assurez-vous que `NUXT_ADMIN_API_KEY` correspond à la valeur de `ADMIN_API_KEY` dans le `.env` du backend.

### 3. Démarrer le serveur de développement

```bash
npm run dev
```

Le frontend sera accessible sur **http://localhost:3000**

## 🧪 Tests du flow complet

### Test 1 : Voir les offres publiques

1. Ouvrir http://localhost:3000
2. Vérifier que la liste des offres s'affiche
3. Cliquer sur une offre pour voir les détails

### Test 2 : Postuler à une offre

1. Aller sur http://localhost:3000/jobs/software-engineer (ou une autre offre)
2. Remplir le formulaire :
   - Nom complet : "Jean Dupont"
   - Email : "jean@example.com"
   - LinkedIn : "https://www.linkedin.com/in/jean" (optionnel)
3. Cliquer sur "Envoyer ma candidature"
4. Vérifier la redirection vers `/apply/success`

### Test 3 : Créer une offre (admin)

1. Aller sur http://localhost:3000/admin/jobs
2. Remplir le formulaire "Créer une nouvelle offre" :
   - Slug : "frontend-developer"
   - Titre : "Frontend Developer"
   - Description : "## Missions\n- Développer des interfaces\n- Travailler avec Vue.js"
   - Localisation : "Paris"
   - Département : "Engineering"
   - Statut : "Ouverte"
3. Cliquer sur "Créer l'offre"
4. Vérifier que l'offre apparaît dans la liste

### Test 4 : Gérer les candidatures (admin)

1. Sur la page `/admin/jobs`, cliquer sur "Voir candidatures" pour une offre
2. Vérifier le kanban avec 6 colonnes (stages)
3. Vérifier que les candidatures sont dans la colonne "Nouvelle"
4. Cliquer sur un bouton "→ Entretien" pour déplacer une candidature
5. Vérifier que la candidature se déplace dans la colonne "Entretien"
6. Rafraîchir la page pour vérifier que le changement est persisté

## 📋 Checklist de vérification

- [ ] Le backend FastAPI tourne sur http://127.0.0.1:8000
- [ ] La base de données est connectée (`GET /health` retourne `{"status":"ok","db":true}`)
- [ ] Le frontend Nuxt tourne sur http://localhost:3000
- [ ] Les variables d'environnement sont correctement configurées
- [ ] La clé admin est la même dans le backend et le frontend

## 🔧 Dépannage

### Le frontend ne charge pas les offres

- Vérifiez que le backend tourne : `curl http://127.0.0.1:8000/health`
- Vérifiez la console du navigateur pour les erreurs
- Vérifiez que `NUXT_PUBLIC_API_BASE` est correct dans `.env`

### Les routes admin ne fonctionnent pas

- Vérifiez que `NUXT_ADMIN_API_KEY` correspond à `ADMIN_API_KEY` du backend
- Vérifiez les logs du serveur Nuxt pour les erreurs
- Vérifiez que les server routes sont bien créées dans `server/api/admin/`

### Erreur CORS

- Le backend a déjà CORS configuré pour `localhost:3000`
- Si vous utilisez un autre port, ajoutez-le dans `app/deps.py` du backend

## 📝 Notes

- Les routes admin passent par des **server routes Nuxt** pour ne pas exposer la clé API au client
- Les routes publiques appellent directement l'API FastAPI
- L'upload de CV n'est pas implémenté (placeholder dans le formulaire)
- Aucune authentification pour l'instant (pages admin non protégées)

