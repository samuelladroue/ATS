# Guide de test du backend ATS

## 1. Démarrer le serveur

```bash
cd netter-ats-backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

## 2. Tests avec curl

### Health check
```bash
curl http://127.0.0.1:8000/health
```

### Récupérer une offre d'emploi
```bash
curl http://127.0.0.1:8000/api/jobs/software-engineer
```

### Créer une nouvelle offre
```bash
curl -X POST http://127.0.0.1:8000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "slug":"data-scientist",
    "title":"Data Scientist",
    "description_md":"### Missions\n- Analyser des données\n- Créer des modèles ML",
    "location":"Lyon",
    "department":"Data",
    "status":"open"
  }'
```

### Postuler à une offre
```bash
curl -X POST http://127.0.0.1:8000/api/jobs/software-engineer/apply \
  -H "Content-Type: application/json" \
  -d '{
    "full_name":"Jean Martin",
    "email":"jean@example.com",
    "linkedin_url":"https://www.linkedin.com/in/jean"
  }'
```

### Tester une erreur (offre inexistante)
```bash
curl http://127.0.0.1:8000/api/jobs/offre-inexistante
```

### Tester une erreur (candidature avec email invalide)
```bash
curl -X POST http://127.0.0.1:8000/api/jobs/software-engineer/apply \
  -H "Content-Type: application/json" \
  -d '{
    "full_name":"Test",
    "email":"email-invalide",
    "linkedin_url":null
  }'
```

## 3. Interface Swagger (recommandé)

Ouvrez dans votre navigateur :
```
http://127.0.0.1:8000/docs
```

Vous pouvez tester toutes les routes directement depuis l'interface !

## 4. Alternative : Redoc

Documentation alternative :
```
http://127.0.0.1:8000/redoc
```

