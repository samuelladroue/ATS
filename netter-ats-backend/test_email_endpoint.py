#!/usr/bin/env python3
"""
Script de test pour l'endpoint d'envoi d'email
"""

import requests
import json
from uuid import UUID

# Configuration
BACKEND_URL = "http://127.0.0.1:8000"
API_KEY = "change-me-in-prod"  # Remplacez par votre clé API admin

# Test: Récupérer un candidat existant
print("🔍 Test de l'endpoint d'envoi d'email\n")

# 1. Vérifier que le backend répond
try:
    response = requests.get(f"{BACKEND_URL}/health")
    print(f"✅ Backend accessible: {response.status_code}")
except Exception as e:
    print(f"❌ Backend non accessible: {e}")
    exit(1)

# 2. Récupérer une candidature pour obtenir un candidate_id
try:
    # Récupérer les offres
    response = requests.get(
        f"{BACKEND_URL}/api/jobs",
        headers={"x-api-key": API_KEY}
    )
    if response.status_code == 200:
        jobs = response.json()
        if jobs:
            job_id = jobs[0]["id"]
            print(f"✅ Offre trouvée: {job_id}")
            
            # Récupérer les candidatures
            response = requests.get(
                f"{BACKEND_URL}/api/jobs/{job_id}/applications",
                headers={"x-api-key": API_KEY}
            )
            if response.status_code == 200:
                applications = response.json()
                if applications:
                    candidate_id = applications[0]["candidate_id"]
                    candidate_email = applications[0]["candidate_email"]
                    print(f"✅ Candidat trouvé: {candidate_id} ({candidate_email})")
                    
                    # 3. Tester l'envoi d'email
                    print("\n📧 Test d'envoi d'email...")
                    email_data = {
                        "candidate_id": str(candidate_id),
                        "subject": "Test email depuis Netter ATS",
                        "body": "Bonjour {{candidate_name}},\n\nCeci est un email de test.",
                        "template_id": None
                    }
                    
                    response = requests.post(
                        f"{BACKEND_URL}/api/emails/send",
                        headers={
                            "x-api-key": API_KEY,
                            "Content-Type": "application/json"
                        },
                        json=email_data
                    )
                    
                    print(f"Status: {response.status_code}")
                    if response.status_code == 200:
                        print("✅ Email envoyé avec succès!")
                        print(json.dumps(response.json(), indent=2))
                    else:
                        print(f"❌ Erreur: {response.status_code}")
                        print(response.text)
                else:
                    print("⚠️  Aucune candidature trouvée")
            else:
                print(f"❌ Erreur lors de la récupération des candidatures: {response.status_code}")
                print(response.text)
        else:
            print("⚠️  Aucune offre trouvée")
    else:
        print(f"❌ Erreur lors de la récupération des offres: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()


