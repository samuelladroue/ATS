# 📧 Activation du module Email - Guide complet

## ✅ Étape 1 : Migration de la base de données

Exécutez la migration SQL dans Supabase pour créer les tables nécessaires :

```sql
-- Copiez et exécutez le contenu de migration_add_email_tables.sql
```

**Fichier** : `migration_add_email_tables.sql`

Cette migration crée :
- `email_templates` : Table pour stocker les templates d'email
- `emails` : Table pour l'historique des emails envoyés

## ✅ Étape 2 : Templates d'exemple (optionnel)

Pour ajouter des templates d'exemple :

```sql
-- Copiez et exécutez le contenu de EMAIL_TEMPLATES_EXAMPLES.sql
```

**Fichier** : `EMAIL_TEMPLATES_EXAMPLES.sql`

Ces templates incluent :
- Invitation entretien présélection
- Invitation entretien technique
- Offre d'emploi
- Refus de candidature
- Confirmation candidature
- Remerciement après entretien

## ✅ Étape 3 : Configuration Resend

### 3.1 Créer un compte Resend

1. Allez sur https://resend.com
2. Créez un compte (gratuit jusqu'à 3000 emails/mois)
3. Vérifiez votre email

### 3.2 Obtenir votre API Key

1. Dans le dashboard Resend, allez dans **API Keys**
2. Cliquez sur **Create API Key**
3. Donnez-lui un nom (ex: "Netter ATS Production")
4. Copiez la clé API (elle ne sera affichée qu'une seule fois !)

### 3.3 Configurer le domaine (optionnel mais recommandé)

Pour utiliser votre propre domaine au lieu de `onboarding@resend.dev` :

1. Allez dans **Domains** dans le dashboard Resend
2. Cliquez sur **Add Domain**
3. Ajoutez votre domaine (ex: `netter.com`)
4. Suivez les instructions DNS pour vérifier le domaine
5. Une fois vérifié, vous pourrez utiliser `noreply@netter.com` ou `recrutement@netter.com`

### 3.4 Configuration dans le backend

Ajoutez ces variables dans votre fichier `.env` du backend :

```bash
# Resend Configuration
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxx
RESEND_FROM_EMAIL=noreply@votre-domaine.com  # ou onboarding@resend.dev pour tester
RESEND_FROM_NAME=Netter ATS
```

**Important** :
- Si vous utilisez `onboarding@resend.dev`, vous pouvez envoyer jusqu'à 100 emails/jour
- Pour la production, configurez votre propre domaine
- Le nom d'expéditeur (`RESEND_FROM_NAME`) apparaîtra comme "Netter ATS" dans la boîte de réception

## ✅ Étape 4 : Redémarrer le backend

Après avoir configuré les variables d'environnement :

```bash
cd netter-ats-backend
source .venv/bin/activate
# Arrêtez le backend actuel (Ctrl+C)
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Vous devriez voir :
```
✅ Resend configuré - Emails envoyés depuis: noreply@votre-domaine.com
```

## ✅ Étape 5 : Tester l'envoi d'email

### Depuis l'interface admin :

1. Allez sur une candidature : `/admin/jobs/[id]`
2. Cliquez sur "Voir détails" d'un candidat
3. Dans la colonne de droite, cliquez sur **"Envoyer un email"**
4. Remplissez le formulaire ou sélectionnez un template
5. Cliquez sur **"Envoyer"**

### Vérifier l'historique :

- Les emails envoyés apparaissent dans la section **"Historique des emails"** du modal candidat
- Vous pouvez voir le sujet, le contenu, la date et l'expéditeur

## ✅ Étape 6 : Gérer les templates

### Créer/Modifier/Supprimer des templates :

1. Allez sur `/admin/email-templates`
2. Cliquez sur **"Créer un template"**
3. Remplissez :
   - **Nom** : Nom du template (ex: "Invitation entretien")
   - **Sujet** : Sujet de l'email (peut contenir `{{candidate_name}}`)
   - **Corps** : Message (peut contenir `{{candidate_name}}`)

### Variables disponibles :

- `{{candidate_name}}` : Remplace automatiquement par le nom du candidat

## 🎯 Fonctionnalités disponibles

### ✅ Composer un email
- Bouton "Envoyer un email" sur chaque profil candidat
- Modal avec sujet, message, et sélection de template
- Prévisualisation avec remplacement des variables

### ✅ Templates d'email
- Créer, modifier, supprimer des templates
- Variables dynamiques (`{{candidate_name}}`)
- Interface dédiée : `/admin/email-templates`

### ✅ Historique des emails
- Tous les emails envoyés à un candidat
- Affichage chronologique (plus récent en premier)
- Sujet, contenu, expéditeur, date/heure

### ✅ Intégration Resend
- Envoi d'emails via Resend API
- Support HTML dans les emails
- Gestion des erreurs d'envoi

## 🐛 Dépannage

### Les emails ne partent pas

1. **Vérifiez la clé API** :
   ```bash
   echo $RESEND_API_KEY  # Doit afficher votre clé
   ```

2. **Vérifiez les logs du backend** :
   - Regardez les erreurs dans la console où tourne uvicorn
   - Les erreurs Resend sont affichées clairement

3. **Vérifiez le domaine** :
   - Si vous utilisez votre domaine, assurez-vous qu'il est vérifié dans Resend
   - Pour tester rapidement, utilisez `onboarding@resend.dev`

### Les templates ne se chargent pas

1. Vérifiez que la table `email_templates` existe dans Supabase
2. Vérifiez les logs du backend pour les erreurs SQL

### L'historique ne s'affiche pas

1. Vérifiez que la table `emails` existe dans Supabase
2. Vérifiez que des emails ont bien été envoyés (ils sont enregistrés même si l'envoi échoue)

## 📝 Notes importantes

- **Limites Resend** :
  - Plan gratuit : 3000 emails/mois
  - `onboarding@resend.dev` : 100 emails/jour max
  - Domaine vérifié : pas de limite quotidienne (selon votre plan)

- **Sécurité** :
  - La clé API Resend est stockée dans `.env` (ne jamais la commiter)
  - Les emails sont envoyés uniquement depuis l'interface admin (protégée par API key)

- **Variables d'environnement** :
  - `RESEND_API_KEY` : **Requis** pour envoyer des emails
  - `RESEND_FROM_EMAIL` : Optionnel (défaut: `onboarding@resend.dev`)
  - `RESEND_FROM_NAME` : Optionnel (défaut: `Netter ATS`)

## 🚀 Prochaines étapes (futures améliorations)

- [ ] Support des réponses d'email (webhook Resend)
- [ ] Envoi en masse
- [ ] Planification d'emails
- [ ] Templates plus avancés avec plus de variables
- [ ] Statistiques d'ouverture/clics

