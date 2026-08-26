import React from 'react'

interface HeaderProps {
  loading: boolean
  onFetchNews: () => void
}

export const Header: React.FC<HeaderProps> = ({ loading, onFetchNews }) => {
  return (
    <div className="header">
      <h1>🚀 SPARK</h1>
      <p>MHCV Industry News Agent - AI-powered insights for the commercial vehicle industry</p>
      <div className="controls" style={{ marginTop: '20px' }}>
        <button
          onClick={onFetchNews}
          disabled={loading}
          style={{
            opacity: loading ? 0.6 : 1,
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? (
            <>
              <span className="spinner"></span> Ładowanie...
            </>
          ) : (
            '📰 Pobierz newsy'
          )}
        </button>
      </div>
    </div>
  )
}
