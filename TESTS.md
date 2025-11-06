# 🧪 Tests de l'ATS - Résultats

## ✅ Backend (FastAPI)

### Health Check
```bash
curl http://127.0.0.1:8000/health
```
**Résultat :** ✅ `{"status":"ok","db":true}`

### Liste des offres publiques
```bash
curl http://127.0.0.1:8000/api/jobs/public
```
**Résultat :** ✅ Retourne 4 offres (data-scientist, product-manager, marketing-intern, software-engineer)

### Détail d'une offre
```bash
curl http://127.0.0.1:8000/api/jobs/software-engineer
```
**Résultat :** ✅ Retourne les détails complets avec UUID, description, etc.

## ✅ Frontend (Nuxt)

### Page d'accueil
- **URL :** http://localhost:3000
- **Test :** Affiche la liste des offres publiques
- **Status :** ✅ En cours de démarrage

### Page détail offre
- **URL :** http://localhost:3000/jobs/software-engineer
- **Test :** Affiche l'offre + formulaire de candidature
- **Status :** À tester

### Page admin
- **URL :** http://localhost:3000/admin/jobs
- **Test :** Liste des offres + création
- **Status :** À tester

### Kanban candidatures
- **URL :** http://localhost:3000/admin/jobs/[id]
- **Test :** Vue kanban avec stages
- **Status :** À tester

## 📋 Checklist de tests

### Tests publics
- [x] Backend health check
- [x] API liste offres publiques
- [x] API détail offre
- [ ] Frontend page d'accueil
- [ ] Frontend page détail offre
- [ ] Formulaire de candidature
- [ ] Page de confirmation

### Tests admin
- [ ] Création d'une offre
- [ ] Liste des offres (admin)
- [ ] Vue candidatures par offre
- [ ] Déplacement candidature entre stages

## 🚀 Commandes utiles

### Backend
```bash
cd netter-ats-backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd netter-ats-frontend
npm run dev
```

### Tests API
```bash
# Liste offres publiques
curl http://127.0.0.1:8000/api/jobs/public

# Détail offre
curl http://127.0.0.1:8000/api/jobs/software-engineer

# Créer offre (admin)
curl -X POST http://127.0.0.1:8000/api/jobs \
  -H "X-API-Key: change-me-in-prod" \
  -H "Content-Type: application/json" \
  -d '{"slug":"test-job","title":"Test Job","status":"open"}'
```

