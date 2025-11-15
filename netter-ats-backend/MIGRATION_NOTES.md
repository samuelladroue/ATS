# Migration : Table des notes de candidature

## Étape 1 : Exécuter la migration SQL

Exécutez le script SQL suivant sur votre base de données Supabase :

```bash
# Via psql ou l'interface Supabase SQL Editor
psql -h your-db-host -U your-user -d your-database -f migration_add_notes_table.sql
```

Ou copiez-collez le contenu de `migration_add_notes_table.sql` dans l'éditeur SQL de Supabase.

## Étape 2 : Redémarrer le backend

Après avoir exécuté la migration, redémarrez le backend FastAPI pour que les nouveaux endpoints soient disponibles.

## Nouveaux endpoints

- `POST /api/applications/{application_id}/notes` - Créer une note
- `GET /api/applications/{application_id}/notes` - Récupérer toutes les notes d'une candidature

## Structure de la table

La table `application_notes` stocke :
- `id` : Identifiant unique de la note
- `application_id` : Référence à la candidature
- `stage` : Stage de la candidature (new, review, interview, offer, rejected, hired)
- `report` : Compte-rendu de l'interviewer
- `rating` : Note sur 4 (1-4)
- `interviewer` : Nom de l'interviewer (optionnel)
- `created_at` : Date de création
- `updated_at` : Date de mise à jour

