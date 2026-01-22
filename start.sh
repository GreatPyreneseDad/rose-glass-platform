#!/bin/bash

# Rose Glass Platform - Start Script

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🌹 Rose Glass Platform${NC}"
echo "Every message perceived. Every response calibrated."
echo ""

# Check for virtual environment
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -q -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env from template...${NC}"
    cp .env.template .env
    echo -e "${RED}⚠️  Please edit .env with your API keys${NC}"
    echo ""
fi

# Load environment
export $(grep -v '^#' .env | xargs)

# Check for API keys
if [ -z "$ANTHROPIC_API_KEY" ] || [ "$ANTHROPIC_API_KEY" = "your-anthropic-key-here" ]; then
    if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your-openai-key-here" ]; then
        echo -e "${RED}⚠️  No valid API keys found in .env${NC}"
        echo "Please set ANTHROPIC_API_KEY or OPENAI_API_KEY"
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}Starting server on http://localhost:8420${NC}"
echo ""
echo "Endpoints:"
echo "  POST /v1/chat/completions  - OpenAI-compatible chat"
echo "  POST /v1/perceive          - Perception only"
echo "  GET  /v1/conversations     - List conversations"
echo ""

# Start server
python -m uvicorn src.server:app --host ${HOST:-0.0.0.0} --port ${PORT:-8420} --reload
