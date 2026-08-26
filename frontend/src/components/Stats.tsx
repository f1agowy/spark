import React, { useState, useEffect } from 'react'
import { libraryAPI } from '../api'

interface StatsData {
  total_articles: number
  articles_by_month: Record<string, number>
  top_tags: Record<string, number>
  sources: Record<string, number>
  categories: Record<string, number>
  recent_articles: Array<{
    title: string
    saved_at: string
    category: string
  }>
}

export const Stats: React.FC = () => {
  const [stats, setStats] = useState<StatsData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      setLoading(true)
      const response = await libraryAPI.getStats()
      setStats(response.stats)
    } catch (error) {
      console.error('Error loading stats:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="card">
        <div className="loading">
          <span className="spinner"></span> Ładowanie statystyk...
        </div>
      </div>
    )
  }

  if (!stats) {
    return (
      <div className="card">
        <div className="empty-state">
          <p>Brak danych statystyk</p>
        </div>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="section-title">📊 Statystyki Roczne 2026</div>

      {/* Total */}
      <div style={{
        background: '#2a2a2a',
        padding: '20px',
        borderRadius: '8px',
        marginBottom: '20px',
        textAlign: 'center',
        border: '2px solid #1e90ff'
      }}>
        <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#1e90ff' }}>
          {stats.total_articles}
        </div>
        <div style={{ color: '#888', marginTop: '5px' }}>Łącznie artykułów w bibliotece</div>
      </div>

      {/* Monthly breakdown */}
      <div style={{ marginBottom: '30px' }}>
        <h3 style={{ color: '#00d4ff', marginBottom: '15px' }}>📅 Po miesiącach:</h3>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
          gap: '10px'
        }}>
          {Object.entries(stats.articles_by_month).map(([month, count]) => (
            <div key={month} style={{
              background: '#2a2a2a',
              padding: '15px',
              borderRadius: '6px',
              textAlign: 'center',
              border: '1px solid #444'
            }}>
              <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#1e90ff' }}>
                {count}
              </div>
              <div style={{ fontSize: '12px', color: '#888', marginTop: '5px' }}>
                {month}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Top tags */}
      <div style={{ marginBottom: '30px' }}>
        <h3 style={{ color: '#00d4ff', marginBottom: '15px' }}>🏷️ Popularne tagi:</h3>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
          {Object.entries(stats.top_tags).map(([tag, count]) => (
            <div key={tag} style={{
              background: '#2a2a2a',
              padding: '8px 12px',
              borderRadius: '20px',
              border: '1px solid #1e90ff',
              fontSize: '12px'
            }}>
              {tag} <span style={{ color: '#888', marginLeft: '5px' }}>({count})</span>
            </div>
          ))}
        </div>
      </div>

      {/* Sources */}
      <div style={{ marginBottom: '30px' }}>
        <h3 style={{ color: '#00d4ff', marginBottom: '15px' }}>📰 Źródła:</h3>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
          gap: '10px'
        }}>
          {Object.entries(stats.sources).map(([source, count]) => (
            <div key={source} style={{
              background: '#2a2a2a',
              padding: '12px',
              borderRadius: '6px',
              border: '1px solid #444'
            }}>
              <div style={{ fontSize: '14px', fontWeight: 'bold' }}>{source}</div>
              <div style={{ fontSize: '12px', color: '#1e90ff', marginTop: '5px' }}>{count} artykułów</div>
            </div>
          ))}
        </div>
      </div>

      {/* Categories */}
      <div>
        <h3 style={{ color: '#00d4ff', marginBottom: '15px' }}>🌍 Kategorie:</h3>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
          gap: '10px'
        }}>
          {Object.entries(stats.categories).map(([category, count]) => (
            <div key={category} style={{
              background: '#2a2a2a',
              padding: '12px',
              borderRadius: '6px',
              border: '1px solid #444'
            }}>
              <div style={{ fontSize: '14px', fontWeight: 'bold' }}>
                {category === 'europe_mhcv' && '🇪🇺 Europa-MHCV'}
                {category === 'europe_other' && '🌍 Europa-Other'}
                {category === 'global' && '🌐 Świat'}
              </div>
              <div style={{ fontSize: '12px', color: '#1e90ff', marginTop: '5px' }}>{count} artykułów</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
