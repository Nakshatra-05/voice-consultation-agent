from fastapi import FastAPI
from app.api.voice_routes import router as voice_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Root route working"}

@app.get("/health")
def health_check():
    return {"status": "OK", "message": "Voice Consultation Agent is running"}

app.include_router(voice_router, prefix="/voice")
