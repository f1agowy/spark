# 🚗 SPARK - MHCV Industry News Agent

AI-powered news aggregator for Medium/Heavy Commercial Vehicles industry. Analyzes multiple sources across Europe and the globe, with interactive AI chat.

## 📰 News Structure
1. **Europe - MHCV** (from 6 key sources)
2. **Europe - Other Industries** (internet sources)
3. **Global News** (LV & worldwide automotive)
4. **💬 Interactive Chat** (ask AI about articles)

## 🌐 Data Sources
- euractiv.com
- theicct.org
- electrive.com
- acea.auto
- transportenvironment.org
- alternative-fuels-observatory.ec.europa.eu
- NewsAPI (worldwide coverage)

## 🛠️ Tech Stack
- **Backend:** Python (FastAPI)
- **Frontend:** React + TypeScript
- **AI:** Google Gemini API (free tier)
- **Web Scraping:** BeautifulSoup, Requests
- **Database:** SQLite (local storage)

## ⚡ Features
- Daily news aggregation on-demand
- Intelligent news categorization
- Web scraping from 6 European sources
- Global news integration
- AI-powered chat about news articles
- Fresh chat session each day
- History of previous conversations

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- Google Gemini API Key
- NewsAPI Key

### Setup

```bash
# Clone repo
git clone https://github.com/f1agowy/spark.git
cd spark

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt

# Create .env file
echo "GEMINI_API_KEY=your_key_here" > .env
echo "NEWSAPI_KEY=your_key_here" >> .env

# Run backend
python main.py

# Frontend setup (new terminal)
cd frontend
npm install
npm run dev
```

Visit: `http://localhost:3000`

## 📁 Project Structure
```
spark/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── base_scraper.py
│   │   └── sources.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── news_service.py
│   │   ├── ai_service.py
│   │   └── categorizer.py
│   └── database/
│       ├── __init__.py
│       ├── models.py
│       └── db.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## 📝 License
MIT
