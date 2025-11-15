#!/usr/bin/env python3
"""
Test direct de Resend pour vérifier que la clé API fonctionne
"""

import resend
import os
from dotenv import load_dotenv

load_dotenv()

# Charger la clé API
api_key = os.getenv("RESEND_API_KEY", "")
print(f"🔑 Clé API: {api_key[:10]}...{api_key[-5:] if len(api_key) > 15 else '***'}")
print()

if not api_key:
    print("❌ RESEND_API_KEY non trouvée dans .env")
    exit(1)

# Configurer Resend
resend.api_key = api_key

# Test d'envoi selon le format exact de leur documentation
print("📧 Test d'envoi d'email avec Resend...")
print()

try:
    params = {
        "from": "Netter ATS <onboarding@resend.dev>",
        "to": ["delivered@resend.dev"],  # Email de test Resend
        "subject": "Test depuis Netter ATS",
        "html": "<p>Ceci est un test d'envoi d'email depuis Netter ATS.</p>"
    }
    
    print("Paramètres:")
    print(f"  from: {params['from']}")
    print(f"  to: {params['to']}")
    print(f"  subject: {params['subject']}")
    print()
    
    email = resend.Emails.send(params)
    
    print("✅ Email envoyé avec succès!")
    print(f"Réponse: {email}")
    
except Exception as e:
    print(f"❌ Erreur lors de l'envoi: {e}")
    import traceback
    traceback.print_exc()


