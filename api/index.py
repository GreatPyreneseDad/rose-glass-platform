"""
Vercel Serverless Function Entry Point for Rose Glass Platform
Vercel's @vercel/python builder supports ASGI apps natively via 'app' variable
"""
import sys
import os

# Add parent directory to path so we can import from src
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import the serverless-compatible FastAPI app
# Vercel expects an 'app' variable for ASGI applications
try:
    from src.server_serverless import app
except Exception as e:
    # Fallback minimal app if import fails
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    @app.get("/api")
    @app.get("/api/")
    def root():
        import traceback
        return {
            "error": "Import failed",
            "details": str(e),
            "traceback": traceback.format_exc()
        }
