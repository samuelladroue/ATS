# Configuration de l'Assistant IA

L'assistant IA permet de créer des offres d'emploi en langage naturel via une chatbox dans l'interface admin.

## Installation

1. Installer la dépendance OpenAI :
```bash
pip install openai
```

Ou réinstaller toutes les dépendances :
```bash
pip install -r requirements.txt
```

## Configuration

Ajoutez votre clé API OpenAI dans le fichier `.env` du backend :

```env
OPENAI_API_KEY=sk-votre-cle-api-openai
```

## Utilisation

1. Démarrez le backend et le frontend
2. Accédez à n'importe quelle page admin (`/admin/jobs`, `/admin/candidates`, etc.)
3. Cliquez sur le bouton "Assistant IA" en bas à droite
4. Tapez une commande en langage naturel, par exemple :
   - "Crée-moi une offre de designer à 100k$ à Paris"
   - "Je veux créer une offre de développeur full-stack remote"
   - "Crée une offre de Product Manager à San Francisco"

L'assistant va :
1. Comprendre votre demande
2. Extraire les informations (titre, description, lieu, département, salaire)
3. Générer une description professionnelle en markdown
4. Créer l'offre dans la base de données
5. Vous afficher une confirmation avec un lien vers l'offre créée

## Modèle utilisé

- **Modèle** : `gpt-4o-mini` (rapide et économique)
- **Temperature** : 0.3 (pour des réponses cohérentes)
- **Format** : JSON structuré

## Exemples de commandes

- "Crée-moi une offre de designer UX/UI à 80k€ à Lyon"
- "Je veux une offre de développeur Python senior remote à 120k$"
- "Crée une offre de Product Manager à Paris, département Product, 90k€"
- "Fais-moi une offre de Data Scientist à Londres, 100k£"

## Notes

- L'assistant génère automatiquement un slug à partir du titre
- Si le slug existe déjà, vous devrez reformuler avec un titre différent
- La description est générée en markdown et peut être modifiée après création
- Toutes les offres créées sont par défaut au statut "open"

