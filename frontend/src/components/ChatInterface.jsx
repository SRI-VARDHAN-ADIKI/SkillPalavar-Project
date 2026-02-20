import { useState, useRef, useEffect, useCallback } from 'react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { SendHorizonal, TriangleAlert, Cpu, Laptop, Database, Ticket, ShieldCheck, ArrowUpCircle } from 'lucide-react'

const API_BASE_URL = 'http://localhost:8000'

const SUGGESTIONS = [
  {
    title: 'Screen Flickering',
    desc: 'ThinkPad T14s display issue',
    prompt: 'My ThinkPad T14s Gen 3 screen is flickering and showing artifacts. How do I fix it?',
  },
  {
    title: 'Battery Drain',
    desc: 'Dell XPS 15 power problem',
    prompt: 'My Dell XPS 15 9530 battery drains very fast and only lasts 2 hours.',
  },
  {
    title: 'Boot Loop',
    desc: 'MacBook M2 recovery',
    prompt: 'My MacBook Pro M2 14-inch is stuck in a boot loop and keeps restarting.',
  },
  {
    title: 'Wi-Fi Drops',
    desc: 'HP EliteBook connectivity',
    prompt: 'My HP EliteBook 840 G9 keeps disconnecting from Wi-Fi every few minutes.',
  },
]

// Tool icon + color mapping
const TOOL_META = {
  'Searching Knowledge Base':  { icon: Database,       color: '#58a6ff', bg: 'rgba(56,139,253,0.12)',  border: 'rgba(56,139,253,0.3)'  },
  'Creating Support Ticket':   { icon: Ticket,         color: '#3fb950', bg: 'rgba(63,185,80,0.12)',   border: 'rgba(63,185,80,0.3)'   },
  'Checking Warranty Status':  { icon: ShieldCheck,    color: '#e3b341', bg: 'rgba(227,179,65,0.12)',  border: 'rgba(227,179,65,0.3)'  },
  'Escalating to Tier 2':      { icon: ArrowUpCircle,  color: '#f78166', bg: 'rgba(247,129,102,0.12)', border: 'rgba(247,129,102,0.3)' },
}

function ToolActivityBar({ toolCalls }) {
  if (!toolCalls || toolCalls.length === 0) return null
  return (
    <div className="tool-activity-bar">
      <span className="tool-activity-label">Agent actions:</span>
      {toolCalls.map((name) => {
        const meta = TOOL_META[name] || { icon: Cpu, color: '#8b949e', bg: 'rgba(139,148,158,0.1)', border: 'rgba(139,148,158,0.2)' }
        const Icon = meta.icon
        return (
          <span
            key={name}
            className="tool-badge"
            style={{ color: meta.color, background: meta.bg, border: `1px solid ${meta.border}` }}
          >
            <Icon size={11} />
            {name}
          </span>
        )
      })}
    </div>
  )
}

function TypingIndicator() {
  return (
    <div className="typing-row">
      <div className="message-avatar bot">
        <Cpu size={13} />
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
        <span className="message-sender">IT Assistant</span>
        <div className="typing-bubble">
          <span className="typing-label">Agent is reasoning</span>
          <div className="typing-dot" />
          <div className="typing-dot" />
          <div className="typing-dot" />
        </div>
      </div>
    </div>
  )
}

function MessageBubble({ message }) {
  const isUser = message.role === 'user'
  const isError = message.isError === true

  return (
    <div className={`message-row ${isUser ? 'user' : 'bot'}`}>
      <div className={`message-avatar ${isUser ? 'user' : 'bot'}`}>
        {isUser ? 'FT' : isError ? <TriangleAlert size={13} /> : <Cpu size={13} />}
      </div>
      <div className="message-content-wrapper">
        <span className="message-sender">{isUser ? 'You' : 'IT Assistant'}</span>
        {!isUser && <ToolActivityBar toolCalls={message.toolCalls} />}
        {isUser ? (
          <div className="message-bubble user">{message.content}</div>
        ) : (
          <div className={`message-bubble bot${isError ? ' error' : ''}`}>
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  )
}

function WelcomeScreen({ onSuggestionClick }) {
  return (
    <div className="welcome-screen">
      <div className="welcome-icon">
        <Laptop size={30} />
      </div>
      <h2 className="welcome-title">Agentic IT Support Assistant</h2>
      <p className="welcome-subtitle">
        Powered by <strong style={{ color: 'var(--accent-hover)' }}>Gemini 1.5 Pro</strong> with autonomous tool use.
        The agent searches the knowledge base, creates support tickets, checks warranty status,
        and escalates to Tier 2 — all autonomously based on your issue.
        <br /><br />
        <strong style={{ color: 'var(--accent-hover)' }}>Tip:</strong> Always mention your laptop model for accurate diagnosis.
      </p>
      <div className="agent-capability-row">
        {Object.entries(TOOL_META).map(([name, meta]) => {
          const Icon = meta.icon
          return (
            <div key={name} className="capability-chip" style={{ borderColor: meta.border, color: meta.color, background: meta.bg }}>
              <Icon size={13} />
              <span>{name}</span>
            </div>
          )
        })}
      </div>
      <div className="welcome-suggestions">
        {SUGGESTIONS.map((s) => (
          <button key={s.title} className="suggestion-card" onClick={() => onSuggestionClick(s.prompt)}>
            <div className="suggestion-card-title">{s.title}</div>
            <div className="suggestion-card-desc">{s.desc}</div>
          </button>
        ))}
      </div>
    </div>
  )
}

export default function ChatInterface() {
  const [messages, setMessages] = useState([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)
  const textareaRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  useEffect(() => {
    const ta = textareaRef.current
    if (!ta) return
    ta.style.height = 'auto'
    ta.style.height = `${Math.min(ta.scrollHeight, 160)}px`
  }, [inputValue])

  const sendMessage = useCallback(async (overrideText) => {
    const textToSend = (overrideText ?? inputValue).trim()
    if (!textToSend || isLoading) return

    const userMsg = { role: 'user', content: textToSend, id: Date.now() }
    setMessages((prev) => [...prev, userMsg])
    setInputValue('')
    setIsLoading(true)

    try {
      // Build history from current messages (exclude errors)
      const historyPayload = messages
        .filter((m) => !m.isError)
        .map((m) => ({ role: m.role, content: m.content }))

      const response = await axios.post(
        `${API_BASE_URL}/api/chat`,
        { message: textToSend, chat_history: historyPayload },
        { timeout: 90000, headers: { 'Content-Type': 'application/json' } }
      )

      const botMsg = {
        role: 'bot',
        content: response.data.response,
        toolCalls: response.data.tool_calls || [],
        id: Date.now() + 1,
        isError: false,
      }
      setMessages((prev) => [...prev, botMsg])
    } catch (err) {
      let errorContent = ''
      if (err.code === 'ECONNREFUSED' || err.code === 'ERR_NETWORK') {
        errorContent =
          '**Connection Error:** Unable to reach the backend server.\n\nEnsure the FastAPI server is running:\n```\ncd backend\n.\\venv\\Scripts\\activate\nuvicorn main:app --reload --port 8000\n```'
      } else if (err.code === 'ECONNABORTED') {
        errorContent =
          '**Timeout:** The agent took too long to respond. The LLM may be busy — please try again.'
      } else if (err.response) {
        errorContent = `**Server Error (${err.response.status}):** ${err.response.data?.detail || 'Unknown error.'}`
      } else {
        errorContent = `**Unexpected Error:** ${err.message || 'Something went wrong.'}`
      }
      setMessages((prev) => [
        ...prev,
        { role: 'bot', content: errorContent, toolCalls: [], id: Date.now() + 1, isError: true },
      ])
    } finally {
      setIsLoading(false)
    }
  }, [inputValue, isLoading, messages])

  const handleKeyDown = useCallback((e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }, [sendMessage])

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="chat-header-left">
          <span className="chat-title">IT Support Assistant</span>
          <span className="chat-subtitle">Agentic · Gemini 1.5 Pro · FAISS RAG · 4 Autonomous Tools</span>
        </div>
        <div className="chat-header-badges">
          <span className="badge badge-rag">Agentic AI</span>
          <span className="badge badge-model">Gemini 1.5 Pro</span>
        </div>
      </div>

      <div className="messages-area">
        {messages.length === 0 && !isLoading ? (
          <WelcomeScreen onSuggestionClick={(p) => sendMessage(p)} />
        ) : (
          <>
            {messages.map((msg) => <MessageBubble key={msg.id} message={msg} />)}
            {isLoading && <TypingIndicator />}
          </>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <div className="input-form">
          <textarea
            ref={textareaRef}
            className="chat-input"
            placeholder="Describe your issue… (e.g., 'My ThinkPad T14s screen is flickering')"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            disabled={isLoading}
          />
          <button
            className="send-button"
            onClick={() => sendMessage()}
            disabled={!inputValue.trim() || isLoading}
            aria-label="Send message"
          >
            <SendHorizonal size={16} />
          </button>
        </div>
        <div className="input-footer">
          <p className="input-footer-text">
            Press <span>Enter</span> to send · <span>Shift+Enter</span> for new line · Always include your <span>laptop model</span>
          </p>
        </div>
      </div>
    </div>
  )
}
