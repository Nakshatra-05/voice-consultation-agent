from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Voice Consultation Agent API is running!"}
