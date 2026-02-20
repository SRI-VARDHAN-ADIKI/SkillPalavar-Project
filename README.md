# SkillPalavar — Intelligent AI Assistant for Tech Support & Field Service

An enterprise-grade **Agentic AI chatbot** for IT support and field service teams. Powered by **Gemini 1.5 Pro**, **LangChain AgentExecutor**, **FAISS vector search**, and a **React + Vite** frontend.

---

## Architecture

```
Frontend (React + Vite)  ──►  Backend (FastAPI)  ──►  AgentExecutor (LangChain)
     port 5173                    port 8000              │
                                                         ├── search_it_knowledge_base  (FAISS RAG)
                                                         ├── create_support_ticket
                                                         ├── check_warranty_status
                                                         └── escalate_to_tier2
```

- **LLM**: Gemini 1.5 Pro via `langchain-google-genai`
- **Embeddings**: Local `all-MiniLM-L6-v2` (sentence-transformers, no API key needed)
- **Vector Store**: FAISS — auto-built from knowledge base on first run, persisted to disk

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.10 or higher |
| Node.js | 18 or higher |
| npm | 9 or higher |
| Git | any recent version |

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/SRI-VARDHAN-ADIKI/SkillPalavar-Project.git
cd SkillPalavar-Project
```

### 2. Backend setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API key

Create a `.env` file inside the `backend/` folder:

```bash
# backend/.env
GEMINI_API_KEY=your_gemini_api_key_here
```

Get a free Gemini API key at: https://aistudio.google.com/app/apikey

### 4. Frontend setup

```bash
cd ../frontend
npm install
```

---

## Running the Project

You need **two terminals** — one for the backend, one for the frontend.

### Terminal 1 — Start the backend

```bash
cd backend
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

uvicorn main:app --reload --port 8000
```

Wait until you see:
```
INFO: AgentExecutor built with 4 tools: [...]
INFO: === Backend is ready. Agentic AI engine online. ===
INFO: Application startup complete.
```

> **Note:** The first run downloads the `all-MiniLM-L6-v2` embedding model (~80 MB) and builds the FAISS index. Subsequent starts load from cache and are much faster.

### Terminal 2 — Start the frontend

```bash
cd frontend
npm run dev
```

Open your browser at: **http://localhost:5173**

---

## Usage

The AI agent autonomously decides which tools to use based on your query. Try these example prompts:

**Simple knowledge lookup:**
> My ThinkPad T14s screen is flickering randomly. What should I do?

**Warranty check:**
> Check the warranty status for device serial number SN-DELL-2024-001

**Ticket creation:**
> Create a support ticket for a Dell XPS 15 with severe battery drain.

**Multi-tool chain (best demo):**
> My HP EliteBook keeps dropping Wi-Fi every 30 minutes. Search for known fixes, create a ticket, and escalate to Tier 2.

The UI shows a **tool activity bar** on each response indicating which agent tools were invoked.

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| `GET` | `/` | Health check |
| `GET` | `/api/health` | Detailed health status |
| `POST` | `/api/chat` | Send a message to the agent |
| `GET` | `/docs` | Interactive Swagger UI |

### POST `/api/chat` — Request body

```json
{
  "message": "My laptop screen is flickering",
  "chat_history": [
    { "role": "user", "content": "Hello" },
    { "role": "assistant", "content": "Hi! How can I help?" }
  ]
}
```

### Response

```json
{
  "response": "Based on the knowledge base...",
  "tool_calls": ["Knowledge Base Search", "Create Support Ticket"]
}
```

---

## Project Structure

```
SkillPalavar-Project/
├── backend/
│   ├── main.py              # FastAPI app, routes, lifespan
│   ├── ai_engine.py         # AgentExecutor, tools, FAISS, embeddings
│   ├── mock_data.py         # 8 IT support knowledge documents
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # API key template
│   └── faiss_index/         # Auto-generated vector index (gitignored)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── ChatInterface.jsx   # Main chat UI with tool activity bar
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── .gitignore
└── README.md
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite 5, Axios, react-markdown, lucide-react |
| Backend | FastAPI, Uvicorn, Pydantic |
| LLM | Gemini 1.5 Pro (`langchain-google-genai 2.x`) |
| Agent | LangChain 0.3.x `AgentExecutor` + `create_tool_calling_agent` |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` (local, CPU) |
| Vector Store | FAISS (`faiss-cpu`) |

---

## Troubleshooting

**Backend won't start — module not found**
```bash
pip install -r requirements.txt
```

**FAISS index corrupted or stale**
```bash
cd backend
rm -rf faiss_index/   # macOS/Linux
# or
Remove-Item -Recurse -Force faiss_index  # Windows PowerShell
```
Restart the backend — it will rebuild automatically.

**Gemini API error (401 / invalid key)**  
Check that `backend/.env` exists and contains a valid `GEMINI_API_KEY`.

**Frontend can't reach backend (CORS / network error)**  
Ensure the backend is running on port `8000` before starting the frontend.
