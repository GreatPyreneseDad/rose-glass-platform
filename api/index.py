"""
Vercel Serverless Function Entry Point for Rose Glass Platform
"""
import sys
import os

# Add parent directory to path so we can import from src
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import app from server
from src.server import app

# Export for Vercel (must be named 'app')
__all__ = ['app']
