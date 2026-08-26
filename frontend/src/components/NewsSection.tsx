import React from 'react'
import { NewsArticle } from '../types'
import { ArticleCard } from './ArticleCard'

interface NewsSectionProps {
  title: string
  icon: string
  articles: NewsArticle[]
  onSave: (article: NewsArticle) => void
  onAskChat: (article: NewsArticle) => void
  savingArticleUrl?: string | null
}

export const NewsSection: React.FC<NewsSectionProps> = ({
  title,
  icon,
  articles,
  onSave,
  onAskChat,
  savingArticleUrl
}) => {
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
          <ArticleCard
            key={index}
            article={article}
            onSave={onSave}
            onAskChat={onAskChat}
            isSaved={savingArticleUrl === article.url}
          />
        ))}
      </div>
    </div>
  )
}
