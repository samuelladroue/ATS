# ⚠️ IMPORTANT : Redémarrer le backend

## Problème
L'erreur 404 indique que le backend FastAPI n'a **pas été redémarré** après l'ajout des nouveaux endpoints pour les notes.

## Solution : Redémarrer le backend

### Option 1 : Utiliser le script (recommandé)
```bash
cd netter-ats-backend
./restart_backend.sh
```

### Option 2 : Redémarrer manuellement
1. **Arrêter le backend actuel** :
   - Trouvez le terminal où le backend tourne
   - Appuyez sur `Ctrl+C` pour l'arrêter

2. **Redémarrer le backend** :
   ```bash
   cd netter-ats-backend
   source .venv/bin/activate
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

## Vérification

Après le redémarrage, vérifiez que les endpoints sont disponibles :

1. **Ouvrez** http://127.0.0.1:8000/docs dans votre navigateur
2. **Cherchez** les endpoints suivants :
   - `POST /api/applications/{application_id}/notes` ✅
   - `GET /api/applications/{application_id}/notes` ✅

Si ces endpoints n'apparaissent **PAS**, il y a un problème dans le code.

## Après le redémarrage

Une fois le backend redémarré :
- ✅ Le bouton "Enregistrer la note" fonctionnera
- ✅ Les notes seront sauvegardées dans la base de données
- ✅ Les notes persisteront après actualisation

## Note importante

N'oubliez pas d'exécuter la **migration SQL** dans Supabase (`migration_add_notes_table.sql`) pour créer la table `application_notes` si ce n'est pas déjà fait !

