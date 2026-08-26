import axios from 'axios'
import { NewsResponse, ChatResponse } from './types'

const API_URL = 'http://localhost:8000/api'

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
  sendMessage: async (message: string, sessionId: string): Promise<ChatResponse> => {
    const response = await api.post('/chat', {
      message,
      session_id: sessionId
    })
    return response.data
  }
}

export default api
