"""
Vercel Serverless Function Entry Point for Rose Glass Platform
"""
import sys
import os

# Add parent directory to path so we can import from src
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import the serverless-compatible FastAPI app
try:
    from src.server_serverless import app
    from mangum import Mangum

    # Wrap FastAPI app with Mangum for serverless execution
    handler = Mangum(app, lifespan="off")

except Exception as e:
    # Fallback minimal app if import fails
    from fastapi import FastAPI
    from mangum import Mangum

    app = FastAPI()

    @app.get("/")
    def root():
        return {"error": "Import failed", "details": str(e), "traceback": str(e.__traceback__)}

    handler = Mangum(app, lifespan="off")
