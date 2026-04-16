from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_health import router as health_router
from app.api.routes_review import router as review_router
from app.api.routes_repo import router as repo_router
from app.api.routes_github import router as github_router
from app.db.init_db import init_db
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(review_router)
app.include_router(repo_router)
app.include_router(github_router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def home():
    return {
        "name": settings.APP_NAME,
        "env": settings.APP_ENV,
        "status": "running"
    }
