"""
Minimal test endpoint for Vercel
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "message": "Test endpoint working"}

@app.get("/health")
def health():
    return {"status": "healthy"}
