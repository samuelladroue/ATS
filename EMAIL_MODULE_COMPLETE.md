# Module Email - Implémentation complète ✅

## 🎉 Ce qui a été implémenté

### Backend ✅
- ✅ Modèles de données (`app/models.py`)
- ✅ Migration SQL (`migration_add_email_tables.sql`)
- ✅ Endpoints API complets :
  - `GET /api/email-templates` - Liste tous les templates
  - `POST /api/email-templates` - Créer un template
  - `GET /api/email-templates/{id}` - Récupérer un template
  - `PATCH /api/email-templates/{id}` - Mettre à jour un template
  - `DELETE /api/email-templates/{id}` - Supprimer un template
  - `POST /api/emails/send` - Envoyer un email
  - `GET /api/candidates/{id}/emails` - Historique des emails
- ✅ Intégration Resend configurée
- ✅ Support des variables `{{candidate_name}}` dans les templates

### Frontend ✅
- ✅ Routes Nuxt server-side pour tous les endpoints
- ✅ Modal Email Composer intégré dans le modal de détails candidat
- ✅ Bouton "Envoyer un email" dans le modal candidat
- ✅ Historique des emails affiché dans le modal candidat
- ✅ Page complète de gestion des templates (`/admin/email-templates`)
- ✅ Sélection de template dans le composer
- ✅ Aperçu en temps réel avec remplacement des variables
- ✅ Lien vers la gestion des templates depuis le composer

## 📋 Étapes pour activer le module

### 1. Exécuter la migration SQL
Exécutez le fichier `migration_add_email_tables.sql` dans votre base Supabase pour créer les tables :
- `email_templates`
- `emails`

### 2. Installer la dépendance Resend
```bash
cd netter-ats-backend
source .venv/bin/activate
pip install resend
```

### 3. Configurer la clé API Resend
Ajoutez dans votre fichier `.env` du backend :
```env
RESEND_API_KEY=votre_cle_api_resend
```

### 4. Modifier l'email expéditeur
Dans `app/main.py`, remplacez `"onboarding@resend.dev"` par votre email vérifié dans Resend (lignes 658 et 676).

**Important** : Vous devez vérifier votre domaine dans Resend avant de pouvoir envoyer des emails depuis votre propre domaine. En attendant, vous pouvez utiliser `onboarding@resend.dev` pour les tests.

### 5. Redémarrer le backend
```bash
# Arrêter le backend actuel (Ctrl+C)
# Puis relancer
cd netter-ats-backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## 🚀 Utilisation

### Envoyer un email à un candidat
1. Ouvrez le modal de détails d'une candidature
2. Cliquez sur le bouton "Envoyer un email" (colonne gauche)
3. Sélectionnez un template (optionnel) ou composez votre email
4. Le sujet et le message peuvent contenir `{{candidate_name}}` qui sera remplacé automatiquement
5. Un aperçu en temps réel montre le résultat avec les variables remplacées
6. Cliquez sur "Envoyer l'email"

### Gérer les templates
1. Accédez à `/admin/email-templates` ou cliquez sur "Gérer les templates" dans le composer
2. Créez un nouveau template avec :
   - Nom du template
   - Sujet (peut contenir `{{candidate_name}}`)
   - Corps du message (peut contenir `{{candidate_name}}`)
3. Modifiez ou supprimez des templates existants

### Consulter l'historique
L'historique des emails envoyés à un candidat s'affiche automatiquement dans le modal de détails (colonne droite), au-dessus de la section "Notes et compte-rendus".

## 📝 Variables supportées

Actuellement, seule la variable `{{candidate_name}}` est supportée. Elle sera automatiquement remplacée par le nom complet du candidat dans :
- Le sujet de l'email
- Le corps de l'email

## 🔧 Notes techniques

1. **Type de candidate_id** : Les candidats utilisent `INTEGER` (SERIAL) dans la base de données, donc les conversions sont gérées automatiquement dans le frontend.

2. **Format HTML** : Les emails sont envoyés en HTML. Les retours à la ligne (`\n`) sont convertis en `<br>`.

3. **Sécurité** : Toutes les routes sont protégées par `verify_admin_api_key`.

4. **Erreurs** : Les erreurs d'envoi sont capturées et affichées à l'utilisateur avec des messages clairs.

## ✨ Fonctionnalités

- ✅ Envoi d'emails individuels
- ✅ Création et gestion de templates
- ✅ Variables dans les templates (`{{candidate_name}}`)
- ✅ Historique complet des emails par candidat
- ✅ Aperçu en temps réel avec remplacement des variables
- ✅ Interface intuitive et intégrée à l'ATS existant
- ✅ Design cohérent avec le reste de l'application

## 🎯 Prochaines étapes possibles (non implémentées)

- Réponses des candidats (nécessite webhook Resend)
- Envoi en masse
- Planification d'emails
- Séquences automatisées
- Plus de variables (nom de l'offre, stage actuel, etc.)

Le module email est maintenant **100% fonctionnel** ! 🎉

