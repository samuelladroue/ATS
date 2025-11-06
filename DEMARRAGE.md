# 🚀 Guide de démarrage rapide - ATS Netter

## ✅ Services lancés

### Backend FastAPI
- **URL :** http://127.0.0.1:8000
- **Status :** ✅ En cours d'exécution
- **Health :** http://127.0.0.1:8000/health
- **Docs API :** http://127.0.0.1:8000/docs

### Frontend Nuxt
- **URL :** http://localhost:3000
- **Status :** ✅ En cours d'exécution
- **Port :** 3000

## 🧪 Tests rapides

### 1. Page d'accueil (Frontend)
Ouvrez dans votre navigateur :
```
http://localhost:3000
```
Vous devriez voir la liste des offres d'emploi.

### 2. Détail d'une offre
```
http://localhost:3000/jobs/software-engineer
```
Vous devriez voir :
- Les détails de l'offre
- Un formulaire de candidature

### 3. Postuler à une offre
1. Remplissez le formulaire sur la page de l'offre
2. Cliquez sur "Envoyer ma candidature"
3. Vous serez redirigé vers `/apply/success`

### 4. Administration
```
http://localhost:3000/admin/jobs
```
Vous pouvez :
- Voir toutes les offres
- Créer une nouvelle offre
- Cliquer sur "Voir candidatures" pour gérer les candidatures

### 5. Gérer les candidatures (Kanban)
```
http://localhost:3000/admin/jobs/[id]
```
Remplacez `[id]` par l'UUID d'une offre (visible dans l'URL de la page admin).

Vous verrez un kanban avec 6 colonnes :
- Nouvelle
- En revue
- Entretien
- Offre
- Embauché
- Refusé

Cliquez sur les boutons pour déplacer les candidatures entre les stages.

## 📋 URLs importantes

### Publiques
- **Accueil :** http://localhost:3000
- **Offre :** http://localhost:3000/jobs/[slug]
- **Confirmation :** http://localhost:3000/apply/success

### Admin
- **Liste offres :** http://localhost:3000/admin/jobs
- **Candidatures :** http://localhost:3000/admin/jobs/[id]

### API Backend
- **Health :** http://127.0.0.1:8000/health
- **Docs :** http://127.0.0.1:8000/docs
- **Offres publiques :** http://127.0.0.1:8000/api/jobs/public
- **Détail offre :** http://127.0.0.1:8000/api/jobs/[slug]

## 🔧 Commandes utiles

### Arrêter les services
```bash
# Trouver les processus
ps aux | grep -E "(uvicorn|nuxt)" | grep -v grep

# Arrêter (remplacez PID par le numéro du processus)
kill PID
```

### Relancer le backend
```bash
cd netter-ats-backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### Relancer le frontend
```bash
cd netter-ats-frontend
npm run dev
```

## 🐛 Dépannage

### Le frontend ne charge pas
1. Vérifiez que le backend tourne : `curl http://127.0.0.1:8000/health`
2. Vérifiez les logs du frontend dans le terminal
3. Vérifiez que le port 3000 n'est pas occupé : `lsof -ti:3000`

### Les routes admin ne fonctionnent pas
1. Vérifiez que `NUXT_ADMIN_API_KEY` dans `.env` du frontend correspond à `ADMIN_API_KEY` du backend
2. Vérifiez les logs du serveur Nuxt pour les erreurs

### Erreur CORS
Le backend a déjà CORS configuré pour `localhost:3000`. Si vous utilisez un autre port, ajoutez-le dans `netter-ats-backend/app/deps.py`.

## 📝 Notes

- Les deux services doivent tourner simultanément
- Le frontend appelle le backend sur `http://127.0.0.1:8000`
- Les routes admin passent par des server routes Nuxt (sécurité)
- Aucune authentification pour l'instant (pages admin non protégées)

