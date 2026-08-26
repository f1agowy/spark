import React, { useState, useEffect } from 'react'
import { NewsArticle } from '../types'
import { formatDate, truncateText } from '../utils'
import { libraryAPI } from '../api'

interface ArticleCardProps {
  article: NewsArticle
  onSave: (article: NewsArticle) => void
  onAskChat: (article: NewsArticle) => void
  isSaved?: boolean
}

export const ArticleCard: React.FC<ArticleCardProps> = ({
  article,
  onSave,
  onAskChat,
  isSaved = false
}) => {
  return (
    <a
      href={article.url}
      target="_blank"
      rel="noopener noreferrer"
      style={{ textDecoration: 'none' }}
    >
      <div className="article">
        <div className="article-title">{article.title}</div>
        <div className="article-source">
          📰 {article.source} • {formatDate(article.published_at)}
        </div>
        <div className="article-description">
          {truncateText(article.description, 180)}
        </div>
        <div className="article-actions" style={{
          marginTop: '10px',
          display: 'flex',
          gap: '10px',
          justifyContent: 'flex-end'
        }}>
          <button
            onClick={(e) => {
              e.preventDefault()
              e.stopPropagation()
              onAskChat(article)
            }}
            style={{
              padding: '6px 12px',
              fontSize: '12px',
              background: '#00d4ff',
              marginRight: '5px'
            }}
          >
            💬 Pytaj
          </button>
          <button
            onClick={(e) => {
              e.preventDefault()
              e.stopPropagation()
              onSave(article)
            }}
            disabled={isSaved}
            style={{
              padding: '6px 12px',
              fontSize: '12px',
              background: isSaved ? '#444' : '#1e90ff',
              cursor: isSaved ? 'not-allowed' : 'pointer',
              opacity: isSaved ? 0.5 : 1
            }}
          >
            {isSaved ? '✓ Zapisano' : '💾 Zapisz'}
          </button>
        </div>
      </div>
    </a>
  )
}
