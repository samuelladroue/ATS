"""
Test de connexion directe (sans pool) pour diagnostiquer les problèmes.
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

async def test_direct():
    """Test de connexion directe."""
    print("🔄 Test de connexion directe (sans pool)...")
    print(f"📋 URL: {DATABASE_URL.split('@')[0]}@***")
    
    try:
        conn = await AsyncConnection.connect(DATABASE_URL)
        print("✅ Connexion établie!")
        
        async with conn.cursor() as cur:
            await cur.execute("SELECT now(), version();")
            result = await cur.fetchone()
            print(f"✅ Requête réussie!")
            print(f"📅 Heure serveur: {result[0]}")
            print(f"📦 Version PostgreSQL: {result[1][:50]}...")
        
        await conn.close()
        print("\n🎉 La connexion fonctionne!")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        print("\n💡 Vérifiez:")
        print("   1. Que votre projet Supabase est actif (non en pause)")
        print("   2. Que vous utilisez la bonne connection string depuis Supabase")
        print("   3. Dans Supabase Dashboard > Settings > Database")
        print("   4. Vérifiez la section 'Connection string' ou 'Connection pooling'")
        print("   5. Assurez-vous d'utiliser le format 'Direct connection' ou 'Transaction'")
        exit(1)

if __name__ == "__main__":
    asyncio.run(test_direct())

