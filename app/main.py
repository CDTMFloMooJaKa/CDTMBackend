# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from .routers import items
from .config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

token = "gmcIxYK0t6aWHYa5"
MONGO_URI = f"mongodb+srv://userCDTM:{token}@cluster0.nr8w3o8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0""

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect MongoDB
    app.mongodb_client = AsyncIOMotorClient(MONGO_URI)
    app.mongodb = app.mongodb_client["trading_sample_data"]
    await app.mongodb.command("ping")
    print("✅ Connected to MongoDB")

    yield  # App runs here

    # Shutdown: close MongoDB
    app.mongodb_client.close()
    print("❌ MongoDB connection closed")

# Include your router
app.include_router(items.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Backend. Visit /docs for API documentation."}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
