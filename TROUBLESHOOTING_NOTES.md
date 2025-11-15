# Résolution du problème 404 pour les notes

## Problème
Erreur 404 lors de l'appel à `/api/applications/{application_id}/notes`

## Solutions à vérifier

### 1. Vérifier que le backend est bien redémarré

Le backend FastAPI doit être redémarré après l'ajout des nouveaux endpoints.

**Vérification :**
```bash
# Arrêter le backend actuel (Ctrl+C)
# Puis redémarrer :
cd netter-ats-backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Vérifier que les endpoints sont bien enregistrés

Ouvrez http://127.0.0.1:8000/docs dans votre navigateur et vérifiez que vous voyez :
- `POST /api/applications/{application_id}/notes`
- `GET /api/applications/{application_id}/notes`

Si ces endpoints n'apparaissent pas, le backend n'a pas été redémarré ou il y a une erreur de syntaxe.

### 3. Vérifier que la migration SQL a été exécutée

La table `application_notes` doit exister dans Supabase. Exécutez le script `migration_add_notes_table.sql`.

### 4. Vérifier les logs

Regardez les logs du backend FastAPI et du serveur Nuxt pour voir les erreurs exactes.

## Test manuel de l'endpoint

Testez directement l'endpoint avec curl :

```bash
# Remplacer {application_id} et {admin_api_key} par de vraies valeurs
curl -X POST "http://127.0.0.1:8000/api/applications/{application_id}/notes" \
  -H "X-API-Key: {admin_api_key}" \
  -H "Content-Type: application/json" \
  -d '{
    "stage": "new",
    "report": "Test note",
    "rating": 3,
    "interviewer": "Test User"
  }'
```

Si cela retourne 404, le backend n'a pas les nouveaux endpoints.

