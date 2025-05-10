# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import items
from .config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://trade-republic-replica-ui.vercel.app/"],  # Correct frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Allow specific HTTP methods
    allow_headers=["*"],  # Allow all headers or specify as needed
)

# Include routers
app.include_router(items.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Backend. Visit /docs for API documentation."}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
