# 🚀 Démarrage simple de Netter ATS

## Méthode la plus simple

### 1. Démarrer tout en une commande
```bash
cd /Users/sam/ATS
./start.sh
```

C'est tout ! Le script va :
- ✅ Arrêter les processus existants
- ✅ Démarrer le backend sur http://127.0.0.1:8000
- ✅ Démarrer le frontend sur http://localhost:3000
- ✅ Vérifier que tout fonctionne

### 2. Arrêter les services
```bash
./stop.sh
```

## Méthode manuelle (si vous préférez)

### Terminal 1 - Backend
```bash
cd /Users/sam/ATS/netter-ats-backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Terminal 2 - Frontend
```bash
cd /Users/sam/ATS/netter-ats-frontend
npm run dev
```

## Vérification

Une fois démarré, ouvrez :
- **Frontend**: http://localhost:3000
- **Backend API**: http://127.0.0.1:8000/docs

## Problèmes courants

### Le backend ne démarre pas
- Vérifiez que le virtualenv existe : `ls netter-ats-backend/.venv`
- Si absent, créez-le : `cd netter-ats-backend && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`

### Le frontend ne démarre pas
- Vérifiez que node_modules existe : `ls netter-ats-frontend/node_modules`
- Si absent, installez : `cd netter-ats-frontend && npm install`

### Port déjà utilisé
- Backend (8000) : `lsof -ti:8000 | xargs kill -9`
- Frontend (3000) : `lsof -ti:3000 | xargs kill -9`

## Logs

- Backend : `tail -f /tmp/netter-backend.log`
- Frontend : `tail -f /tmp/netter-frontend.log`

