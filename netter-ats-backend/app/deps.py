import os
from fastapi import Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "change-me-in-prod")


def enable_cors(app):
    # Autorise ton futur front local (Nuxt) et tests directs
    origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",   # Vite dev server si besoin
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "*",  # pour dev uniquement; ensuite restreins
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


async def verify_admin_api_key(x_api_key: str = Header(..., alias="x-api-key")):
    """Vérifie que l'API key admin est valide. Accepte X-API-Key ou x-api-key."""
    if x_api_key != ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing admin API key"
        )
    return x_api_key

