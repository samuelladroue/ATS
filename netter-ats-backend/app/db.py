import os
from contextlib import asynccontextmanager
from psycopg_pool import AsyncConnectionPool
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Pool de connexions PostgreSQL
pool: AsyncConnectionPool | None = None


async def init_db():
    """Initialise le pool de connexions à la base de données."""
    global pool
    pool = AsyncConnectionPool(
        conninfo=DATABASE_URL,
        min_size=1,
        max_size=10,
    )
    await pool.open()


async def close_db():
    """Ferme le pool de connexions."""
    global pool
    if pool:
        await pool.close()


@asynccontextmanager
async def get_db():
    """Context manager pour obtenir une connexion depuis le pool."""
    if not pool:
        raise RuntimeError("Database pool not initialized. Call init_db() first.")
    async with pool.connection() as conn:
        yield conn


async def check_db_connection() -> bool:
    """Vérifie que la connexion à la base de données fonctionne."""
    try:
        async with get_db() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT now();")
                await cur.fetchone()
        return True
    except Exception:
        return False

