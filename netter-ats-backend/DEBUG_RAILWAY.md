# 🐛 Déboguer "Application failed to respond" sur Railway

## ✅ Étape 1 : Vérifier les logs de déploiement

1. **Sur Railway**, allez dans votre service "ATS"
2. Cliquez sur l'onglet **"Deploy Logs"** (ou **"Build Logs"**)
3. **Lisez les dernières lignes** pour voir l'erreur exacte

## 🔍 Causes courantes et solutions

### Erreur 1 : "Database connection failed"
**Symptôme** : Erreur de connexion PostgreSQL dans les logs

**Solution** :
- Vérifiez que `DATABASE_URL` est correct dans les variables d'environnement
- Vérifiez que le mot de passe Supabase est correct
- Vérifiez que l'URL utilise bien le Session Pooler (avec `.pooler.supabase.com`)

### Erreur 2 : "No module named 'app'"
**Symptôme** : `ModuleNotFoundError: No module named 'app'`

**Solution** :
- Vérifiez que **Root Directory** est bien `netter-ats-backend` dans Settings
- Vérifiez que le fichier `app/__init__.py` existe

### Erreur 3 : "Port already in use" ou problème de port
**Symptôme** : Erreur liée au port

**Solution** :
- Vérifiez que le `Procfile` utilise bien `$PORT`
- Le port dans "Networking" doit correspondre au port que Railway assigne (généralement automatique)

### Erreur 4 : "Import error" ou dépendances manquantes
**Symptôme** : Erreur d'import Python

**Solution** :
- Vérifiez que `requirements.txt` contient toutes les dépendances
- Vérifiez les logs de build pour voir si `pip install` a réussi

### Erreur 5 : Application démarre mais crash immédiatement
**Symptôme** : L'app démarre puis crash

**Solution** :
- Vérifiez les logs de déploiement pour voir l'erreur Python exacte
- Vérifiez que `DATABASE_URL` est bien défini
- Vérifiez que la connexion à la base fonctionne

## 📋 Checklist de vérification

- [ ] `DATABASE_URL` est défini dans les variables d'environnement
- [ ] `ADMIN_API_KEY` est défini dans les variables d'environnement
- [ ] Root Directory est `netter-ats-backend`
- [ ] Le build s'est terminé sans erreur
- [ ] Les logs montrent "Application startup complete"
- [ ] Le port dans Networking correspond au port de l'app

## 🔧 Actions immédiates

1. **Allez dans "Deploy Logs"** sur Railway
2. **Copiez les dernières lignes d'erreur**
3. **Vérifiez les points ci-dessus**

