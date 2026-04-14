# AI-Powered Market Reaction Simulator

A production-style, full-stack financial intelligence platform that converts market news into structured event signals, simulates how multiple market participants may react, and produces a dashboard with sentiment, price direction, volatility, reversal probability, and timeline views.

## Why this project matters

Most retail news tools stop at summarization. This platform goes further by combining:

- **Financial NLP** for event parsing and sentiment extraction
- **Agent-based simulation** across five market participant types
- **Interaction rounds** to model narrative conflict over time
- **Market outcome synthesis** into price, volatility, and reversal expectations
- **Scenario testing** so users can tweak assumptions and rerun simulations

## Stack

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- Recharts
- Lucide icons

### Backend
- FastAPI
- SQLAlchemy + SQLite
- Pydantic
- yfinance
- transformers + PyTorch

### NLP / AI
- Default model: `ProsusAI/finbert` via Hugging Face
- Fallback: deterministic finance-aware heuristic parser when model download is unavailable

## Key Features

- Manual event input: headline + optional article body
- Event structuring into positives, negatives, uncertainty, event type, sector
- Five agents:
  - Retail Investor
  - Hedge Fund
  - Institutional Investor
  - Analyst
  - Market Maker
- Multi-round interaction engine:
  - Immediate
  - Short-term
  - Medium-term
- Market outcome engine:
  - Expected price direction
  - Volatility level
  - Reversal probability
  - Confidence range
- Scenario testing sliders
- SQLite persistence for all simulation runs
- Sample events for quick testing

## Architecture

```text
User Input → NLP Structuring → Agent Simulation → Interaction Engine → Outcome Engine → Storage → Dashboard
```

### Backend flow
1. Accept event payload from frontend
2. Fetch optional market context with `yfinance`
3. Parse event into structured financial signals
4. Run 5-agent simulation across 3 rounds
5. Aggregate conflict, conviction, and uncertainty
6. Produce final market outlook
7. Persist run to SQLite
8. Return full simulation response to frontend

### Frontend flow
1. User enters headline/article/ticker
2. User optionally adjusts scenario controls
3. Frontend calls FastAPI
4. Dashboard renders:
   - sentiment overview
   - simulation summary
   - agent cards
   - price path chart
   - volatility chart
   - interaction timeline

## Project Structure

```text
market_reaction_simulator/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── public/
│   ├── styles/
│   ├── package.json
│   └── tailwind.config.ts
├── data/
│   └── sample_events.json
├── .gitignore
└── README.md
```

## Local Setup

### 1. Backend

```bash
cd backend
python -m venv .venv
```

#### Windows
```bash
.venv\Scripts\activate
```

#### macOS / Linux
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run backend:

```bash
uvicorn app.main:app --reload --port 8000
```

Backend docs:
- Swagger UI: `http://localhost:8000/docs`
- Health: `http://localhost:8000/api/v1/health`

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

## Environment Variables

### Backend
Create `backend/.env` if needed:

```env
APP_NAME=AI-Powered Market Reaction Simulator
APP_ENV=development
ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend
Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```

## Free Resource Guarantee

This project only uses free tooling:

- Hugging Face open-source models
- local Python inference
- SQLite
- yfinance
- Next.js + FastAPI
- GitHub free tier

No credit card or usage-based billing is required.

## Testing

### Sample event 1
- Ticker: `AAPL`
- Headline: `Apple beats earnings expectations but warns of softer iPhone demand in China`

Expected behavior:
- mixed sentiment
- positive near-term impulse
- moderate volatility
- non-trivial reversal risk due to guidance conflict

### Sample event 2
- Ticker: `TSLA`
- Headline: `Tesla announces surprise price cuts amid slowing EV demand`

Expected behavior:
- negative sentiment tilt
- higher volatility
- hedge fund / analyst disagreement likely

### Sample event 3
- Ticker: `NVDA`
- Headline: `NVIDIA secures large sovereign AI infrastructure contract and raises revenue outlook`

Expected behavior:
- bullish bias
- strong institutional support
- lower reversal risk unless uncertainty is manually increased

## GitHub Push Guide

### 1. Initialize repository

```bash
git init
git add .
git commit -m "Initial commit: AI-Powered Market Reaction Simulator"
```

### 2. Create GitHub repo
Go to GitHub and create a new free repository, for example:

```text
ai-powered-market-reaction-simulator
```

### 3. Connect remote

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-powered-market-reaction-simulator.git
git push -u origin main
```

## Production Extensions

Ideas for future upgrades while staying mostly free/open-source:

- Add more specialized agents (options desk, short seller, macro fund)
- Introduce Monte Carlo scenario branching
- Use vector search for historical analog events
- Add WebSocket streaming updates
- Support news ingestion from RSS feeds
- Add backtesting against actual post-news returns

## License

Use MIT if you want to open-source it publicly.
