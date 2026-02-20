import os
import uuid
import datetime
import logging
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage

from mock_data import MOCK_IT_DOCUMENTS

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FAISS_INDEX_DIR = "./faiss_index"

# ---------------------------------------------------------------------------
# Global vector store reference (set during startup, used inside tools)
# ---------------------------------------------------------------------------
_vector_store: FAISS | None = None

_EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # ~80MB, fast, local — no API key needed
_embeddings_instance: HuggingFaceEmbeddings | None = None


def get_embeddings() -> HuggingFaceEmbeddings:
    """Return a cached instance of the local HuggingFace embedding model."""
    global _embeddings_instance
    if _embeddings_instance is None:
        logger.info("Loading local embedding model '%s'...", _EMBEDDING_MODEL)
        _embeddings_instance = HuggingFaceEmbeddings(
            model_name=_EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
        logger.info("Embedding model loaded.")
    return _embeddings_instance


# ---------------------------------------------------------------------------
# AGENT TOOLS
# ---------------------------------------------------------------------------

@tool
def search_it_knowledge_base(query: str) -> str:
    """Search the internal IT knowledge base for troubleshooting guides,
    hardware repair procedures, driver fixes, OS recovery steps, and technical
    documentation for enterprise laptops and PCs. Always use this tool first
    when a user reports any hardware or software issue."""
    if _vector_store is None:
        return "ERROR: Knowledge base is not available. Cannot retrieve documentation."
    docs = _vector_store.similarity_search(query, k=3)
    if not docs:
        return "No relevant documentation found in the knowledge base for this query."
    chunks = [f"[Chunk {i + 1}]\n{d.page_content}" for i, d in enumerate(docs)]
    return "\n\n---\n\n".join(chunks)


@tool
def create_support_ticket(issue_summary: str, laptop_model: str, priority: str = "Medium") -> str:
    """Create a formal IT support ticket to track the user's issue in the
    enterprise ticketing system. Use this for every reported issue so it can
    be tracked, assigned, and followed up. Priority must be one of: Low,
    Medium, High, Critical."""
    valid_priorities = {"Low", "Medium", "High", "Critical"}
    if priority not in valid_priorities:
        priority = "Medium"
    ticket_id = f"INC-{uuid.uuid4().hex[:8].upper()}"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    sla_map = {
        "Critical": "1 hour response / 4 hour resolution",
        "High": "2 hour response / 8 hour resolution",
        "Medium": "4 hour response / 24 hour resolution",
        "Low": "8 hour response / 72 hour resolution",
    }
    return (
        f"**Ticket Created Successfully**\n\n"
        f"- **Ticket ID**: `{ticket_id}`\n"
        f"- **Issue**: {issue_summary}\n"
        f"- **Device**: {laptop_model}\n"
        f"- **Priority**: {priority}\n"
        f"- **SLA**: {sla_map[priority]}\n"
        f"- **Created**: {timestamp}\n"
        f"- **Status**: Open — Assigned to IT Support Queue\n"
        f"- **Tracking**: it-portal.company.internal/tickets/{ticket_id}"
    )


@tool
def check_warranty_status(laptop_model: str) -> str:
    """Check the warranty status, coverage type, and expiry date for a
    specific laptop model. Use this when hardware replacement or repair
    authorization is being discussed."""
    model_lower = laptop_model.lower()

    warranty_db = {
        "thinkpad": {
            "plan": "3-Year Lenovo Premier Support",
            "expires": "2026-12-31",
            "coverage": "Parts, labor, on-site next-business-day service, accidental damage protection",
            "contact": "1-800-426-7378 | support.lenovo.com",
        },
        "dell xps": {
            "plan": "3-Year Dell ProSupport Plus",
            "expires": "2026-09-15",
            "coverage": "Hardware repair, accidental damage, next-business-day on-site, Keep Your Hard Drive",
            "contact": "1-800-624-9897 | dell.com/support",
        },
        "dell latitude": {
            "plan": "3-Year Dell ProSupport",
            "expires": "2027-03-20",
            "coverage": "Parts & labor, next-business-day on-site hardware support",
            "contact": "1-800-624-9897 | dell.com/support",
        },
        "macbook": {
            "plan": "AppleCare+ for Enterprise (3 Years)",
            "expires": "2026-07-01",
            "coverage": "Hardware defects, battery service, 2 incidents of accidental damage per year",
            "contact": "1-800-275-2273 | apple.com/support",
        },
        "hp elitebook": {
            "plan": "3-Year HP Care Pack (Next Business Day On-Site)",
            "expires": "2027-01-10",
            "coverage": "Parts, labor, on-site repair, defective media retention",
            "contact": "1-800-474-6836 | support.hp.com",
        },
        "surface": {
            "plan": "Microsoft Complete for Business (2 Years)",
            "expires": "2026-05-22",
            "coverage": "Hardware defects, accidental damage (limited), Microsoft Store service",
            "contact": "1-800-642-7676 | support.microsoft.com",
        },
        "zenbook": {
            "plan": "2-Year ASUS Commercial Warranty",
            "expires": "2026-11-30",
            "coverage": "Manufacturing defects, parts & labor, mail-in service",
            "contact": "1-888-678-3688 | asus.com/support",
        },
        "ideapad": {
            "plan": "2-Year Lenovo Standard Warranty",
            "expires": "2026-08-14",
            "coverage": "Parts & labor, depot/mail-in service",
            "contact": "1-800-426-7378 | support.lenovo.com",
        },
    }

    matched_brand = None
    for key in warranty_db:
        if key in model_lower:
            matched_brand = key
            break

    if not matched_brand:
        return (
            f"**Warranty Status: Not Found**\n\n"
            f"No warranty record found for model: **{laptop_model}**\n\n"
            f"Please check the device serial number at the manufacturer's support portal "
            f"or contact the IT Asset Management team at assets@company.com."
        )

    w = warranty_db[matched_brand]
    expiry = datetime.datetime.strptime(w["expires"], "%Y-%m-%d")
    today = datetime.datetime.now()
    days_remaining = (expiry - today).days
    status = "Active" if days_remaining > 0 else "Expired"
    days_label = f"{days_remaining} days remaining" if days_remaining > 0 else f"expired {abs(days_remaining)} days ago"

    return (
        f"**Warranty Status for {laptop_model}**\n\n"
        f"- **Status**: {status} ({days_label})\n"
        f"- **Plan**: {w['plan']}\n"
        f"- **Expiry Date**: {w['expires']}\n"
        f"- **Coverage**: {w['coverage']}\n"
        f"- **Support Contact**: {w['contact']}"
    )


@tool
def escalate_to_tier2(issue_summary: str, ticket_id: str = "") -> str:
    """Escalate a complex or unresolvable issue to Tier 2 IT Support specialists.
    Use this when the knowledge base does not contain a solution, when hardware
    replacement is confirmed needed, or when the issue is business-critical.
    Optionally pass an existing ticket_id to link the escalation."""
    escalation_id = f"ESC-{uuid.uuid4().hex[:6].upper()}"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    ticket_ref = f" (linked to `{ticket_id}`)" if ticket_id else ""

    return (
        f"**Escalated to Tier 2 IT Support**{ticket_ref}\n\n"
        f"- **Escalation ID**: `{escalation_id}`\n"
        f"- **Issue Summary**: {issue_summary}\n"
        f"- **Escalated At**: {timestamp}\n"
        f"- **Tier 2 Team**: Senior Field Engineers & Systems Specialists\n"
        f"- **Expected Response**: Within 2 business hours\n"
        f"- **Contact Options**:\n"
        f"  - Email: tier2-support@company.com\n"
        f"  - Phone: Extension 4357 (HELP)\n"
        f"  - Teams: #it-tier2-support\n\n"
        f"A Tier 2 specialist will review the case and contact the user directly."
    )


# ---------------------------------------------------------------------------
# AGENT SYSTEM PROMPT
# ---------------------------------------------------------------------------

AGENT_SYSTEM_PROMPT = """You are **SkillPalavar IT Assistant** — an expert Agentic IT Support Agent for an enterprise organization. You operate autonomously using specialized tools to diagnose and resolve hardware and software issues for employees and field technicians.

## YOUR TOOLS & WHEN TO USE THEM

1. **search_it_knowledge_base** — ALWAYS call this first for any technical issue. Search with the issue description and laptop model for best results.
2. **create_support_ticket** — Create a ticket for EVERY reported issue after you have the issue details and laptop model. Set priority based on severity (Critical = cannot work at all, High = major function broken, Medium = degraded performance, Low = cosmetic or minor).
3. **check_warranty_status** — Call this whenever hardware repair or part replacement is mentioned or recommended by the knowledge base.
4. **escalate_to_tier2** — Use when: the knowledge base has no solution, hardware failure is confirmed, or the issue is business-critical and unresolved.

## STRICT BEHAVIOR RULES

- **Model Verification**: If the user has NOT mentioned a specific laptop model or brand, you MUST ask for it before calling any tools. Do not assume or guess the model.
- **Always create a ticket**: For every distinct issue, create a support ticket for proper tracking.
- **Recommended tool chain for hardware issues**: search KB → create ticket → check warranty → escalate if needed.
- **Markdown formatting**: Format your final response in clean Markdown with numbered steps, bold labels, and code blocks for terminal commands.
- **No hallucination**: Base troubleshooting steps ONLY on what search_it_knowledge_base returns. If the tool returns no useful results, escalate — never invent steps.
- **Professional tone**: Calm, clear, and thorough at all times."""


# ---------------------------------------------------------------------------
# LLM + EMBEDDINGS
# ---------------------------------------------------------------------------


def get_llm() -> ChatGoogleGenerativeAI:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=api_key,
        temperature=0.1,
    )


# ---------------------------------------------------------------------------
# VECTOR STORE INITIALIZATION
# ---------------------------------------------------------------------------

def initialize_vector_store() -> FAISS:
    global _vector_store
    embeddings = get_embeddings()
    index_file = os.path.join(FAISS_INDEX_DIR, "index.faiss")

    if os.path.exists(index_file):
        logger.info("Loading existing FAISS index from '%s'...", FAISS_INDEX_DIR)
        vs = FAISS.load_local(
            FAISS_INDEX_DIR,
            embeddings,
            allow_dangerous_deserialization=True,
        )
        logger.info("FAISS index loaded successfully.")
        _vector_store = vs
        return vs

    logger.info("No existing FAISS index. Building from mock documents...")
    raw_documents = [
        Document(page_content=doc_text, metadata={"source": f"mock_doc_{idx}"})
        for idx, doc_text in enumerate(MOCK_IT_DOCUMENTS)
    ]
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = text_splitter.split_documents(raw_documents)
    logger.info("Split %d raw documents into %d chunks.", len(raw_documents), len(chunks))

    vs = FAISS.from_documents(documents=chunks, embedding=embeddings)
    os.makedirs(FAISS_INDEX_DIR, exist_ok=True)
    vs.save_local(FAISS_INDEX_DIR)
    logger.info("FAISS index saved at '%s' with %d chunks.", FAISS_INDEX_DIR, len(chunks))
    _vector_store = vs
    return vs


# ---------------------------------------------------------------------------
# AGENT EXECUTOR BUILDER
# ---------------------------------------------------------------------------

AGENT_TOOLS = [
    search_it_knowledge_base,
    create_support_ticket,
    check_warranty_status,
    escalate_to_tier2,
]

TOOL_DISPLAY_NAMES = {
    "search_it_knowledge_base": "Searching Knowledge Base",
    "create_support_ticket": "Creating Support Ticket",
    "check_warranty_status": "Checking Warranty Status",
    "escalate_to_tier2": "Escalating to Tier 2",
}


def build_agent_executor(vector_store: FAISS) -> AgentExecutor:
    global _vector_store
    _vector_store = vector_store
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", AGENT_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm=llm, tools=AGENT_TOOLS, prompt=prompt)
    executor = AgentExecutor(
        agent=agent,
        tools=AGENT_TOOLS,
        verbose=True,
        max_iterations=6,
        handle_parsing_errors=True,
    )
    logger.info("AgentExecutor built with %d tools: %s", len(AGENT_TOOLS), [t.name for t in AGENT_TOOLS])
    return executor


# ---------------------------------------------------------------------------
# MAIN INFERENCE FUNCTION
# ---------------------------------------------------------------------------

def get_agent_response(
    agent_executor: AgentExecutor,
    user_message: str,
    chat_history: list[dict] | None = None,
) -> tuple[str, list[str]]:
    """
    Run the user message through the agent executor.
    Returns (response_text, list_of_tool_display_names_used).
    """
    try:
        invoke_input: dict = {"input": user_message}
        if chat_history:
            lc_history = []
            for msg in chat_history:
                if msg.get("role") == "user":
                    lc_history.append(HumanMessage(content=msg["content"]))
                elif msg.get("role") == "bot":
                    lc_history.append(AIMessage(content=msg["content"]))
            if lc_history:
                invoke_input["chat_history"] = lc_history

        result = agent_executor.invoke(invoke_input)
        response_text = result.get("output", "")

        tools_used: list[str] = []
        for action, _ in result.get("intermediate_steps", []):
            raw_name = getattr(action, "tool", None)
            display = TOOL_DISPLAY_NAMES.get(raw_name, raw_name)
            if display and display not in tools_used:
                tools_used.append(display)

        if not response_text:
            response_text = "I was unable to generate a response. Please rephrase your question."

        return response_text, tools_used

    except Exception as exc:
        logger.error("Error during agent execution: %s", exc, exc_info=True)
        return (
            "I'm experiencing a technical issue and cannot process your request right now. "
            "Please try again or contact Tier 2 IT Support at extension 4357.",
            [],
        )
