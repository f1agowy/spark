import React, { useState, useEffect } from 'react'
import { Header } from './components/Header'
import { NewsSection } from './components/NewsSection'
import { Chat } from './components/Chat'
import { Library } from './components/Library'
import { Stats } from './components/Stats'
import { ArticleCard } from './components/ArticleCard'
import { NewsResponse, NewsArticle } from './types'
import { newsAPI, chatAPI, libraryAPI } from './api'
import { getStoredSessionId } from './utils'
import './App.css'

function App() {
  const [news, setNews] = useState<NewsResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [sessionId] = useState(() => getStoredSessionId())
  const [activeTab, setActiveTab] = useState<'news' | 'chat' | 'library' | 'stats'>('news')
  const [chatArticleContext, setChatArticleContext] = useState<string>('')
  const [savingArticle, setSavingArticle] = useState<string | null>(null)

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

  const handleSaveArticle = async (article: NewsArticle) => {
    try {
      setSavingArticle(article.url)
      await libraryAPI.save({
        title: article.title,
        url: article.url,
        source: article.source,
        description: article.description,
        category: article.category,
        user_note: '',
        tags: ''
      })
      alert('✅ Artykuł zapisany do biblioteki!')
    } catch (err) {
      console.error('Error saving:', err)
      alert('❌ Błąd podczas zapisywania')
    } finally {
      setSavingArticle(null)
    }
  }

  const handleAskChat = (article: NewsArticle) => {
    setChatArticleContext(`Artykuł: ${article.title}\nŹródło: ${article.source}\nTreść: ${article.description}`)
    setActiveTab('chat')
  }

  const handleAskChatFromLibrary = (article: any, context: string) => {
    setChatArticleContext(`Artykuł: ${article.title}\nMoja notatka: ${context}`)
    setActiveTab('chat')
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
            onClick={() => {
              setChatArticleContext('')
              setActiveTab('chat')
            }}
          >
            💬 Chat
          </button>
          <button
            className={`tab ${activeTab === 'library' ? 'active' : ''}`}
            onClick={() => setActiveTab('library')}
          >
            📚 Biblioteka
          </button>
          <button
            className={`tab ${activeTab === 'stats' ? 'active' : ''}`}
            onClick={() => setActiveTab('stats')}
          >
            📊 Statystyki
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
                onSave={handleSaveArticle}
                onAskChat={handleAskChat}
                savingArticleUrl={savingArticle}
              />
              <NewsSection
                title="Europa - Pozostała branża"
                icon="🌍"
                articles={news.data.europe_other}
                onSave={handleSaveArticle}
                onAskChat={handleAskChat}
                savingArticleUrl={savingArticle}
              />
              <NewsSection
                title="Świat - Globalne newsy"
                icon="🌐"
                articles={news.data.global}
                onSave={handleSaveArticle}
                onAskChat={handleAskChat}
                savingArticleUrl={savingArticle}
              />
            </>
          )}
        </>
      ) : activeTab === 'chat' ? (
        <Chat sessionId={sessionId} articleContext={chatArticleContext} />
      ) : activeTab === 'library' ? (
        <Library onAskChat={handleAskChatFromLibrary} />
      ) : (
        <Stats />
      )}
    </div>
  )
}

export default App
