-- Migration: Créer une table pour les notes de candidature
-- À exécuter sur votre base Supabase

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

