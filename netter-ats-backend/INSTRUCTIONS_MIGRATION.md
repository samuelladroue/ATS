# Instructions pour activer le système de notes

## ⚠️ IMPORTANT : Migration requise

Pour que les notes soient sauvegardées et persistent après actualisation, vous devez exécuter la migration SQL suivante dans votre base de données Supabase.

## Étapes

### 1. Ouvrir Supabase SQL Editor

1. Allez sur votre projet Supabase
2. Cliquez sur "SQL Editor" dans le menu de gauche
3. Cliquez sur "New query"

### 2. Exécuter la migration

Copiez-collez le contenu du fichier `migration_add_notes_table.sql` dans l'éditeur SQL et exécutez-le.

Le script va créer :
- La table `application_notes` pour stocker les notes
- Les index nécessaires pour les performances
- Le trigger pour mettre à jour `updated_at` automatiquement

### 3. Vérifier que la migration a fonctionné

Exécutez le script `check_notes_table.sql` pour vérifier que la table existe bien.

### 4. Redémarrer le backend (si nécessaire)

Si le backend était déjà en cours d'exécution, redémarrez-le pour qu'il reconnaisse la nouvelle table.

## Après la migration

Une fois la migration exécutée :
- ✅ Les notes seront sauvegardées dans la base de données
- ✅ Les notes persisteront après actualisation de la page
- ✅ Les notes seront visibles dans le kanban
- ✅ Les notes seront visibles dans le modal de détails

## En cas d'erreur

Si vous voyez une erreur indiquant que la table n'existe pas :
1. Vérifiez que vous avez bien exécuté la migration
2. Vérifiez que vous êtes connecté à la bonne base de données dans Supabase
3. Vérifiez les logs du backend pour plus de détails

