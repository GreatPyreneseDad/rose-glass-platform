"""
Minimal test endpoint for Vercel
Vercel's @vercel/python builder supports ASGI apps natively via 'app' variable
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
@app.get("/test")
@app.get("/test/")
def root():
    return {"status": "ok", "message": "Test endpoint working"}

@app.get("/test/health")
def health():
    return {"status": "healthy"}
