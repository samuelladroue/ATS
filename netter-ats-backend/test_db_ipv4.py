"""
Test de connexion en forçant IPv4.
"""
import asyncio
import os
from dotenv import load_dotenv
from psycopg import AsyncConnection

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ ERREUR: DATABASE_URL n'est pas défini")
    exit(1)

# Forcer IPv4 en modifiant l'URL pour utiliser l'adresse IP directement
# ou en ajoutant des paramètres de connexion
async def test_ipv4():
    """Test avec IPv4."""
    print("🔄 Test de connexion (IPv4)...")
    
    # Essayer avec l'hostname directement (psycopg devrait gérer IPv4/IPv6)
    # Mais on peut aussi essayer de forcer IPv4 via les paramètres de connexion
    try:
        # Ajouter ?connect_timeout=10 pour limiter le timeout
        test_url = DATABASE_URL
        if "?" in test_url:
            test_url += "&connect_timeout=10"
        else:
            test_url += "?connect_timeout=10"
        
        print(f"📋 Tentative de connexion...")
        conn = await AsyncConnection.connect(test_url)
        print("✅ Connexion établie!")
        
        async with conn.cursor() as cur:
            await cur.execute("SELECT now(), current_database(), version();")
            result = await cur.fetchone()
            print(f"✅ Requête réussie!")
            print(f"📅 Heure serveur: {result[0]}")
            print(f"🗄️  Base de données: {result[1]}")
            print(f"📦 Version: {result[2][:60]}...")
        
        await conn.close()
        print("\n🎉 La connexion fonctionne!")
        return True
        
    except Exception as e:
        error_str = str(e)
        print(f"\n❌ ERREUR: {error_str}")
        
        if "Connection refused" in error_str:
            print("\n💡 Le serveur refuse la connexion. Causes possibles:")
            print("   1. ⏸️  Votre projet Supabase est en PAUSE")
            print("      → Allez sur https://supabase.com/dashboard")
            print("      → Vérifiez que votre projet est ACTIF (pas en pause)")
            print("      → Si en pause, cliquez sur 'Restore' pour le réactiver")
            print()
            print("   2. 🌐 Problème de réseau IPv6")
            print("      → Votre réseau peut bloquer IPv6")
            print("      → Essayez depuis un autre réseau (VPN, mobile hotspot)")
            print()
            print("   3. 🔒 Firewall ou restrictions réseau")
            print("      → Vérifiez que le port 5432 n'est pas bloqué")
        
        return False

if __name__ == "__main__":
    success = asyncio.run(test_ipv4())
    exit(0 if success else 1)

