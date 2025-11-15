# 🗄️ Exécuter la migration SQL pour créer la table application_notes

## Étape par étape

### 1. Ouvrir Supabase SQL Editor

1. Allez sur https://supabase.com
2. Connectez-vous à votre projet
3. Dans le menu de gauche, cliquez sur **"SQL Editor"**
4. Cliquez sur **"New query"**

### 2. Copier le script de migration

Copiez-collez le contenu suivant dans l'éditeur SQL :

```sql
-- Table pour les notes de candidature
CREATE TABLE IF NOT EXISTS application_notes (
    id SERIAL PRIMARY KEY,
    application_id UUID NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
    stage VARCHAR(50) NOT NULL CHECK (stage IN ('new', 'review', 'interview', 'offer', 'rejected', 'hired')),
    report TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 4),
    interviewer VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Index pour améliorer les performances
CREATE INDEX IF NOT EXISTS idx_application_notes_application_id ON application_notes(application_id);
CREATE INDEX IF NOT EXISTS idx_application_notes_stage ON application_notes(stage);
CREATE INDEX IF NOT EXISTS idx_application_notes_created_at ON application_notes(created_at);

-- Trigger pour mettre à jour updated_at automatiquement
CREATE TRIGGER update_application_notes_updated_at BEFORE UPDATE ON application_notes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### 3. Exécuter la migration

1. Cliquez sur le bouton **"Run"** (ou appuyez sur `Ctrl+Enter`)
2. Vous devriez voir un message de succès : "Success. No rows returned"

### 4. Vérifier que la table existe

Exécutez cette requête pour vérifier :

```sql
SELECT EXISTS (
   SELECT FROM information_schema.tables 
   WHERE table_schema = 'public' 
   AND table_name = 'application_notes'
) AS table_exists;
```

Vous devriez voir `table_exists: true`

### 5. Tester dans l'application

Après avoir exécuté la migration :
- ✅ Le bouton "Enregistrer la note" fonctionnera
- ✅ Les notes seront sauvegardées dans la base de données
- ✅ Les notes persisteront après actualisation

## En cas d'erreur

Si vous voyez une erreur concernant la fonction `update_updated_at_column`, cela signifie que cette fonction n'existe pas encore. Dans ce cas, exécutez d'abord ce script :

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';
```

Puis réessayez la migration.

