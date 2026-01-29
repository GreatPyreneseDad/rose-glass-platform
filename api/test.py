"""
Minimal test endpoint for Vercel
"""
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "message": "Test endpoint working"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# Mangum handler for Vercel
handler = Mangum(app, lifespan="off")
