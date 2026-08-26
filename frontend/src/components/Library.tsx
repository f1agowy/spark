import React, { useState, useEffect } from 'react'
import { libraryAPI } from '../api'
import { formatDate } from '../utils'

interface SavedArticle {
  id: string
  title: string
  url: string
  source: string
  description: string
  category: string
  user_note: string
  ai_generated_note: string
  tags: string
  saved_at: string
}

interface LibraryProps {
  onAskChat: (article: SavedArticle, context: string) => void
}

export const Library: React.FC<LibraryProps> = ({ onAskChat }) => {
  const [articles, setArticles] = useState<SavedArticle[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedMonth, setSelectedMonth] = useState<number | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [editingId, setEditingId] = useState<string | null>(null)
  const [editNote, setEditNote] = useState('')
  const [editTags, setEditTags] = useState('')
  const [enhancingId, setEnhancingId] = useState<string | null>(null)

  useEffect(() => {
    loadArticles()
  }, [selectedMonth])

  const loadArticles = async () => {
    try {
      setLoading(true)
      const response = await libraryAPI.getAll(selectedMonth)
      setArticles(response.articles)
    } catch (error) {
      console.error('Error loading articles:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: string) => {
    if (window.confirm('Usunąć artykuł?')) {
      try {
        await libraryAPI.delete(id)
        setArticles(articles.filter(a => a.id !== id))
      } catch (error) {
        console.error('Error deleting:', error)
      }
    }
  }

  const handleSaveEdit = async (id: string) => {
    try {
      await libraryAPI.update(id, {
        user_note: editNote,
        tags: editTags
      })
      setArticles(articles.map(a => 
        a.id === id ? { ...a, user_note: editNote, tags: editTags } : a
      ))
      setEditingId(null)
    } catch (error) {
      console.error('Error updating:', error)
    }
  }

  const handleEnhanceNote = async (id: string, article: SavedArticle) => {
    try {
      setEnhancingId(id)
      const response = await libraryAPI.enhanceNote(id, {
        current_note: article.user_note,
        article_title: article.title,
        prompt: 'Rozwiń tę notatkę z bardziej szczegółową analizą wpływu na branżę'
      })
      setArticles(articles.map(a => 
        a.id === id ? { ...a, ai_generated_note: response.enhanced_note } : a
      ))
    } catch (error) {
      console.error('Error enhancing:', error)
    } finally {
      setEnhancingId(null)
    }
  }

  const filteredArticles = articles.filter(a => 
    a.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    a.user_note.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const months = [
    'Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec',
    'Lipiec', 'Sierpień', 'Wrzesień', 'Pazdziernik', 'Listopad', 'Grudzień'
  ]

  return (
    <div className="card">
      <div className="section-title">📚 Biblioteka Roczna</div>

      {/* Filters */}
      <div style={{ marginBottom: '20px', display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
        <button
          onClick={() => setSelectedMonth(null)}
          style={{
            padding: '8px 12px',
            background: selectedMonth === null ? '#1e90ff' : '#333',
            border: '1px solid #444',
            borderRadius: '6px',
            color: 'white',
            cursor: 'pointer',
            fontSize: '12px'
          }}
        >
          Wszystkie
        </button>
        {months.map((month, idx) => (
          <button
            key={idx}
            onClick={() => setSelectedMonth(idx + 1)}
            style={{
              padding: '8px 12px',
              background: selectedMonth === idx + 1 ? '#1e90ff' : '#333',
              border: '1px solid #444',
              borderRadius: '6px',
              color: 'white',
              cursor: 'pointer',
              fontSize: '12px'
            }}
          >
            {month}
          </button>
        ))}
      </div>

      {/* Search */}
      <input
        type="text"
        placeholder="🔍 Wyszukaj artykuł..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        style={{
          width: '100%',
          marginBottom: '20px',
          padding: '10px',
          background: '#2a2a2a',
          border: '1px solid #444',
          borderRadius: '6px',
          color: 'white'
        }}
      />

      {/* Articles */}
      {loading ? (
        <div className="loading">
          <span className="spinner"></span> Ładowanie...
        </div>
      ) : filteredArticles.length === 0 ? (
        <div className="empty-state">
          <p>Brak zapisanych artykułów</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          {filteredArticles.map((article) => (
            <div key={article.id} style={{
              background: '#2a2a2a',
              padding: '15px',
              borderRadius: '8px',
              border: '1px solid #444'
            }}>
              <a href={article.url} target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none' }}>
                <div style={{ color: '#00d4ff', fontWeight: 'bold', marginBottom: '8px', cursor: 'pointer' }}>
                  {article.title}
                </div>
              </a>
              <div style={{ fontSize: '12px', color: '#888', marginBottom: '10px' }}>
                📰 {article.source} • {formatDate(article.saved_at)}
              </div>

              {/* User Note */}
              {editingId === article.id ? (
                <div style={{ marginBottom: '10px' }}>
                  <textarea
                    value={editNote}
                    onChange={(e) => setEditNote(e.target.value)}
                    style={{
                      width: '100%',
                      minHeight: '80px',
                      padding: '8px',
                      background: '#333',
                      border: '1px solid #1e90ff',
                      borderRadius: '4px',
                      color: 'white',
                      marginBottom: '10px',
                      fontFamily: 'inherit'
                    }}
                  />
                  <input
                    type="text"
                    value={editTags}
                    onChange={(e) => setEditTags(e.target.value)}
                    placeholder="Tagi: #EURO7,#REGULACJE"
                    style={{
                      width: '100%',
                      padding: '8px',
                      background: '#333',
                      border: '1px solid #1e90ff',
                      borderRadius: '4px',
                      color: 'white',
                      marginBottom: '10px'
                    }}
                  />
                  <div style={{ display: 'flex', gap: '10px' }}>
                    <button onClick={() => handleSaveEdit(article.id)} style={{ padding: '6px 12px', fontSize: '12px' }}>
                      ✅ Zapisz
                    </button>
                    <button onClick={() => setEditingId(null)} style={{ padding: '6px 12px', fontSize: '12px', background: '#666' }}>
                      ❌ Anuluj
                    </button>
                  </div>
                </div>
              ) : (
                <div>
                  {article.user_note && (
                    <div style={{
                      background: '#1a1a1a',
                      padding: '10px',
                      borderRadius: '4px',
                      marginBottom: '10px',
                      borderLeft: '3px solid #1e90ff'
                    }}>
                      <div style={{ fontSize: '12px', color: '#888', marginBottom: '5px' }}>📝 Moja notatka:</div>
                      <div style={{ color: '#ccc' }}>{article.user_note}</div>
                    </div>
                  )}

                  {article.ai_generated_note && (
                    <div style={{
                      background: '#1a1a1a',
                      padding: '10px',
                      borderRadius: '4px',
                      marginBottom: '10px',
                      borderLeft: '3px solid #00d4ff'
                    }}>
                      <div style={{ fontSize: '12px', color: '#888', marginBottom: '5px' }}>🤖 Notatka AI:</div>
                      <div style={{ color: '#ccc' }}>{article.ai_generated_note}</div>
                    </div>
                  )}

                  {article.tags && (
                    <div style={{ marginBottom: '10px', display: 'flex', flexWrap: 'wrap', gap: '5px' }}>
                      {article.tags.split(',').map((tag, idx) => (
                        <span key={idx} style={{
                          background: '#1e90ff',
                          color: 'white',
                          padding: '4px 8px',
                          borderRadius: '12px',
                          fontSize: '11px'
                        }}>
                          {tag.trim()}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* Actions */}
              {editingId !== article.id && (
                <div style={{ display: 'flex', gap: '8px', marginTop: '10px', flexWrap: 'wrap' }}>
                  <button
                    onClick={() => {
                      setEditingId(article.id)
                      setEditNote(article.user_note)
                      setEditTags(article.tags)
                    }}
                    style={{ padding: '6px 12px', fontSize: '12px', background: '#00d4ff' }}
                  >
                    ✏️ Edytuj
                  </button>
                  <button
                    onClick={() => handleEnhanceNote(article.id, article)}
                    disabled={enhancingId === article.id}
                    style={{
                      padding: '6px 12px',
                      fontSize: '12px',
                      background: enhancingId === article.id ? '#666' : '#1e90ff',
                      cursor: enhancingId === article.id ? 'not-allowed' : 'pointer'
                    }}
                  >
                    {enhancingId === article.id ? '⏳ AI pisze...' : '✨ Rozwiń AI'}
                  </button>
                  <button
                    onClick={() => onAskChat(article, article.user_note)}
                    style={{ padding: '6px 12px', fontSize: '12px', background: '#666' }}
                  >
                    💬 Pytaj
                  </button>
                  <button
                    onClick={() => handleDelete(article.id)}
                    style={{ padding: '6px 12px', fontSize: '12px', background: '#8b0000' }}
                  >
                    🗑️ Usuń
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
