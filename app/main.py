from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.ai import router as ai_router
from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router
from app.api.documents import router as documents_router
from app.api.incidents import router as incidents_router
from app.config import settings
from app.db.init_db import init_db

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    init_db()


app.include_router(auth_router, prefix="/api/auth")
app.include_router(incidents_router, prefix="/api/incidents")
app.include_router(dashboard_router, prefix="/api/dashboard")
app.include_router(ai_router, prefix="/api/ai")
app.include_router(documents_router, prefix="/api/documents")


@app.get("/")
def root():
    return {"message": f"{settings.app_name} is running"}
