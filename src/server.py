"""
Rose Glass Platform v2.1 - LLM Proxy Server
Every message perceived. Every response calibrated.
With cultural lens selection and extended dimensions (τ, λ)
"""

import os
from dotenv import load_dotenv
load_dotenv()  # Load .env file
import json
import time
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import httpx

from src.rose_lens import get_lens, Perception, RoseLens, CULTURAL_LENSES
from src.calibrator import get_calibrator
from src.db import get_db, init_db


# ============== Models ==============

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 4096
    stream: Optional[bool] = False
    lens: Optional[str] = None  # Cultural lens for Rose Glass v2.1
    
class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: str

class ChatResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[Choice]
    usage: Usage
    rose_glass: Optional[Dict[str, Any]] = None


# ============== App ==============

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    print("🌹 Rose Glass Platform v2.1 initialized")
    print(f"   Available lenses: {', '.join(CULTURAL_LENSES.keys())}")
    yield
    # Shutdown
    print("🌹 Rose Glass Platform shutting down")

app = FastAPI(
    title="Rose Glass Platform",
    description="LLM proxy with perception and calibration - v2.1 with cultural lenses",
    version="2.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Core Logic ==============

lens = get_lens()
calibrator = get_calibrator()

# Provider configurations
PROVIDERS = {
    "anthropic": {
        "base_url": "https://api.anthropic.com/v1",
        "models": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku", "claude-sonnet-4", "claude-opus-4"],
        "env_key": "ANTHROPIC_API_KEY"
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4o"],
        "env_key": "OPENAI_API_KEY"
    }
}


def detect_provider(model: str) -> str:
    """Detect which provider to use based on model name."""
    model_lower = model.lower()
    if "claude" in model_lower:
        return "anthropic"
    elif "gpt" in model_lower:
        return "openai"
    else:
        return "openai"


async def call_anthropic(
    messages: List[Message],
    model: str,
    system_injection: str,
    temperature: float,
    max_tokens: int,
    api_key: str
) -> tuple[str, int, int]:
    """Call Anthropic API with Rose Glass injection."""
    
    anthropic_messages = []
    system_content = system_injection
    
    for msg in messages:
        if msg.role == "system":
            system_content = f"{system_injection}\n\n{msg.content}"
        else:
            anthropic_messages.append({
                "role": msg.role,
                "content": msg.content
            })
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": model,
                "max_tokens": max_tokens,
                "system": system_content,
                "messages": anthropic_messages
            },
            timeout=120.0
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
        data = response.json()
        content = data["content"][0]["text"]
        input_tokens = data["usage"]["input_tokens"]
        output_tokens = data["usage"]["output_tokens"]
        
        return content, input_tokens, output_tokens


async def call_openai(
    messages: List[Message],
    model: str,
    system_injection: str,
    temperature: float,
    max_tokens: int,
    api_key: str
) -> tuple[str, int, int]:
    """Call OpenAI API with Rose Glass injection."""
    
    openai_messages = []
    has_system = False
    
    for msg in messages:
        if msg.role == "system":
            has_system = True
            openai_messages.append({
                "role": "system",
                "content": f"{system_injection}\n\n{msg.content}"
            })
        else:
            openai_messages.append({
                "role": msg.role,
                "content": msg.content
            })
    
    if not has_system:
        openai_messages.insert(0, {
            "role": "system",
            "content": system_injection
        })
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": openai_messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            },
            timeout=120.0
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        input_tokens = data["usage"]["prompt_tokens"]
        output_tokens = data["usage"]["completion_tokens"]
        
        return content, input_tokens, output_tokens


# ============== Endpoints ==============

@app.get("/")
async def root():
    return {
        "name": "Rose Glass Platform",
        "version": "2.1.0",
        "status": "operational",
        "available_lenses": list(CULTURAL_LENSES.keys()),
        "message": "Translation, not measurement. Understanding, not judgment."
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.get("/v1/lenses")
async def list_lenses():
    """List available cultural lenses with descriptions."""
    return {
        lens_name: {
            "name": lens_name,
            "description": lens_cal.description,
            "km": lens_cal.km,
            "ki": lens_cal.ki,
            "weights": {
                "psi": lens_cal.psi_weight,
                "rho": lens_cal.rho_weight,
                "q": lens_cal.q_weight,
                "f": lens_cal.f_weight
            }
        }
        for lens_name, lens_cal in CULTURAL_LENSES.items()
    }


@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_completions(
    request: ChatRequest,
    authorization: Optional[str] = Header(None),
    x_api_key: Optional[str] = Header(None)
):
    """
    OpenAI-compatible chat completions endpoint.
    Messages are perceived through Rose Glass v2.1.
    Responses are calibrated to user state.
    Supports cultural lens selection.
    """
    
    # Get API key
    api_key = None
    if authorization and authorization.startswith("Bearer "):
        api_key = authorization[7:]
    elif x_api_key:
        api_key = x_api_key
    
    provider = detect_provider(request.model)
    
    if not api_key:
        env_key = PROVIDERS[provider]["env_key"]
        api_key = os.getenv(env_key)
    
    if not api_key:
        raise HTTPException(
            status_code=401, 
            detail=f"No API key provided. Set {PROVIDERS[provider]['env_key']} or pass in header."
        )
    
    # Get the last user message for perception
    user_message = None
    for msg in reversed(request.messages):
        if msg.role == "user":
            user_message = msg.content
            break
    
    # Perceive through Rose Glass v2.1 with selected lens
    perception = lens.perceive(
        text=user_message or "",
        lens_name=request.lens,  # Use lens from request
        multi_lens=True  # Always calculate λ
    )
    
    # Generate calibrated system injection
    system_injection = calibrator.generate_system_injection(perception)
    
    # Call appropriate provider
    start_time = time.time()
    
    if provider == "anthropic":
        content, input_tokens, output_tokens = await call_anthropic(
            messages=request.messages,
            model=request.model,
            system_injection=system_injection,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            api_key=api_key
        )
    else:
        content, input_tokens, output_tokens = await call_openai(
            messages=request.messages,
            model=request.model,
            system_injection=system_injection,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            api_key=api_key
        )
    
    elapsed = time.time() - start_time
    
    # Store conversation in database
    db = get_db()
    conversation_id = str(uuid.uuid4())
    db.log_exchange(
        conversation_id=conversation_id,
        user_message=user_message or "",
        assistant_message=content,
        perception=perception.to_dict(),
        model=request.model,
        elapsed_seconds=elapsed
    )
    
    # Build response
    return ChatResponse(
        id=f"chatcmpl-{conversation_id[:8]}",
        created=int(time.time()),
        model=request.model,
        choices=[
            Choice(
                index=0,
                message=Message(role="assistant", content=content),
                finish_reason="stop"
            )
        ],
        usage=Usage(
            prompt_tokens=input_tokens,
            completion_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens
        ),
        rose_glass=perception.to_dict()
    )


@app.post("/v1/perceive")
async def perceive_only(request: Request):
    """
    Perception-only endpoint.
    Analyze text without calling an LLM.
    Supports lens selection and multi-lens comparison.
    """
    body = await request.json()
    text = body.get("text", "")
    selected_lens = body.get("lens", None)
    compare_lenses = body.get("compare_lenses", False)
    
    perception = lens.perceive(
        text=text,
        lens_name=selected_lens,
        multi_lens=True
    )
    
    guidance = calibrator.calibrate(perception)
    
    response = {
        "perception": perception.to_dict(),
        "guidance": {
            "tone": guidance.tone,
            "complexity": guidance.complexity,
            "length": guidance.length,
            "emotional_mirroring": guidance.emotional_mirroring,
            "include_questions": guidance.include_questions,
            "affirmation_level": guidance.affirmation_level,
            "cautions": guidance.cautions
        },
        "system_injection": calibrator.generate_system_injection(perception)
    }
    
    # Include multi-lens comparison if requested
    if compare_lenses and perception.lens_readings:
        response["lens_comparison"] = {
            lr.lens_name: {
                "coherence": round(lr.coherence, 3),
                "q_optimized": round(lr.q_optimized, 3)
            }
            for lr in perception.lens_readings
        }
    
    return response


@app.post("/v1/compare")
async def compare_lenses_endpoint(request: Request):
    """
    Compare how text appears through all cultural lenses.
    Returns coherence scores for each lens.
    """
    body = await request.json()
    text = body.get("text", "")
    
    comparison = lens.compare_lenses(text)
    
    return {
        "text_preview": text[:100] + "..." if len(text) > 100 else text,
        "comparison": comparison,
        "lambda": max(comparison.values()) - min(comparison.values()),  # Spread
        "most_coherent_lens": max(comparison, key=comparison.get),
        "least_coherent_lens": min(comparison, key=comparison.get)
    }


@app.get("/v1/conversations")
async def list_conversations(limit: int = 50):
    """List recent conversations with perceptions."""
    db = get_db()
    return db.get_recent_conversations(limit=limit)


@app.get("/v1/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get a specific conversation."""
    db = get_db()
    conv = db.get_conversation(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8420)
