import React from 'react'
import { NewsArticle } from '../types'
import { formatDate, truncateText } from '../utils'

interface NewsSectionProps {
  title: string
  icon: string
  articles: NewsArticle[]
}

export const NewsSection: React.FC<NewsSectionProps> = ({ title, icon, articles }) => {
  if (articles.length === 0) {
    return null
  }

  return (
    <div className="card">
      <div className="section-title">
        {icon} {title} ({articles.length})
      </div>
      <div>
        {articles.map((article, index) => (
          <a
            key={index}
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            style={{ textDecoration: 'none' }}
          >
            <div className="article">
              <div className="article-title">{article.title}</div>
              <div className="article-source">📍 {article.source}</div>
              <div className="article-description">
                {truncateText(article.description, 180)}
              </div>
            </div>
          </a>
        ))}
      </div>
    </div>
  )
}
