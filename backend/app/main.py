from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.core.config import settings
from app.db.session import init_db


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description="AI-Powered Market Reaction Simulator API",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def on_startup() -> None:
        init_db()

    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_application()
