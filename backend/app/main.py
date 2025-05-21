from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import youtube, settings

app = FastAPI(
    title="Social Mantra AI API",
    description="API for Social Media Marketing and Niche Analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(youtube.router)
app.include_router(settings.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Social Mantra AI API"}
