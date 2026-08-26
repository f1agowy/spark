import React, { useState, useRef, useEffect } from 'react'
import { ChatMessage } from '../types'
import { chatAPI } from '../api'

interface ChatProps {
  sessionId: string
}

export const Chat: React.FC<ChatProps> = ({ sessionId }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async () => {
    if (!input.trim() || loading) return

    const userMessage = input
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])
    setLoading(true)

    try {
      const response = await chatAPI.sendMessage(userMessage, sessionId)
      setMessages(prev => [...prev, { role: 'assistant', content: response.response }])
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Błąd podczas wysyłania wiadomości'
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: `❌ Błąd: ${errorMessage}` }
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="card">
      <div className="section-title">💬 Chat z agentem AI</div>
      <div className="chat-container">
        <div className="messages">
          {messages.length === 0 ? (
            <div className="empty-state">
              <p>👋 Cześć! Jestem SPARK, Twój asystent ds. branży MHCV.</p>
              <p>Możesz zadać mi pytania o pobrane artykuły lub branżę.</p>
            </div>
          ) : (
            messages.map((msg, index) => (
              <div key={index} className={`message ${msg.role}`}>
                <div className="message-content">{msg.content}</div>
              </div>
            ))
          )}
          {loading && (
            <div className="message assistant">
              <div className="message-content">
                <span className="spinner"></span> Myślę...
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        <div className="chat-input-area">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Zadaj pytanie..."
            disabled={loading}
          />
          <button
            onClick={handleSendMessage}
            disabled={loading || !input.trim()}
          >
            Wyślij
          </button>
        </div>
      </div>
    </div>
  )
}
