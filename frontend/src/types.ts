export interface NewsArticle {
  title: string
  url: string
  description: string
  source: string
  published_at: string
  category?: string
  image_url?: string
}

export interface NewsResponse {
  success: boolean
  timestamp: string
  data: {
    europe_mhcv: NewsArticle[]
    europe_other: NewsArticle[]
    global: NewsArticle[]
    all_news: NewsArticle[]
    total_articles: number
  }
  categories: {
    europe_mhcv: number
    europe_other: number
    global: number
  }
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface ChatResponse {
  success: boolean
  response: string
  session_id: string
  timestamp: string
}
