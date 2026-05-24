from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.api import api_router
from .core.database import SessionLocal, engine
from .models import base
from .core import initial_data

# Create database tables
base.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Signature API",
    description="Autonomous AI Business Operating System",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Initialize default data on startup"""
    db = SessionLocal()
    try:
        initial_data.init_agents(db)
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Welcome to Signature API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/health/db")
async def db_health_check():
    # Placeholder for actual database health check
    return {"status": "healthy", "service": "database"}

@app.get("/health/redis")
async def redis_health_check():
    # Placeholder for actual Redis health check
    return {"status": "healthy", "service": "redis"}