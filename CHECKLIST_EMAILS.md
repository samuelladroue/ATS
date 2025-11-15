# ✅ Checklist - Activation du module Email

## 📋 Prérequis

- [x] Resend installé dans le backend (`pip install resend`)
- [x] Code backend prêt (endpoints email créés)
- [x] Code frontend prêt (composer, historique, templates)
- [x] Routes serveur Nuxt créées

## 🗄️ Base de données

### Étape 1 : Créer les tables
- [ ] Exécuter `migration_add_email_tables.sql` dans Supabase
  - Table `email_templates` créée
  - Table `emails` créée
  - Index créés
  - Trigger créé

### Étape 2 : Ajouter des templates d'exemple (optionnel)
- [ ] Exécuter `EMAIL_TEMPLATES_EXAMPLES.sql` dans Supabase
  - 6 templates d'exemple ajoutés

## 🔑 Configuration Resend

### Étape 3 : Créer un compte Resend
- [ ] Aller sur https://resend.com
- [ ] Créer un compte
- [ ] Vérifier l'email

### Étape 4 : Obtenir la clé API
- [ ] Aller dans **API Keys** du dashboard
- [ ] Créer une nouvelle clé API
- [ ] Copier la clé (format: `re_xxxxxxxxxxxxxxxxxxxxx`)

### Étape 5 : Configurer le domaine (optionnel)
- [ ] Aller dans **Domains**
- [ ] Ajouter votre domaine
- [ ] Configurer les DNS selon les instructions
- [ ] Attendre la vérification

### Étape 6 : Configurer les variables d'environnement
- [ ] Ouvrir `.env` dans `netter-ats-backend/`
- [ ] Ajouter :
  ```bash
  RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxx
  RESEND_FROM_EMAIL=noreply@votre-domaine.com  # ou onboarding@resend.dev pour tester
  RESEND_FROM_NAME=Netter ATS
  ```

## 🚀 Démarrage

### Étape 7 : Redémarrer le backend
- [ ] Arrêter le backend actuel
- [ ] Redémarrer avec `uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
- [ ] Vérifier le message : `✅ Resend configuré - Emails envoyés depuis: ...`

## 🧪 Tests

### Étape 8 : Tester la gestion des templates
- [ ] Aller sur `/admin/email-templates`
- [ ] Créer un nouveau template
- [ ] Modifier un template existant
- [ ] Supprimer un template

### Étape 9 : Tester l'envoi d'email
- [ ] Aller sur `/admin/jobs/[id]` (une offre avec candidatures)
- [ ] Cliquer sur "Voir détails" d'un candidat
- [ ] Cliquer sur "Envoyer un email"
- [ ] Sélectionner un template OU écrire un email personnalisé
- [ ] Cliquer sur "Envoyer"
- [ ] Vérifier que l'email apparaît dans l'historique

### Étape 10 : Vérifier la réception
- [ ] Vérifier la boîte email du candidat
- [ ] Vérifier que l'email est bien reçu
- [ ] Vérifier que le formatage est correct

## 📝 Variables disponibles dans les templates

- `{{candidate_name}}` : Nom complet du candidat

## 🐛 Dépannage

### Les emails ne partent pas
- [ ] Vérifier que `RESEND_API_KEY` est bien défini dans `.env`
- [ ] Vérifier les logs du backend pour les erreurs
- [ ] Vérifier que le domaine est vérifié (si vous utilisez votre domaine)
- [ ] Tester avec `onboarding@resend.dev` d'abord

### Les templates ne se chargent pas
- [ ] Vérifier que la table `email_templates` existe
- [ ] Vérifier les logs du backend
- [ ] Vérifier la console du navigateur

### L'historique ne s'affiche pas
- [ ] Vérifier que la table `emails` existe
- [ ] Vérifier qu'un email a bien été envoyé
- [ ] Vérifier les logs du backend

## 📚 Documentation

- Guide complet : `netter-ats-backend/ACTIVATION_EMAILS.md`
- Migration SQL : `netter-ats-backend/migration_add_email_tables.sql`
- Templates exemples : `netter-ats-backend/EMAIL_TEMPLATES_EXAMPLES.sql`

