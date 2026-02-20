import logging
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from ai_engine import initialize_vector_store, build_agent_executor, get_agent_response

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app_state: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=== SkillPalavar Agentic IT Assistant Backend Starting Up ===")
    try:
        logger.info("Initializing FAISS vector store...")
        vector_store = initialize_vector_store()
        app_state["vector_store"] = vector_store

        logger.info("Building AgentExecutor with 4 tools (search, ticket, warranty, escalate)...")
        agent_executor = build_agent_executor(vector_store)
        app_state["agent_executor"] = agent_executor

        logger.info("=== Backend is ready. Agentic AI engine online. ===")
    except Exception as exc:
        logger.critical("FATAL: Failed to initialize AI engine on startup: %s", exc, exc_info=True)
        app_state["startup_error"] = str(exc)

    yield

    logger.info("=== SkillPalavar Backend Shutting Down ===")
    app_state.clear()


app = FastAPI(
    title="SkillPalavar Agentic IT Assistant API",
    description="Agentic AI-powered IT Support Assistant with autonomous tool use for enterprise field service.",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# REQUEST / RESPONSE MODELS
# ---------------------------------------------------------------------------

class HistoryMessage(BaseModel):
    role: str = Field(..., description="'user' or 'bot'")
    content: str = Field(..., description="Message text content")


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The user's IT support question or issue description.",
    )
    chat_history: Optional[List[HistoryMessage]] = Field(
        default=None,
        description="Previous conversation turns for multi-turn context.",
    )


class ChatResponse(BaseModel):
    response: str = Field(..., description="The agent's final response in Markdown format.")
    tool_calls: List[str] = Field(
        default=[],
        description="List of tool display names the agent invoked to produce this response.",
    )


# ---------------------------------------------------------------------------
# ENDPOINTS
# ---------------------------------------------------------------------------

@app.get("/", tags=["Health"])
async def root():
    if "startup_error" in app_state:
        return {"status": "degraded", "error": app_state["startup_error"]}
    return {
        "status": "healthy",
        "message": "SkillPalavar Agentic IT Assistant API v2.0 is running.",
        "architecture": "LangChain AgentExecutor + Gemini 1.5 Pro + FAISS RAG",
        "tools": ["search_it_knowledge_base", "create_support_ticket", "check_warranty_status", "escalate_to_tier2"],
        "docs": "/docs",
    }


@app.get("/api/health", tags=["Health"])
async def health_check():
    if "startup_error" in app_state:
        raise HTTPException(status_code=503, detail=f"AI engine failed: {app_state['startup_error']}")
    if "agent_executor" not in app_state:
        raise HTTPException(status_code=503, detail="Agent executor is not yet initialized.")
    return {
        "status": "healthy",
        "components": {
            "vector_store": "faiss",
            "agent": "AgentExecutor",
            "llm": "gemini-1.5-pro",
            "tools": 4,
        },
    }


@app.post("/api/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Main agentic chat endpoint. The agent autonomously decides which tools to
    call (knowledge base search, ticket creation, warranty check, escalation)
    based on the user's message and conversation history.
    """
    if "startup_error" in app_state:
        raise HTTPException(
            status_code=503,
            detail="The AI engine failed to initialize. Please contact your system administrator.",
        )

    agent_executor = app_state.get("agent_executor")
    if agent_executor is None:
        raise HTTPException(status_code=503, detail="The AI agent is not yet ready. Please try again.")

    logger.info("Received chat request. Message: %.80s...", request.message)

    history = [msg.model_dump() for msg in request.chat_history] if request.chat_history else None
    response_text, tool_calls = get_agent_response(agent_executor, request.message, history)

    logger.info("Agent response ready. Tools used: %s", tool_calls)
    return ChatResponse(response=response_text, tool_calls=tool_calls)
