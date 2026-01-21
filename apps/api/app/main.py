from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.collections import router as collections_router
from app.api.files import router as files_router


from app.core.config import settings
from app.core.logging import setup_logging




setup_logging()

app = FastAPI(title=settings.APP_NAME)

# CORS (we'll tighten this later)
origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(collections_router)
app.include_router(files_router)

