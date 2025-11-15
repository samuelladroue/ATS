# État du projet ATS - Netter

## ✅ Ce qui est fait

### Backend FastAPI
- ✅ Connexion PostgreSQL/Supabase (Session Pooler IPv4)
- ✅ Tables créées : `jobs`, `candidates`, `applications`
- ✅ Modèles Pydantic avec UUID
- ✅ Authentification admin (API key)
- ✅ CORS configuré

### Routes API implémentées

**Jobs (Admin) :**
- ✅ `POST /api/jobs` - Créer une offre
- ✅ `GET /api/jobs` - Lister toutes les offres

**Jobs (Public) :**
- ✅ `GET /api/jobs/{slug}` - Voir une offre

**Applications :**
- ✅ `POST /api/jobs/{slug}/apply` - Postuler à une offre
- ✅ `GET /api/jobs/{job_id}/applications` - Voir les candidatures (admin)
- ✅ `PATCH /api/applications/{application_id}` - Mettre à jour une candidature (admin)

**Système :**
- ✅ `GET /health` - Health check

## 🔨 Ce qui reste à faire pour un ATS fonctionnel

### 1. Frontend (priorité haute)
**Pour les candidats :**
- Page publique listant les offres ouvertes
- Page de détail d'une offre
- Formulaire de candidature

**Pour les admins :**
- Dashboard de gestion des candidatures
- Vue liste des offres avec actions (ouvrir/fermer)
- Vue détail d'une candidature avec gestion des stages

**Technologies suggérées :**
- Nuxt 3 (comme mentionné dans les commentaires)
- React + Vite
- Vue 3 + Vite

### 2. Fonctionnalités backend manquantes

**Routes publiques :**
- ⚠️ `GET /api/jobs` (public) - Liste des offres ouvertes uniquement
  - Actuellement, cette route est admin-only
  - Besoin d'une version publique qui filtre `status = 'open'`

**Gestion des offres :**
- ⚠️ `PATCH /api/jobs/{job_id}` - Modifier une offre (admin)
- ⚠️ `DELETE /api/jobs/{job_id}` - Supprimer/fermer une offre (admin)

**Upload de CV :**
- ⚠️ Le schéma a `resume_url` mais pas d'endpoint d'upload
- Options :
  - Upload vers Supabase Storage
  - Upload vers S3/Cloudflare R2
  - Lien externe (LinkedIn, portfolio)

**Notifications :**
- ⚠️ Email de confirmation au candidat
- ⚠️ Email de notification à l'admin quand nouvelle candidature

### 3. Améliorations UX/UI

**Candidats :**
- Recherche/filtrage des offres (par département, localisation)
- Confirmation visuelle après candidature
- Page "Merci pour votre candidature"

**Admins :**
- Statistiques (nombre de candidatures par offre, par stage)
- Export CSV des candidatures
- Filtres avancés (par stage, date, offre)
- Recherche de candidats

### 4. Sécurité et validation

- ✅ API key admin (fait)
- ⚠️ Rate limiting (limiter les candidatures par IP/email)
- ⚠️ Validation plus stricte des données
- ⚠️ Sanitization du markdown dans les descriptions

### 5. Tests

- ⚠️ Tests unitaires des routes
- ⚠️ Tests d'intégration avec la base
- ⚠️ Tests E2E du flow complet

## 🎯 Prochaines étapes recommandées

### Phase 1 : MVP fonctionnel (minimum viable)
1. **Route publique pour lister les offres ouvertes**
   ```python
   @app.get("/api/jobs/public", response_model=list[JobList])
   async def list_public_jobs():
       # Retourne uniquement les offres avec status='open'
   ```

2. **Frontend minimal**
   - Page liste des offres
   - Page détail offre + formulaire candidature
   - Page admin basique pour voir les candidatures

### Phase 2 : Améliorations
3. Upload de CV (Supabase Storage)
4. Notifications email
5. Dashboard admin plus complet

### Phase 3 : Features avancées
6. Recherche/filtres
7. Statistiques
8. Export de données

## 📝 Notes techniques

- Le backend est prêt et fonctionnel
- Les UUID sont correctement gérés
- La base de données est configurée
- Il manque principalement le frontend pour rendre l'ATS utilisable

