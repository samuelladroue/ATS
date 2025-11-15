#!/usr/bin/env python3
"""
Script de vérification de la configuration email
"""

import os
import sys
import asyncio
from pathlib import Path

# Couleurs pour les messages
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
NC = '\033[0m'  # No Color

def check_resend_installed():
    """Vérifie si Resend est installé"""
    try:
        import resend
        print(f"{GREEN}✅ Resend est installé{NC}")
        return True
    except ImportError:
        print(f"{RED}❌ Resend n'est pas installé{NC}")
        print(f"   Installez-le avec: pip install resend")
        return False

def check_env_variables():
    """Vérifie les variables d'environnement"""
    print("\n📋 Vérification des variables d'environnement:")
    
    api_key = os.getenv("RESEND_API_KEY", "")
    from_email = os.getenv("RESEND_FROM_EMAIL", "onboarding@resend.dev")
    from_name = os.getenv("RESEND_FROM_NAME", "Netter ATS")
    
    if api_key:
        masked_key = api_key[:10] + "..." + api_key[-5:] if len(api_key) > 15 else "***"
        print(f"{GREEN}✅ RESEND_API_KEY configurée: {masked_key}{NC}")
    else:
        print(f"{YELLOW}⚠️  RESEND_API_KEY non configurée{NC}")
        print(f"   Ajoutez-la dans votre fichier .env")
    
    print(f"{GREEN}✅ RESEND_FROM_EMAIL: {from_email}{NC}")
    print(f"{GREEN}✅ RESEND_FROM_NAME: {from_name}{NC}")
    
    return bool(api_key)

def check_database_tables():
    """Vérifie si les tables existent (nécessite une connexion DB)"""
    print("\n🗄️  Vérification des tables de base de données:")
    print(f"{YELLOW}⚠️  Vérification manuelle requise{NC}")
    print(f"   Exécutez dans Supabase:")
    print(f"   SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name IN ('email_templates', 'emails');")
    print(f"\n   Les tables doivent exister:")
    print(f"   - email_templates")
    print(f"   - emails")

def check_backend_code():
    """Vérifie que le code backend est prêt"""
    print("\n💻 Vérification du code backend:")
    
    main_py = Path(__file__).parent / "app" / "main.py"
    if not main_py.exists():
        print(f"{RED}❌ app/main.py non trouvé{NC}")
        return False
    
    content = main_py.read_text()
    
    checks = [
        ("resend", "Import Resend"),
        ("/api/emails/send", "Endpoint send_email"),
        ("/api/email-templates", "Endpoints email_templates"),
        ("/api/candidates", "Endpoint candidate emails"),
    ]
    
    all_ok = True
    for check, name in checks:
        if check in content:
            print(f"{GREEN}✅ {name} présent{NC}")
        else:
            print(f"{RED}❌ {name} manquant{NC}")
            all_ok = False
    
    return all_ok

def main():
    print("🔍 Vérification de la configuration email pour Netter ATS\n")
    print("=" * 60)
    
    resend_ok = check_resend_installed()
    env_ok = check_env_variables()
    code_ok = check_backend_code()
    check_database_tables()
    
    print("\n" + "=" * 60)
    print("\n📊 Résumé:")
    
    if resend_ok and env_ok and code_ok:
        print(f"{GREEN}✅ Configuration prête !{NC}")
        print(f"\n📝 Prochaines étapes:")
        print(f"   1. Exécutez la migration SQL dans Supabase")
        print(f"   2. Redémarrez le backend")
        print(f"   3. Testez l'envoi d'email depuis l'interface admin")
    else:
        print(f"{YELLOW}⚠️  Configuration incomplète{NC}")
        print(f"\n📝 Actions requises:")
        if not resend_ok:
            print(f"   - Installez Resend: pip install resend")
        if not env_ok:
            print(f"   - Configurez RESEND_API_KEY dans .env")
        if not code_ok:
            print(f"   - Vérifiez que le code backend est à jour")
    
    print(f"\n📚 Documentation:")
    print(f"   - Guide complet: ACTIVATION_EMAILS.md")
    print(f"   - Checklist: ../CHECKLIST_EMAILS.md")

if __name__ == "__main__":
    main()

