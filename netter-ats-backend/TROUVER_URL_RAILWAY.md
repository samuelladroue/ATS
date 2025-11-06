# 🔗 Où trouver l'URL sur Railway

## Méthode 1 : Dans l'en-tête du service (le plus simple)

1. **Regardez juste en dessous du nom du service** ("ATS / 2b2abc46")
2. Il devrait y avoir une **URL** ou un **bouton "Generate Domain"**
3. Si vous voyez "Generate Domain", cliquez dessus
4. Railway générera une URL automatiquement (ex: `https://ats-production-xxxx.up.railway.app`)

## Méthode 2 : Dans Settings → Networking

1. Cliquez sur **Settings** (⚙️)
2. Allez dans l'onglet **"Networking"** ou **"Domains"**
3. Vous verrez l'URL générée par Railway
4. Si aucune URL n'apparaît, cliquez sur **"Generate Domain"**

## Méthode 3 : Dans l'onglet Details

1. Dans l'onglet **"Details"** du service
2. Cherchez une section **"Public URL"** ou **"Domain"**
3. L'URL devrait être affichée là

## Méthode 4 : Via l'API Railway (si besoin)

Si vous ne trouvez toujours pas l'URL, Railway génère toujours une URL par défaut. Elle suit ce format :
```
https://[service-name]-[random-id].up.railway.app
```

## ⚠️ Si aucune URL n'apparaît

1. Allez dans **Settings** → **"Networking"**
2. Cliquez sur **"Generate Domain"**
3. Railway créera une URL publique automatiquement

## ✅ Une fois que vous avez l'URL

L'URL ressemble à :
```
https://ats-production-xxxx.up.railway.app
```

Testez-la :
```
https://votre-url.up.railway.app/health
```

Devrait retourner : `{"status": "ok", "db": true}`

