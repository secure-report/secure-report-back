from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, reports, media, chat

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    """Conecta a MongoDB al iniciar"""
    from app.db import mongo

@app.get("/api/health")
async def health():
    """Verifica estado del servidor"""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": f"Bienvenido a {settings.APP_NAME}",
        "docs": "/docs"
    }

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(media.router, prefix="/api/media", tags=["Media"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)