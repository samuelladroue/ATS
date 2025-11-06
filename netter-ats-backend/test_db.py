"""
Script de test pour vérifier la connexion à la base de données PostgreSQL.
"""
import asyncio
import os
from dotenv import load_dotenv
from psycopg_pool import AsyncConnectionPool

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ ERREUR: DATABASE_URL n'est pas défini dans le fichier .env")
    exit(1)


async def test_connection():
    """Teste la connexion à la base de données."""
    print("🔄 Connexion à la base de données...")
    
    pool = AsyncConnectionPool(
        conninfo=DATABASE_URL,
        min_size=1,
        max_size=1,
    )
    await pool.open()
    
    try:
        async with pool.connection() as conn:
            async with conn.cursor() as cur:
                print("✅ Connexion établie!")
                print("🔄 Exécution de SELECT now();...")
                
                await cur.execute("SELECT now();")
                result = await cur.fetchone()
                
                print(f"✅ Requête réussie!")
                print(f"📅 Heure serveur: {result[0]}")
                print("\n🎉 La connexion à PostgreSQL fonctionne correctement!")
                
    except Exception as e:
        print(f"❌ ERREUR lors de la connexion: {e}")
        print("\n💡 Vérifiez:")
        print("   - Que votre URL DATABASE_URL est correcte dans .env")
        print("   - Que votre mot de passe Supabase est correct")
        print("   - Que votre base de données Supabase est accessible")
        exit(1)
    finally:
        if pool:
            await pool.close()


if __name__ == "__main__":
    asyncio.run(test_connection())

