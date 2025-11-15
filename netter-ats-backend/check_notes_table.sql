-- Script pour vérifier si la table application_notes existe
-- Exécutez ce script dans Supabase SQL Editor pour vérifier

-- Vérifier si la table existe
SELECT EXISTS (
   SELECT FROM information_schema.tables 
   WHERE table_schema = 'public' 
   AND table_name = 'application_notes'
) AS table_exists;

-- Si la table existe, compter les notes
SELECT COUNT(*) as total_notes FROM application_notes;

-- Voir la structure de la table si elle existe
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'application_notes'
ORDER BY ordinal_position;

