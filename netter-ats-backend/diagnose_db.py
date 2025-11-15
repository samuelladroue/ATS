"""
Script de diagnostic pour identifier les problèmes de connexion à la base de données.
"""
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("🔍 Diagnostic de la connexion PostgreSQL\n")
print("=" * 60)

# 1. Vérifier que DATABASE_URL existe
if not DATABASE_URL:
    print("❌ ERREUR: DATABASE_URL n'est pas défini dans .env")
    exit(1)

print("✅ DATABASE_URL est défini")

# 2. Vérifier le format de l'URL
if not DATABASE_URL.startswith("postgresql://"):
    print("⚠️  ATTENTION: L'URL ne commence pas par 'postgresql://'")
else:
    print("✅ Format de l'URL correct (postgresql://)")

# 3. Extraire les informations de l'URL (sans afficher le mot de passe)
try:
    parsed = urllib.parse.urlparse(DATABASE_URL)
    
    print(f"\n📋 Informations de connexion:")
    print(f"   Host: {parsed.hostname}")
    print(f"   Port: {parsed.port or 5432}")
    print(f"   Database: {parsed.path.lstrip('/')}")
    print(f"   User: {parsed.username}")
    
    # Vérifier le mot de passe
    password = parsed.password
    if not password or password == "TON_MOT_DE_PASSE":
        print(f"\n❌ PROBLÈME DÉTECTÉ:")
        print(f"   Le mot de passe n'est pas configuré ou est toujours 'TON_MOT_DE_PASSE'")
        print(f"   → Vous devez remplacer TON_MOT_DE_PASSE par votre vrai mot de passe Supabase")
    else:
        print(f"   Password: {'*' * len(password)} (configuré)")
        
        # Vérifier si le mot de passe contient des caractères spéciaux
        special_chars = ['@', ':', '/', '?', '#', '[', ']', '%']
        has_special = any(char in password for char in special_chars)
        if has_special:
            print(f"\n⚠️  ATTENTION: Le mot de passe contient des caractères spéciaux")
            print(f"   Ces caractères doivent être encodés en URL (URL encoding)")
            print(f"   Exemple: @ devient %40, : devient %3A, etc.")
            print(f"\n   Mot de passe encodé: {urllib.parse.quote(password, safe='')}")
            print(f"   → Utilisez cette version encodée dans votre DATABASE_URL")
    
    # Vérifier les paramètres de requête
    if parsed.query:
        params = urllib.parse.parse_qs(parsed.query)
        if 'sslmode' in params:
            print(f"   SSL Mode: {params['sslmode'][0]}")
        else:
            print(f"   ⚠️  SSL Mode non spécifié (recommandé: require)")
    
except Exception as e:
    print(f"❌ ERREUR lors de l'analyse de l'URL: {e}")

print("\n" + "=" * 60)
print("\n💡 Solutions possibles:")
print("   1. Vérifiez que vous avez remplacé TON_MOT_DE_PASSE par votre vrai mot de passe")
print("   2. Si votre mot de passe contient des caractères spéciaux, encodez-les en URL")
print("   3. Vérifiez que votre base Supabase est active et accessible")
print("   4. Vérifiez votre mot de passe dans le dashboard Supabase (Settings > Database)")
print("\n📖 Pour obtenir votre mot de passe Supabase:")
print("   - Allez sur https://supabase.com/dashboard")
print("   - Sélectionnez votre projet")
print("   - Allez dans Settings > Database")
print("   - Copiez le mot de passe de la section 'Connection string'")

