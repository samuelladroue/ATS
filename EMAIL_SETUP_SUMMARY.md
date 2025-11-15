# 📧 Résumé - Module Email Netter ATS

## ✅ Ce qui est prêt

### Backend
- ✅ Resend installé (`pip install resend`)
- ✅ Code backend complet avec tous les endpoints
- ✅ Gestion des variables d'environnement (RESEND_API_KEY, RESEND_FROM_EMAIL, RESEND_FROM_NAME)
- ✅ Support conditionnel (fonctionne même sans Resend pour les autres fonctionnalités)

### Frontend
- ✅ Page de gestion des templates (`/admin/email-templates`)
- ✅ Composer d'email dans le modal candidat
- ✅ Historique des emails par candidat
- ✅ Toutes les routes serveur Nuxt créées

### Base de données
- ✅ Script de migration SQL prêt (`migration_add_email_tables.sql`)
- ✅ Script de templates d'exemple prêt (`EMAIL_TEMPLATES_EXAMPLES.sql`)

## 🚀 Pour activer les emails

### 1. Migration de la base de données

Exécutez dans Supabase :
```sql
-- Contenu de migration_add_email_tables.sql
```

### 2. Configuration Resend

1. **Créer un compte** : https://resend.com
2. **Obtenir la clé API** : Dashboard → API Keys → Create API Key
3. **Configurer dans `.env`** :
   ```bash
   RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxx
   RESEND_FROM_EMAIL=noreply@votre-domaine.com  # ou onboarding@resend.dev pour tester
   RESEND_FROM_NAME=Netter ATS
   ```

### 3. Redémarrer le backend

```bash
cd netter-ats-backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Vous devriez voir :
```
✅ Resend configuré - Emails envoyés depuis: noreply@votre-domaine.com
```

### 4. Tester

1. Aller sur `/admin/jobs/[id]`
2. Cliquer sur "Voir détails" d'un candidat
3. Cliquer sur "Envoyer un email"
4. Sélectionner un template ou écrire un email
5. Envoyer

## 📁 Fichiers créés/modifiés

### Backend
- `app/main.py` - Endpoints email ajoutés
- `migration_add_email_tables.sql` - Migration SQL
- `EMAIL_TEMPLATES_EXAMPLES.sql` - Templates d'exemple
- `ACTIVATION_EMAILS.md` - Guide complet
- `check_email_setup.py` - Script de vérification

### Frontend
- `pages/admin/email-templates.vue` - Gestion des templates
- `pages/admin/jobs/[id].vue` - Composer et historique email
- `server/api/emails/send.post.ts` - Route d'envoi
- `server/api/email-templates/*.ts` - Routes templates
- `server/api/candidates/[id]/emails.get.ts` - Route historique

## 🎯 Fonctionnalités

### ✅ Composer un email
- Modal avec sujet, message, sélection de template
- Prévisualisation avec remplacement des variables
- Variables disponibles : `{{candidate_name}}`

### ✅ Templates d'email
- CRUD complet (créer, lire, modifier, supprimer)
- Interface dédiée : `/admin/email-templates`
- Variables dynamiques

### ✅ Historique des emails
- Tous les emails envoyés à un candidat
- Affichage chronologique
- Sujet, contenu, expéditeur, date/heure

### ✅ Intégration Resend
- Envoi via Resend API
- Support HTML
- Gestion des erreurs

## 🔍 Vérification

Exécutez le script de vérification :
```bash
cd netter-ats-backend
source .venv/bin/activate
python3 check_email_setup.py
```

## 📚 Documentation

- **Guide complet** : `netter-ats-backend/ACTIVATION_EMAILS.md`
- **Checklist** : `CHECKLIST_EMAILS.md`
- **Migration SQL** : `netter-ats-backend/migration_add_email_tables.sql`
- **Templates exemples** : `netter-ats-backend/EMAIL_TEMPLATES_EXAMPLES.sql`

## ⚠️ Notes importantes

- **Limites Resend** :
  - Plan gratuit : 3000 emails/mois
  - `onboarding@resend.dev` : 100 emails/jour max
  - Domaine vérifié : pas de limite quotidienne (selon votre plan)

- **Sécurité** :
  - La clé API est dans `.env` (ne jamais commiter)
  - Les emails sont envoyés uniquement depuis l'interface admin

- **Variables d'environnement** :
  - `RESEND_API_KEY` : **Requis** pour envoyer
  - `RESEND_FROM_EMAIL` : Optionnel (défaut: `onboarding@resend.dev`)
  - `RESEND_FROM_NAME` : Optionnel (défaut: `Netter ATS`)

## 🎉 Prêt à utiliser !

Une fois la migration SQL exécutée et Resend configuré, le module email est entièrement fonctionnel.

