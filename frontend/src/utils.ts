import { v4 as uuidv4 } from 'uuid'

export function generateSessionId(): string {
  return uuidv4()
}

export function getTodaySessionKey(): string {
  const today = new Date().toISOString().split('T')[0]
  return `spark_session_${today}`
}

export function getStoredSessionId(): string {
  const key = getTodaySessionKey()
  let sessionId = localStorage.getItem(key)
  
  if (!sessionId) {
    sessionId = generateSessionId()
    localStorage.setItem(key, sessionId)
  }
  
  return sessionId
}

export function formatDate(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleDateString('pl-PL', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

export function truncateText(text: string, length: number = 150): string {
  if (text.length <= length) return text
  return text.substring(0, length) + '...'
}
