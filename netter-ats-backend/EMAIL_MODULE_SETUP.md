# Module Email - Guide d'installation et configuration

## ✅ Ce qui a été implémenté

### Backend
1. **Modèles de données** (`app/models.py`)
   - `EmailTemplateCreate`, `EmailTemplateUpdate`, `EmailTemplate`
   - `EmailSend`, `Email`

2. **Migration SQL** (`migration_add_email_tables.sql`)
   - Table `email_templates` pour stocker les templates
   - Table `emails` pour l'historique des emails envoyés

3. **Endpoints API** (`app/main.py`)
   - `GET /api/email-templates` - Liste tous les templates
   - `POST /api/email-templates` - Créer un template
   - `GET /api/email-templates/{id}` - Récupérer un template
   - `PATCH /api/email-templates/{id}` - Mettre à jour un template
   - `DELETE /api/email-templates/{id}` - Supprimer un template
   - `POST /api/emails/send` - Envoyer un email
   - `GET /api/candidates/{id}/emails` - Historique des emails d'un candidat

4. **Intégration Resend**
   - Configuration via variable d'environnement `RESEND_API_KEY`
   - Remplacement automatique des variables dans les templates (`{{candidate_name}}`)

### Frontend - Routes Server-side
- `/server/api/email-templates/index.get.ts`
- `/server/api/email-templates/index.post.ts`
- `/server/api/email-templates/[id].get.ts`
- `/server/api/email-templates/[id].patch.ts`
- `/server/api/email-templates/[id].delete.ts`
- `/server/api/emails/send.post.ts`
- `/server/api/candidates/[id]/emails.get.ts`

## 📋 Étapes pour finaliser

### 1. Exécuter la migration SQL
Exécutez le fichier `migration_add_email_tables.sql` dans votre base Supabase pour créer les tables nécessaires.

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

### 4. Modifier l'email expéditeur dans `app/main.py`
Remplacez `"onboarding@resend.dev"` par votre email vérifié dans Resend (lignes 658 et 676).

### 5. Frontend - À implémenter
Les composants suivants doivent être créés/modifiés :

#### A. Modal Email Composer
- Ajouter un bouton "Send Email" dans le modal de détails candidat (colonne gauche)
- Créer un modal avec :
  - Champ sujet
  - Champ message (textarea)
  - Sélecteur de template (optionnel)
  - Bouton pour créer un nouveau template
  - Bouton d'envoi

#### B. Page de gestion des templates
- Créer `/pages/admin/email-templates.vue`
- Liste des templates avec actions (éditer, supprimer)
- Formulaire pour créer/éditer un template
- Support des variables `{{candidate_name}}`

#### C. Historique des emails
- Ajouter une section dans le modal de détails candidat (colonne droite)
- Afficher les emails envoyés en ordre chronologique
- Afficher sujet, corps, expéditeur, date/heure

## 🔧 Variables de template supportées

Actuellement supporté :
- `{{candidate_name}}` - Remplace par le nom complet du candidat

## 📝 Notes importantes

1. **Type de candidate_id** : Les candidats utilisent `INTEGER` (SERIAL) et non UUID dans la base de données actuelle.

2. **Email expéditeur** : Vous devez vérifier votre domaine dans Resend avant de pouvoir envoyer des emails depuis votre propre domaine.

3. **Format HTML** : Les emails sont envoyés en HTML. Les retours à la ligne (`\n`) sont convertis en `<br>`.

4. **Sécurité** : Toutes les routes sont protégées par `verify_admin_api_key`.

## 🚀 Prochaines étapes

Une fois la migration SQL exécutée et Resend configuré, vous pouvez :
1. Tester l'envoi d'emails via l'API directement
2. Implémenter les composants frontend
3. Créer des templates de base
4. Tester le flux complet depuis l'interface

