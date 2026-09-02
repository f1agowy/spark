import axios from 'axios'
import { NewsResponse, ChatResponse } from './types'

const API_URL = 'https://mobglo.onrender.com'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const newsAPI = {
  fetch: async (forceRefresh: boolean = false): Promise<NewsResponse> => {
    const response = await api.post('/news/fetch', {
      force_refresh: forceRefresh
    })
    return response.data
  }
}

export const chatAPI = {
  sendMessage: async (message: string, sessionId: string, articleContext?: string): Promise<ChatResponse> => {
    const response = await api.post('/chat', {
      message,
      session_id: sessionId,
      article_context: articleContext
    })
    return response.data
  }
}

export const libraryAPI = {
  save: async (data: any) => {
    const response = await api.post('/library/save', data)
    return response.data
  },
  getAll: async (month?: number) => {
    const params = month ? `?month=${month}` : ''
    const response = await api.get(`/library/all${params}`)
    return response.data
  },
  update: async (articleId: string, data: any) => {
    const response = await api.put(`/library/${articleId}`, data)
    return response.data
  },
  delete: async (articleId: string) => {
    const response = await api.delete(`/library/${articleId}`)
    return response.data
  },
  enhanceNote: async (articleId: string, data: any) => {
    const response = await api.post(`/library/${articleId}/enhance-note`, data)
    return response.data
  },
  getStats: async () => {
    const response = await api.get('/stats')
    return response.data
  },
  exportExcel: async () => {
    const response = await api.get('/library/export/excel')
    return response.data
  }
}

export default api
