from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.databases import sql
from app.routers.books import router as books_router
from app.routers.comments import router as comments_router
from app.routers.quotes import router as quotes_router
from app.routers.catalog import router as catalog_router
import logging

def get_application():
    
    sql.Base.metadata.create_all(bind=sql.engine)

    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.include_router(books_router)
    _app.include_router(comments_router)
    _app.include_router(quotes_router)
    _app.include_router(catalog_router)
    
    logging.info("Start app...")

    return _app


app = get_application()
