import React, { useState, useEffect } from 'react'
import { Header } from './components/Header'
import { NewsSection } from './components/NewsSection'
import { Chat } from './components/Chat'
import { NewsResponse } from './types'
import { newsAPI } from './api'
import { getStoredSessionId } from './utils'
import './App.css'

function App() {
  const [news, setNews] = useState<NewsResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [sessionId] = useState(() => getStoredSessionId())
  const [activeTab, setActiveTab] = useState<'news' | 'chat'>('news')

  const handleFetchNews = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await newsAPI.fetch(true)
      setNews(data)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Błąd podczas pobierania newsów'
      setError(errorMessage)
      console.error('Error fetching news:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    // Auto-fetch news on mount
    handleFetchNews()
  }, [])

  return (
    <div className="container">
      <Header loading={loading} onFetchNews={handleFetchNews} />

      {error && (
        <div className="error">
          ❌ {error}
        </div>
      )}

      {news && (
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'news' ? 'active' : ''}`}
            onClick={() => setActiveTab('news')}
          >
            📰 Newsy ({news.categories.europe_mhcv + news.categories.europe_other + news.categories.global})
          </button>
          <button
            className={`tab ${activeTab === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveTab('chat')}
          >
            💬 Chat
          </button>
        </div>
      )}

      {activeTab === 'news' ? (
        <>
          {!news ? (
            <div className="empty-state">
              <div className="spinner"></div>
              <p>Ładowanie newsów...</p>
            </div>
          ) : (
            <>
              <NewsSection
                title="Europa - MHCV"
                icon="🇪🇺"
                articles={news.data.europe_mhcv}
              />
              <NewsSection
                title="Europa - Pozostała branża"
                icon="🌍"
                articles={news.data.europe_other}
              />
              <NewsSection
                title="Świat - Globalne newsy"
                icon="🌐"
                articles={news.data.global}
              />
            </>
          )}
        </>
      ) : (
        <Chat sessionId={sessionId} />
      )}
    </div>
  )
}

export default App
