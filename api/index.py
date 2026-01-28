"""
Vercel Serverless Function Entry Point for Rose Glass Platform
"""
import sys
import os

# Add parent directory to path so we can import from src
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.server import app

# Vercel requires the app to be exported as 'app' or a callable handler
# The FastAPI app can be used directly
handler = app
