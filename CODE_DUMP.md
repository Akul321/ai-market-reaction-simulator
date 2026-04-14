# Source Code Dump

## `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.sqlite3
*.db
.venv/
venv/
.env
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Node
node_modules/
.next/
out/
.env.local
npm-debug.log*

# OS / Editor
.DS_Store
Thumbs.db
.vscode/
.idea/

# Build artifacts
dist/
build/
coverage/

# Model caches
.cache/
.huggingface/
```

## `README.md`

```markdown
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
```

## `backend/app/__init__.py`

```py

```

## `backend/app/api/routes.py`

```py
import json
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.simulation import SimulationRun
from app.schemas.simulation import EventInput, HealthResponse, SampleEvent, SimulationResponse
from app.services.market_data import MarketDataService
from app.services.simulation_engine import SimulationEngine

router = APIRouter()
simulation_engine = SimulationEngine()
market_data_service = MarketDataService()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", app_name=settings.app_name)


@router.get("/sample-events", response_model=List[SampleEvent])
def sample_events() -> List[SampleEvent]:
    data_path = Path(__file__).resolve().parents[3] / "data" / "sample_events.json"
    with open(data_path, "r", encoding="utf-8") as file:
        payload = json.load(file)
    return [SampleEvent(**item) for item in payload]


@router.post("/simulate", response_model=SimulationResponse)
def simulate_event(payload: EventInput, db: Session = Depends(get_db)) -> SimulationResponse:
    market_context = market_data_service.get_market_context(payload.ticker)
    result = simulation_engine.run(payload=payload, market_context=market_context)

    db_record = SimulationRun(
        ticker=payload.ticker,
        headline=payload.headline,
        article=payload.article,
        event_type=result.structured_event.event_type,
        sector=result.structured_event.sector,
        sentiment_score=result.structured_event.sentiment_score,
        price_direction=result.outcome.expected_price_direction,
        volatility_level=result.outcome.volatility_level,
        reversal_probability=result.outcome.reversal_probability,
        confidence_low=result.outcome.confidence_range["low"],
        confidence_high=result.outcome.confidence_range["high"],
        raw_response=result.model_dump_json(indent=2),
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    return result.model_copy(update={"run_id": db_record.id})


@router.get("/runs/{run_id}")
def get_run(run_id: int, db: Session = Depends(get_db)):
    record = db.query(SimulationRun).filter(SimulationRun.id == run_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Simulation run not found")
    return json.loads(record.raw_response)
```

## `backend/app/core/config.py`

```py
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI-Powered Market Reaction Simulator"
    app_env: str = "development"
    database_url: str = "sqlite:///./market_simulator.db"
    allowed_origins: List[str] = ["http://localhost:3000"]
    huggingface_model_name: str = "ProsusAI/finbert"
    yfinance_period: str = "1mo"
    yfinance_interval: str = "1d"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
```

## `backend/app/db/base.py`

```py
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
```

## `backend/app/db/session.py`

```py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base import Base

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    from app.models.simulation import SimulationRun

    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## `backend/app/main.py`

```py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.core.config import settings
from app.db.session import init_db


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description="AI-Powered Market Reaction Simulator API",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def on_startup() -> None:
        init_db()

    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_application()
```

## `backend/app/models/__init__.py`

```py

```

## `backend/app/models/simulation.py`

```py
from sqlalchemy import DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SimulationRun(Base):
    __tablename__ = "simulation_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ticker: Mapped[str] = mapped_column(String(16), nullable=True, index=True)
    headline: Mapped[str] = mapped_column(String(500), nullable=False)
    article: Mapped[str] = mapped_column(Text, nullable=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=True)
    sector: Mapped[str] = mapped_column(String(100), nullable=True)
    sentiment_score: Mapped[float] = mapped_column(Float, default=0.0)
    price_direction: Mapped[str] = mapped_column(String(32), nullable=False)
    volatility_level: Mapped[str] = mapped_column(String(32), nullable=False)
    reversal_probability: Mapped[float] = mapped_column(Float, default=0.0)
    confidence_low: Mapped[float] = mapped_column(Float, default=0.0)
    confidence_high: Mapped[float] = mapped_column(Float, default=0.0)
    raw_response: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
```

## `backend/app/schemas/__init__.py`

```py

```

## `backend/app/schemas/simulation.py`

```py
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class ScenarioControls(BaseModel):
    shock_intensity: float = Field(default=0.6, ge=0.0, le=1.0)
    uncertainty_bias: float = Field(default=0.4, ge=0.0, le=1.0)
    liquidity_stress: float = Field(default=0.3, ge=0.0, le=1.0)
    narrative_persistence: float = Field(default=0.5, ge=0.0, le=1.0)


class EventInput(BaseModel):
    ticker: Optional[str] = None
    headline: str = Field(..., min_length=5, max_length=500)
    article: Optional[str] = Field(default=None, max_length=5000)
    scenario: ScenarioControls = Field(default_factory=ScenarioControls)


class StructuredEvent(BaseModel):
    summary: str
    positives: List[str]
    negatives: List[str]
    uncertainty: List[str]
    event_type: str
    sector: str
    sentiment_breakdown: Dict[str, float]
    sentiment_score: float


class AgentReaction(BaseModel):
    agent_name: str
    interpretation: str
    action: Literal["buy", "sell", "hold"]
    confidence: float
    time_horizon: str
    round: str
    conviction_score: float


class TimelinePoint(BaseModel):
    round: str
    net_pressure: float
    consensus: float
    disagreement: float
    expected_price_move_pct: float
    volatility_index: float


class MarketOutcome(BaseModel):
    expected_price_direction: str
    expected_price_move_pct: float
    volatility_level: str
    volatility_index: float
    reversal_probability: float
    confidence_range: Dict[str, float]
    dominant_narrative: str


class MarketContext(BaseModel):
    ticker: Optional[str] = None
    latest_close: Optional[float] = None
    avg_volume: Optional[float] = None
    return_5d_pct: Optional[float] = None
    realized_volatility: Optional[float] = None


class SimulationResponse(BaseModel):
    structured_event: StructuredEvent
    market_context: MarketContext
    agent_reactions: List[AgentReaction]
    timeline: List[TimelinePoint]
    outcome: MarketOutcome
    run_id: int


class HealthResponse(BaseModel):
    status: str
    app_name: str


class SampleEvent(BaseModel):
    ticker: str
    headline: str
    article: Optional[str] = None
```

## `backend/app/services/agent_factory.py`

```py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from app.schemas.simulation import AgentReaction, MarketContext, ScenarioControls, StructuredEvent


@dataclass
class AgentProfile:
    name: str
    sensitivity: float
    contrarian_bias: float
    horizon: str
    style: str


class AgentFactory:
    def __init__(self) -> None:
        self.agents = [
            AgentProfile("Retail Investor", sensitivity=0.95, contrarian_bias=0.10, horizon="immediate", style="narrative-driven and momentum sensitive"),
            AgentProfile("Hedge Fund", sensitivity=1.20, contrarian_bias=0.35, horizon="short-term", style="opportunistic, tactical, and conflict-seeking"),
            AgentProfile("Institutional Investor", sensitivity=0.75, contrarian_bias=0.05, horizon="medium-term", style="quality-focused and risk-calibrated"),
            AgentProfile("Analyst", sensitivity=0.70, contrarian_bias=0.20, horizon="medium-term", style="fundamental and guidance-oriented"),
            AgentProfile("Market Maker", sensitivity=0.55, contrarian_bias=0.40, horizon="immediate", style="liquidity-aware and volatility-pricing"),
        ]

    def generate_reactions(
        self,
        structured_event: StructuredEvent,
        scenario: ScenarioControls,
        market_context: MarketContext,
        rounds: List[str],
    ) -> List[AgentReaction]:
        reactions: List[AgentReaction] = []
        base_signal = structured_event.sentiment_score
        uncertainty_penalty = len(structured_event.uncertainty) * 0.04 + scenario.uncertainty_bias * 0.2
        context_boost = (market_context.return_5d_pct or 0.0) / 100.0

        for round_index, round_name in enumerate(rounds):
            round_decay = [1.0, 0.82, 0.68][round_index]
            for agent in self.agents:
                adjusted_signal = (base_signal + context_boost) * agent.sensitivity * round_decay
                adjusted_signal -= uncertainty_penalty * (1 - agent.contrarian_bias)
                adjusted_signal += scenario.shock_intensity * 0.15 * (1 if base_signal >= 0 else -1)
                adjusted_signal -= scenario.liquidity_stress * 0.10 if agent.name == "Market Maker" else 0.0
                adjusted_signal += scenario.narrative_persistence * 0.08 if agent.horizon == "medium-term" else 0.0

                conviction = max(-1.0, min(1.0, adjusted_signal))
                confidence = min(0.99, max(0.05, 0.55 + abs(conviction) * 0.35 - uncertainty_penalty * 0.2))
                action = self._action_from_signal(conviction)
                interpretation = self._build_interpretation(agent, structured_event, action, conviction)

                reactions.append(
                    AgentReaction(
                        agent_name=agent.name,
                        interpretation=interpretation,
                        action=action,
                        confidence=round(confidence, 3),
                        time_horizon=agent.horizon,
                        round=round_name,
                        conviction_score=round(conviction, 3),
                    )
                )
        return reactions

    def _action_from_signal(self, signal: float) -> str:
        if signal > 0.10:
            return "buy"
        if signal < -0.10:
            return "sell"
        return "hold"

    def _build_interpretation(self, agent: AgentProfile, event: StructuredEvent, action: str, conviction: float) -> str:
        direction = "upside" if conviction >= 0 else "downside"
        return (
            f"The {agent.name.lower()} reads this as a {event.event_type.replace('_', ' ')} signal with {direction} bias. "
            f"Its style is {agent.style}, so it chooses to {action} based on the current balance of positives, negatives, and uncertainty."
        )
```

## `backend/app/services/interaction_engine.py`

```py
from __future__ import annotations

from collections import defaultdict
from typing import List

from app.schemas.simulation import AgentReaction, TimelinePoint


class InteractionEngine:
    def build_timeline(self, reactions: List[AgentReaction]) -> List[TimelinePoint]:
        grouped = defaultdict(list)
        for reaction in reactions:
            grouped[reaction.round].append(reaction)

        timeline: List[TimelinePoint] = []
        for round_name in ["immediate", "short_term", "medium_term"]:
            round_reactions = grouped.get(round_name, [])
            if not round_reactions:
                continue
            convictions = [r.conviction_score for r in round_reactions]
            net_pressure = sum(convictions) / len(convictions)
            buy_share = sum(1 for r in round_reactions if r.action == "buy") / len(round_reactions)
            sell_share = sum(1 for r in round_reactions if r.action == "sell") / len(round_reactions)
            consensus = abs(buy_share - sell_share)
            disagreement = 1 - consensus
            expected_move = net_pressure * 3.2
            volatility_index = min(100.0, 25 + disagreement * 40 + abs(net_pressure) * 20)

            timeline.append(
                TimelinePoint(
                    round=round_name,
                    net_pressure=round(net_pressure, 3),
                    consensus=round(consensus, 3),
                    disagreement=round(disagreement, 3),
                    expected_price_move_pct=round(expected_move, 2),
                    volatility_index=round(volatility_index, 2),
                )
            )
        return timeline
```

## `backend/app/services/market_data.py`

```py
from __future__ import annotations

from typing import Optional

import numpy as np
import yfinance as yf

from app.core.config import settings
from app.schemas.simulation import MarketContext


class MarketDataService:
    def get_market_context(self, ticker: Optional[str]) -> MarketContext:
        if not ticker:
            return MarketContext()
        try:
            data = yf.download(
                ticker,
                period=settings.yfinance_period,
                interval=settings.yfinance_interval,
                progress=False,
                auto_adjust=True,
            )
            if data.empty:
                return MarketContext(ticker=ticker)

            close = data["Close"].dropna()
            volume = data["Volume"].dropna() if "Volume" in data.columns else None
            returns = close.pct_change().dropna()
            realized_vol = float(returns.std() * np.sqrt(252)) if len(returns) > 1 else None
            return_5d = float((close.iloc[-1] / close.iloc[-6] - 1) * 100) if len(close) >= 6 else None

            return MarketContext(
                ticker=ticker.upper(),
                latest_close=round(float(close.iloc[-1]), 2),
                avg_volume=round(float(volume.tail(10).mean()), 2) if volume is not None and len(volume) else None,
                return_5d_pct=round(return_5d, 2) if return_5d is not None else None,
                realized_volatility=round(realized_vol, 4) if realized_vol is not None else None,
            )
        except Exception:
            return MarketContext(ticker=ticker.upper())
```

## `backend/app/services/nlp_service.py`

```py
from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Dict, List, Optional

from app.core.config import settings
from app.schemas.simulation import StructuredEvent
from app.utils.keywords import EVENT_TYPE_KEYWORDS, NEGATIVE_KEYWORDS, POSITIVE_KEYWORDS, SECTOR_KEYWORDS, UNCERTAINTY_KEYWORDS

try:
    from transformers import pipeline
except Exception:  # pragma: no cover
    pipeline = None


@dataclass
class NLPArtifacts:
    sentiment_label: str
    sentiment_confidence: float


class NLPService:
    """Financial NLP parser with a Hugging Face primary path and heuristic fallback."""

    def __init__(self) -> None:
        self._classifier = None
        self._load_failed = False

    def _get_classifier(self):
        if self._classifier is not None:
            return self._classifier
        if self._load_failed or pipeline is None:
            return None
        try:
            self._classifier = pipeline(
                "text-classification",
                model=settings.huggingface_model_name,
                tokenizer=settings.huggingface_model_name,
                truncation=True,
            )
            return self._classifier
        except Exception:
            self._load_failed = True
            return None

    def analyze(self, headline: str, article: Optional[str] = None) -> StructuredEvent:
        text = f"{headline}. {article or ''}".strip()
        cleaned = self._normalize(text)

        positives = self._extract_signals(cleaned, POSITIVE_KEYWORDS)
        negatives = self._extract_signals(cleaned, NEGATIVE_KEYWORDS)
        uncertainty = self._extract_signals(cleaned, UNCERTAINTY_KEYWORDS)
        event_type = self._infer_event_type(cleaned)
        sector = self._infer_sector(cleaned)
        sentiment = self._get_sentiment(cleaned, positives, negatives)
        sentiment_breakdown = self._build_sentiment_breakdown(sentiment, len(positives), len(negatives), len(uncertainty))
        sentiment_score = sentiment_breakdown["positive"] - sentiment_breakdown["negative"]
        summary = self._build_summary(headline, event_type, sector, positives, negatives, uncertainty)

        return StructuredEvent(
            summary=summary,
            positives=positives,
            negatives=negatives,
            uncertainty=uncertainty,
            event_type=event_type,
            sector=sector,
            sentiment_breakdown=sentiment_breakdown,
            sentiment_score=round(sentiment_score, 3),
        )

    def _normalize(self, text: str) -> str:
        return re.sub(r"\s+", " ", text.lower()).strip()

    def _extract_signals(self, text: str, keywords: set[str]) -> List[str]:
        hits = []
        for kw in sorted(keywords):
            if kw in text:
                hits.append(kw)
        return hits[:6]

    def _infer_event_type(self, text: str) -> str:
        best_label, best_score = "general_corporate", 0
        for label, keywords in EVENT_TYPE_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > best_score:
                best_label, best_score = label, score
        return best_label

    def _infer_sector(self, text: str) -> str:
        best_label, best_score = "Broad Market", 0
        for label, keywords in SECTOR_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > best_score:
                best_label, best_score = label, score
        return best_label

    def _get_sentiment(self, text: str, positives: List[str], negatives: List[str]) -> NLPArtifacts:
        classifier = self._get_classifier()
        if classifier is not None:
            try:
                result = classifier(text[:512])[0]
                label = result["label"].lower()
                score = float(result["score"])
                return NLPArtifacts(sentiment_label=label, sentiment_confidence=score)
            except Exception:
                pass

        raw = len(positives) - len(negatives)
        confidence = min(0.95, 0.55 + abs(raw) * 0.08)
        if raw > 0:
            label = "positive"
        elif raw < 0:
            label = "negative"
        else:
            label = "neutral"
        return NLPArtifacts(sentiment_label=label, sentiment_confidence=confidence)

    def _build_sentiment_breakdown(
        self,
        sentiment: NLPArtifacts,
        positive_hits: int,
        negative_hits: int,
        uncertainty_hits: int,
    ) -> Dict[str, float]:
        base_pos = 0.33
        base_neg = 0.33
        base_neu = 0.34

        if sentiment.sentiment_label == "positive":
            base_pos += 0.25 * sentiment.sentiment_confidence
            base_neg -= 0.12
        elif sentiment.sentiment_label == "negative":
            base_neg += 0.25 * sentiment.sentiment_confidence
            base_pos -= 0.12
        else:
            base_neu += 0.18 * sentiment.sentiment_confidence

        base_pos += positive_hits * 0.04
        base_neg += negative_hits * 0.04
        base_neu += uncertainty_hits * 0.03

        values = [max(0.01, v) for v in [base_pos, base_neg, base_neu]]
        total = sum(values)
        normalized = [round(v / total, 3) for v in values]
        correction = 1.0 - sum(normalized)
        normalized[2] = round(normalized[2] + correction, 3)
        return {"positive": normalized[0], "negative": normalized[1], "neutral": normalized[2]}

    def _build_summary(
        self,
        headline: str,
        event_type: str,
        sector: str,
        positives: List[str],
        negatives: List[str],
        uncertainty: List[str],
    ) -> str:
        tone = "mixed"
        if len(positives) > len(negatives):
            tone = "constructive"
        elif len(negatives) > len(positives):
            tone = "cautious"

        return (
            f"{headline} is classified as a {event_type.replace('_', ' ')} event in the {sector} sector. "
            f"The signal mix is {tone}, with {len(positives)} positive cues, {len(negatives)} negative cues, "
            f"and {len(uncertainty)} uncertainty markers influencing market interpretation."
        )
```

## `backend/app/services/outcome_engine.py`

```py
from __future__ import annotations

from typing import List

from app.schemas.simulation import AgentReaction, MarketOutcome, ScenarioControls, StructuredEvent, TimelinePoint


class OutcomeEngine:
    def synthesize(
        self,
        structured_event: StructuredEvent,
        reactions: List[AgentReaction],
        timeline: List[TimelinePoint],
        scenario: ScenarioControls,
    ) -> MarketOutcome:
        final_round = timeline[-1] if timeline else None
        avg_confidence = sum(r.confidence for r in reactions) / max(len(reactions), 1)
        aggregate_conviction = sum(r.conviction_score for r in reactions) / max(len(reactions), 1)
        disagreement = sum(t.disagreement for t in timeline) / max(len(timeline), 1)

        expected_move_pct = (final_round.expected_price_move_pct if final_round else aggregate_conviction * 2.0)
        expected_move_pct *= 1 + scenario.shock_intensity * 0.3
        expected_move_pct = round(expected_move_pct, 2)

        if expected_move_pct > 0.5:
            direction = "Bullish"
        elif expected_move_pct < -0.5:
            direction = "Bearish"
        else:
            direction = "Sideways / Mixed"

        volatility_index = round((final_round.volatility_index if final_round else 35.0) + scenario.liquidity_stress * 12, 2)
        if volatility_index >= 65:
            volatility_level = "High"
        elif volatility_index >= 45:
            volatility_level = "Moderate"
        else:
            volatility_level = "Low"

        reversal_probability = min(
            0.95,
            max(
                0.05,
                0.22
                + disagreement * 0.38
                + abs(structured_event.sentiment_breakdown["positive"] - structured_event.sentiment_breakdown["negative"]) * 0.15
                + scenario.uncertainty_bias * 0.18,
            ),
        )

        low = max(0.05, avg_confidence - 0.16 - disagreement * 0.08)
        high = min(0.99, avg_confidence + 0.10 - scenario.uncertainty_bias * 0.04)

        dominant_narrative = self._dominant_narrative(structured_event, direction, volatility_level)
        return MarketOutcome(
            expected_price_direction=direction,
            expected_price_move_pct=expected_move_pct,
            volatility_level=volatility_level,
            volatility_index=volatility_index,
            reversal_probability=round(reversal_probability, 3),
            confidence_range={"low": round(low, 3), "high": round(high, 3)},
            dominant_narrative=dominant_narrative,
        )

    def _dominant_narrative(self, event: StructuredEvent, direction: str, volatility_level: str) -> str:
        pos = len(event.positives)
        neg = len(event.negatives)
        unc = len(event.uncertainty)
        return (
            f"{direction} bias driven by a {event.event_type.replace('_', ' ')} interpretation in {event.sector}, "
            f"with {pos} positive signals, {neg} negative signals, and {unc} uncertainty markers. "
            f"Volatility is expected to remain {volatility_level.lower()} while market participants digest the narrative."
        )
```

## `backend/app/services/simulation_engine.py`

```py
from __future__ import annotations

from app.schemas.simulation import EventInput, MarketContext, SimulationResponse
from app.services.agent_factory import AgentFactory
from app.services.interaction_engine import InteractionEngine
from app.services.nlp_service import NLPService
from app.services.outcome_engine import OutcomeEngine


class SimulationEngine:
    def __init__(self) -> None:
        self.nlp_service = NLPService()
        self.agent_factory = AgentFactory()
        self.interaction_engine = InteractionEngine()
        self.outcome_engine = OutcomeEngine()

    def run(self, payload: EventInput, market_context: MarketContext) -> SimulationResponse:
        structured_event = self.nlp_service.analyze(payload.headline, payload.article)
        rounds = ["immediate", "short_term", "medium_term"]
        reactions = self.agent_factory.generate_reactions(
            structured_event=structured_event,
            scenario=payload.scenario,
            market_context=market_context,
            rounds=rounds,
        )
        timeline = self.interaction_engine.build_timeline(reactions)
        outcome = self.outcome_engine.synthesize(
            structured_event=structured_event,
            reactions=reactions,
            timeline=timeline,
            scenario=payload.scenario,
        )
        return SimulationResponse(
            structured_event=structured_event,
            market_context=market_context,
            agent_reactions=reactions,
            timeline=timeline,
            outcome=outcome,
            run_id=0,
        )
```

## `backend/app/utils/keywords.py`

```py
POSITIVE_KEYWORDS = {
    "beats", "beat", "surge", "growth", "record", "raises", "upgrade", "profit", "expands",
    "strong", "outperform", "wins", "contract", "accelerates", "optimistic", "improves", "approval",
    "partnership", "rebound", "recover", "upside", "bullish", "guidance raised"
}

NEGATIVE_KEYWORDS = {
    "misses", "miss", "cuts", "cut", "warning", "warns", "weak", "slows", "lawsuit", "probe",
    "decline", "drops", "drop", "lower", "downgrade", "recall", "loss", "headwind", "soft",
    "delays", "risk", "uncertain", "pressure", "fall", "bearish", "demand slowdown"
}

UNCERTAINTY_KEYWORDS = {
    "may", "could", "uncertain", "mixed", "volatile", "guidance", "outlook", "possible", "watch",
    "pending", "regulatory", "macro", "seasonal", "depends", "if", "however", "but"
}

EVENT_TYPE_KEYWORDS = {
    "earnings": ["earnings", "revenue", "guidance", "quarter", "profit"],
    "merger_acquisition": ["acquire", "merger", "buyout", "takeover"],
    "product_launch": ["launch", "release", "rollout", "debut"],
    "regulatory": ["regulator", "antitrust", "probe", "approval", "lawsuit"],
    "pricing": ["price cut", "pricing", "discount", "tariff"],
    "contract": ["contract", "deal", "agreement", "partnership"],
    "macro": ["inflation", "rates", "fed", "macro", "economy"],
}

SECTOR_KEYWORDS = {
    "Technology": ["ai", "software", "semiconductor", "chip", "cloud", "iphone", "data center"],
    "Automotive": ["ev", "vehicle", "auto", "battery", "tesla"],
    "Financials": ["bank", "insurance", "fintech", "credit", "brokerage"],
    "Healthcare": ["drug", "fda", "biotech", "hospital", "medical"],
    "Energy": ["oil", "gas", "solar", "energy"],
    "Consumer": ["retail", "consumer", "demand", "brand", "ecommerce"],
}
```

## `backend/requirements.txt`

```txt
fastapi==0.115.6
uvicorn[standard]==0.32.1
sqlalchemy==2.0.36
pydantic==2.10.3
pydantic-settings==2.6.1
python-dotenv==1.0.1
httpx==0.28.1
yfinance==0.2.54
pandas==2.2.3
numpy==2.1.3
transformers==4.47.0
torch==2.5.1
python-multipart==0.0.19
```

## `data/sample_events.json`

```json
[
  {
    "ticker": "AAPL",
    "headline": "Apple beats earnings expectations but warns of softer iPhone demand in China",
    "article": "Apple reported quarterly revenue above analyst expectations and raised services growth commentary, but management warned that iPhone demand in China may remain soft over the next quarter."
  },
  {
    "ticker": "TSLA",
    "headline": "Tesla announces surprise price cuts amid slowing EV demand",
    "article": "Tesla lowered prices across several major markets in an effort to defend market share as electric vehicle demand weakened and competition intensified."
  },
  {
    "ticker": "NVDA",
    "headline": "NVIDIA secures large sovereign AI infrastructure contract and raises revenue outlook",
    "article": "The company signed a multi-year AI infrastructure deal and lifted forward revenue guidance, reinforcing confidence in data center demand and sovereign AI expansion."
  }
]
```

## `frontend/app/globals.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  color-scheme: dark;
}

body {
  background:
    radial-gradient(circle at top left, rgba(122, 162, 255, 0.12), transparent 35%),
    radial-gradient(circle at top right, rgba(102, 227, 196, 0.1), transparent 30%),
    #0a1020;
  color: #edf2ff;
}

.card {
  @apply rounded-2xl border border-white/10 bg-panel/80 backdrop-blur shadow-glow;
}

.metric-label {
  @apply text-xs uppercase tracking-[0.18em] text-white/50;
}

.metric-value {
  @apply mt-2 text-2xl font-semibold text-white;
}
```

## `frontend/app/layout.tsx`

```tsx
import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI-Powered Market Reaction Simulator",
  description: "Financial event simulation dashboard",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

## `frontend/app/page.tsx`

```tsx
"use client";

import { useEffect, useMemo, useState } from "react";
import AgentCard from "@/components/AgentCard";
import MetricCard from "@/components/MetricCard";
import SentimentBars from "@/components/SentimentBars";
import SimulationForm from "@/components/SimulationForm";
import TimelineChart from "@/components/TimelineChart";
import { fetchSampleEvents, simulateEvent } from "@/lib/api";
import { SampleEvent, ScenarioControls, SimulationResponse } from "@/lib/types";
import { BarChart3, BrainCircuit, Gauge, Waves } from "lucide-react";

const defaultScenario: ScenarioControls = {
  shock_intensity: 0.6,
  uncertainty_bias: 0.4,
  liquidity_stress: 0.3,
  narrative_persistence: 0.5,
};

export default function HomePage() {
  const [ticker, setTicker] = useState("AAPL");
  const [headline, setHeadline] = useState("Apple beats earnings expectations but warns of softer iPhone demand in China");
  const [article, setArticle] = useState("Apple reported quarterly revenue above analyst expectations and raised services growth commentary, but management warned that iPhone demand in China may remain soft over the next quarter.");
  const [scenario, setScenario] = useState<ScenarioControls>(defaultScenario);
  const [sampleEvents, setSampleEvents] = useState<SampleEvent[]>([]);
  const [result, setResult] = useState<SimulationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchSampleEvents().then(setSampleEvents).catch(() => setSampleEvents([]));
  }, []);

  useEffect(() => {
    handleSubmit();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleScenarioChange = (key: keyof ScenarioControls, value: number) => {
    setScenario((prev) => ({ ...prev, [key]: value }));
  };

  const handleSampleSelect = (event: SampleEvent) => {
    setTicker(event.ticker);
    setHeadline(event.headline);
    setArticle(event.article || "");
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await simulateEvent({ ticker, headline, article, scenario });
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  const groupedAgents = useMemo(() => {
    if (!result) return {} as Record<string, SimulationResponse["agent_reactions"]>;
    return result.agent_reactions.reduce((acc, item) => {
      if (!acc[item.round]) acc[item.round] = [];
      acc[item.round].push(item);
      return acc;
    }, {} as Record<string, SimulationResponse["agent_reactions"]>);
  }, [result]);

  return (
    <main className="min-h-screen px-4 py-8 md:px-8 lg:px-12">
      <div className="mx-auto max-w-7xl space-y-8">
        <section className="card overflow-hidden p-8">
          <div className="grid gap-8 lg:grid-cols-[1.5fr_1fr] lg:items-end">
            <div>
              <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-accent/20 bg-accent/10 px-3 py-1 text-xs font-medium uppercase tracking-[0.2em] text-accent">
                <BrainCircuit size={14} /> Multi-Agent Financial Intelligence
              </div>
              <h1 className="max-w-4xl text-4xl font-semibold tracking-tight text-white md:text-5xl">
                AI-Powered Market Reaction Simulator
              </h1>
              <p className="mt-4 max-w-3xl text-base leading-7 text-white/65 md:text-lg">
                Convert earnings headlines, guidance changes, regulatory developments, and surprise announcements into structured event intelligence, simulated market participant reactions, and tradeable scenario dashboards.
              </p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="rounded-2xl border border-white/10 bg-white/5 p-5">
                <Gauge className="text-accent" />
                <div className="mt-3 text-sm text-white/60">Outcome Engine</div>
                <div className="mt-1 text-xl font-semibold text-white">Direction + Volatility</div>
              </div>
              <div className="rounded-2xl border border-white/10 bg-white/5 p-5">
                <BarChart3 className="text-accent" />
                <div className="mt-3 text-sm text-white/60">Scenario Testing</div>
                <div className="mt-1 text-xl font-semibold text-white">Interactive Reruns</div>
              </div>
            </div>
          </div>
        </section>

        <SimulationForm
          ticker={ticker}
          headline={headline}
          article={article}
          scenario={scenario}
          sampleEvents={sampleEvents}
          loading={loading}
          onTickerChange={setTicker}
          onHeadlineChange={setHeadline}
          onArticleChange={setArticle}
          onScenarioChange={handleScenarioChange}
          onSampleSelect={handleSampleSelect}
          onSubmit={handleSubmit}
        />

        {error ? (
          <div className="rounded-2xl border border-rose-500/20 bg-rose-500/10 p-4 text-rose-200">{error}</div>
        ) : null}

        {result ? (
          <>
            <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
              <MetricCard label="Expected Direction" value={result.outcome.expected_price_direction} subtext={result.outcome.dominant_narrative} />
              <MetricCard label="Expected Move" value={`${result.outcome.expected_price_move_pct}%`} subtext="Round-adjusted directional impact" />
              <MetricCard label="Volatility Outlook" value={result.outcome.volatility_level} subtext={`Index ${result.outcome.volatility_index}`} />
              <MetricCard label="Reversal Probability" value={`${Math.round(result.outcome.reversal_probability * 100)}%`} subtext={`Confidence ${Math.round(result.outcome.confidence_range.low * 100)}-${Math.round(result.outcome.confidence_range.high * 100)}%`} />
            </section>

            <section className="grid gap-6 xl:grid-cols-[1.25fr_0.75fr]">
              <div className="card p-6">
                <div className="flex items-center gap-3">
                  <Waves className="text-accent" />
                  <div>
                    <h2 className="text-xl font-semibold text-white">Structured Event Summary</h2>
                    <p className="mt-1 text-sm text-white/55">Event parsing, sector classification, and market context.</p>
                  </div>
                </div>

                <p className="mt-5 leading-7 text-white/75">{result.structured_event.summary}</p>

                <div className="mt-6 grid gap-4 md:grid-cols-2">
                  <div className="rounded-2xl bg-white/5 p-4">
                    <div className="text-sm text-white/50">Event Type</div>
                    <div className="mt-1 text-lg font-semibold capitalize text-white">{result.structured_event.event_type.replaceAll("_", " ")}</div>
                  </div>
                  <div className="rounded-2xl bg-white/5 p-4">
                    <div className="text-sm text-white/50">Sector</div>
                    <div className="mt-1 text-lg font-semibold text-white">{result.structured_event.sector}</div>
                  </div>
                </div>

                <div className="mt-6 grid gap-4 md:grid-cols-3">
                  <div className="rounded-2xl bg-emerald-500/10 p-4">
                    <div className="text-sm text-emerald-200/70">Positives</div>
                    <div className="mt-3 flex flex-wrap gap-2">
                      {result.structured_event.positives.length ? result.structured_event.positives.map((item) => (
                        <span key={item} className="rounded-full bg-emerald-500/10 px-3 py-1 text-xs text-emerald-200">{item}</span>
                      )) : <span className="text-sm text-white/50">None detected</span>}
                    </div>
                  </div>
                  <div className="rounded-2xl bg-rose-500/10 p-4">
                    <div className="text-sm text-rose-200/70">Negatives</div>
                    <div className="mt-3 flex flex-wrap gap-2">
                      {result.structured_event.negatives.length ? result.structured_event.negatives.map((item) => (
                        <span key={item} className="rounded-full bg-rose-500/10 px-3 py-1 text-xs text-rose-200">{item}</span>
                      )) : <span className="text-sm text-white/50">None detected</span>}
                    </div>
                  </div>
                  <div className="rounded-2xl bg-amber-500/10 p-4">
                    <div className="text-sm text-amber-200/70">Uncertainty</div>
                    <div className="mt-3 flex flex-wrap gap-2">
                      {result.structured_event.uncertainty.length ? result.structured_event.uncertainty.map((item) => (
                        <span key={item} className="rounded-full bg-amber-500/10 px-3 py-1 text-xs text-amber-100">{item}</span>
                      )) : <span className="text-sm text-white/50">None detected</span>}
                    </div>
                  </div>
                </div>

                <div className="mt-6 grid gap-4 md:grid-cols-2">
                  <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                    <div className="text-sm text-white/50">Ticker / Close</div>
                    <div className="mt-1 text-lg font-semibold text-white">{result.market_context.ticker || "N/A"} {result.market_context.latest_close ? `· ${result.market_context.latest_close}` : ""}</div>
                  </div>
                  <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                    <div className="text-sm text-white/50">5D Return / Realized Vol</div>
                    <div className="mt-1 text-lg font-semibold text-white">
                      {result.market_context.return_5d_pct ?? "N/A"} {typeof result.market_context.return_5d_pct === "number" ? "%" : ""}
                      {" · "}
                      {result.market_context.realized_volatility ?? "N/A"}
                    </div>
                  </div>
                </div>
              </div>

              <SentimentBars breakdown={result.structured_event.sentiment_breakdown} />
            </section>

            <TimelineChart data={result.timeline} />

            <section className="space-y-6">
              {Object.entries(groupedAgents).map(([round, agents]) => (
                <div key={round}>
                  <div className="mb-4 flex items-center justify-between">
                    <h2 className="text-2xl font-semibold capitalize text-white">{round.replaceAll("_", " ")} Reactions</h2>
                    <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs uppercase tracking-[0.18em] text-white/55">
                      {agents.length} agents
                    </span>
                  </div>
                  <div className="grid gap-4 xl:grid-cols-2">
                    {agents.map((agent, index) => (
                      <AgentCard key={`${agent.agent_name}-${index}`} agent={agent} />
                    ))}
                  </div>
                </div>
              ))}
            </section>
          </>
        ) : null}
      </div>
    </main>
  );
}
```

## `frontend/components/AgentCard.tsx`

```tsx
import { Brain, Clock3, ShieldAlert, TrendingDown, TrendingUp } from "lucide-react";

const actionStyles = {
  buy: "bg-emerald-500/15 text-emerald-300 border-emerald-400/20",
  sell: "bg-rose-500/15 text-rose-300 border-rose-400/20",
  hold: "bg-white/10 text-white/80 border-white/10",
};

type AgentCardProps = {
  agent: {
    agent_name: string;
    interpretation: string;
    action: "buy" | "sell" | "hold";
    confidence: number;
    time_horizon: string;
    round: string;
    conviction_score: number;
  };
};

export default function AgentCard({ agent }: AgentCardProps) {
  const trendIcon = agent.action === "buy" ? TrendingUp : agent.action === "sell" ? TrendingDown : ShieldAlert;
  const Icon = trendIcon;

  return (
    <div className="card p-5">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="text-lg font-semibold text-white">{agent.agent_name}</h3>
          <p className="mt-1 text-sm capitalize text-white/50">{agent.round.replace("_", " ")} round</p>
        </div>
        <span className={`rounded-full border px-3 py-1 text-xs font-semibold uppercase ${actionStyles[agent.action]}`}>
          {agent.action}
        </span>
      </div>

      <p className="mt-4 text-sm leading-6 text-white/75">{agent.interpretation}</p>

      <div className="mt-4 grid grid-cols-3 gap-3 text-sm">
        <div className="rounded-xl bg-white/5 p-3">
          <div className="flex items-center gap-2 text-white/50"><Brain size={14} /> Confidence</div>
          <div className="mt-2 font-semibold text-white">{Math.round(agent.confidence * 100)}%</div>
        </div>
        <div className="rounded-xl bg-white/5 p-3">
          <div className="flex items-center gap-2 text-white/50"><Clock3 size={14} /> Horizon</div>
          <div className="mt-2 font-semibold capitalize text-white">{agent.time_horizon}</div>
        </div>
        <div className="rounded-xl bg-white/5 p-3">
          <div className="flex items-center gap-2 text-white/50"><Icon size={14} /> Conviction</div>
          <div className="mt-2 font-semibold text-white">{agent.conviction_score.toFixed(2)}</div>
        </div>
      </div>
    </div>
  );
}
```

## `frontend/components/MetricCard.tsx`

```tsx
type MetricCardProps = {
  label: string;
  value: string;
  subtext?: string;
};

export default function MetricCard({ label, value, subtext }: MetricCardProps) {
  return (
    <div className="card p-5">
      <div className="metric-label">{label}</div>
      <div className="metric-value">{value}</div>
      {subtext ? <p className="mt-2 text-sm text-white/60">{subtext}</p> : null}
    </div>
  );
}
```

## `frontend/components/SentimentBars.tsx`

```tsx
type SentimentBarsProps = {
  breakdown: Record<string, number>;
};

export default function SentimentBars({ breakdown }: SentimentBarsProps) {
  const items = [
    { key: "positive", label: "Positive" },
    { key: "negative", label: "Negative" },
    { key: "neutral", label: "Neutral" },
  ];

  return (
    <div className="card p-5">
      <h3 className="text-lg font-semibold text-white">Sentiment Breakdown</h3>
      <div className="mt-5 space-y-4">
        {items.map((item) => {
          const value = Math.max(0, Math.min(100, Math.round((breakdown[item.key] || 0) * 100)));
          return (
            <div key={item.key}>
              <div className="mb-2 flex items-center justify-between text-sm text-white/70">
                <span>{item.label}</span>
                <span>{value}%</span>
              </div>
              <div className="h-3 overflow-hidden rounded-full bg-white/10">
                <div className="h-full rounded-full bg-gradient-to-r from-accent2 to-accent" style={{ width: `${value}%` }} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
```

## `frontend/components/SimulationForm.tsx`

```tsx
"use client";

import { ChangeEvent } from "react";
import { SampleEvent, ScenarioControls } from "@/lib/types";

type SimulationFormProps = {
  ticker: string;
  headline: string;
  article: string;
  scenario: ScenarioControls;
  sampleEvents: SampleEvent[];
  loading: boolean;
  onTickerChange: (value: string) => void;
  onHeadlineChange: (value: string) => void;
  onArticleChange: (value: string) => void;
  onScenarioChange: (key: keyof ScenarioControls, value: number) => void;
  onSampleSelect: (event: SampleEvent) => void;
  onSubmit: () => void;
};

const sliders: Array<{ key: keyof ScenarioControls; label: string; helper: string }> = [
  { key: "shock_intensity", label: "Shock Intensity", helper: "Amplifies directional reaction" },
  { key: "uncertainty_bias", label: "Uncertainty Bias", helper: "Raises narrative ambiguity" },
  { key: "liquidity_stress", label: "Liquidity Stress", helper: "Widens market maker caution" },
  { key: "narrative_persistence", label: "Narrative Persistence", helper: "Extends medium-term follow through" },
];

export default function SimulationForm(props: SimulationFormProps) {
  const {
    ticker,
    headline,
    article,
    scenario,
    sampleEvents,
    loading,
    onTickerChange,
    onHeadlineChange,
    onArticleChange,
    onScenarioChange,
    onSampleSelect,
    onSubmit,
  } = props;

  return (
    <div className="card p-6">
      <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
        <div>
          <h2 className="text-2xl font-semibold text-white">Run Simulation</h2>
          <p className="mt-1 text-sm text-white/60">Input a market-moving event and rerun alternate scenarios instantly.</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {sampleEvents.map((event) => (
            <button
              key={`${event.ticker}-${event.headline}`}
              onClick={() => onSampleSelect(event)}
              className="rounded-full border border-white/10 bg-white/5 px-3 py-2 text-xs font-medium text-white/80 transition hover:bg-white/10"
            >
              {event.ticker}
            </button>
          ))}
        </div>
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <label className="block">
          <span className="mb-2 block text-sm font-medium text-white/75">Ticker</span>
          <input
            value={ticker}
            onChange={(e) => onTickerChange(e.target.value.toUpperCase())}
            placeholder="AAPL"
            className="w-full rounded-xl border border-white/10 bg-ink px-4 py-3 text-white outline-none focus:border-accent"
          />
        </label>

        <label className="block md:col-span-2">
          <span className="mb-2 block text-sm font-medium text-white/75">Headline</span>
          <input
            value={headline}
            onChange={(e) => onHeadlineChange(e.target.value)}
            placeholder="Apple beats earnings expectations but warns of softer demand"
            className="w-full rounded-xl border border-white/10 bg-ink px-4 py-3 text-white outline-none focus:border-accent"
          />
        </label>

        <label className="block md:col-span-2">
          <span className="mb-2 block text-sm font-medium text-white/75">Article / Context</span>
          <textarea
            value={article}
            onChange={(e) => onArticleChange(e.target.value)}
            rows={5}
            placeholder="Paste article details or management commentary here..."
            className="w-full rounded-xl border border-white/10 bg-ink px-4 py-3 text-white outline-none focus:border-accent"
          />
        </label>
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        {sliders.map((slider) => (
          <div key={slider.key} className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm font-medium text-white">{slider.label}</div>
                <div className="mt-1 text-xs text-white/50">{slider.helper}</div>
              </div>
              <div className="text-sm font-semibold text-accent">{scenario[slider.key].toFixed(2)}</div>
            </div>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={scenario[slider.key]}
              onChange={(e: ChangeEvent<HTMLInputElement>) => onScenarioChange(slider.key, Number(e.target.value))}
              className="mt-4 w-full"
            />
          </div>
        ))}
      </div>

      <button
        onClick={onSubmit}
        disabled={loading || !headline.trim()}
        className="mt-6 inline-flex items-center rounded-xl bg-accent px-5 py-3 font-semibold text-ink transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {loading ? "Running simulation..." : "Simulate Market Reaction"}
      </button>
    </div>
  );
}
```

## `frontend/components/TimelineChart.tsx`

```tsx
"use client";

import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

type TimelineChartProps = {
  data: {
    round: string;
    expected_price_move_pct: number;
    volatility_index: number;
  }[];
};

export default function TimelineChart({ data }: TimelineChartProps) {
  const normalized = data.map((item) => ({
    ...item,
    round: item.round.replace("_", " "),
  }));

  return (
    <div className="card p-5">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-white">Timeline Simulation</h3>
        <p className="mt-1 text-sm text-white/60">Price movement and volatility across interaction rounds.</p>
      </div>
      <div className="h-[320px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={normalized}>
            <CartesianGrid stroke="rgba(255,255,255,0.08)" vertical={false} />
            <XAxis dataKey="round" stroke="rgba(255,255,255,0.45)" />
            <YAxis stroke="rgba(255,255,255,0.45)" />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="expected_price_move_pct" name="Expected Move %" strokeWidth={3} />
            <Line type="monotone" dataKey="volatility_index" name="Volatility Index" strokeWidth={3} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
```

## `frontend/lib/api.ts`

```ts
import { EventInput, SampleEvent, SimulationResponse } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";

export async function fetchSampleEvents(): Promise<SampleEvent[]> {
  const res = await fetch(`${API_BASE_URL}/sample-events`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error("Failed to load sample events");
  }
  return res.json();
}

export async function simulateEvent(payload: EventInput): Promise<SimulationResponse> {
  const res = await fetch(`${API_BASE_URL}/simulate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const detail = await res.text();
    throw new Error(detail || "Simulation request failed");
  }

  return res.json();
}
```

## `frontend/lib/types.ts`

```ts
export type ScenarioControls = {
  shock_intensity: number;
  uncertainty_bias: number;
  liquidity_stress: number;
  narrative_persistence: number;
};

export type EventInput = {
  ticker?: string;
  headline: string;
  article?: string;
  scenario: ScenarioControls;
};

export type SimulationResponse = {
  structured_event: {
    summary: string;
    positives: string[];
    negatives: string[];
    uncertainty: string[];
    event_type: string;
    sector: string;
    sentiment_breakdown: Record<string, number>;
    sentiment_score: number;
  };
  market_context: {
    ticker?: string | null;
    latest_close?: number | null;
    avg_volume?: number | null;
    return_5d_pct?: number | null;
    realized_volatility?: number | null;
  };
  agent_reactions: {
    agent_name: string;
    interpretation: string;
    action: "buy" | "sell" | "hold";
    confidence: number;
    time_horizon: string;
    round: string;
    conviction_score: number;
  }[];
  timeline: {
    round: string;
    net_pressure: number;
    consensus: number;
    disagreement: number;
    expected_price_move_pct: number;
    volatility_index: number;
  }[];
  outcome: {
    expected_price_direction: string;
    expected_price_move_pct: number;
    volatility_level: string;
    volatility_index: number;
    reversal_probability: number;
    confidence_range: { low: number; high: number };
    dominant_narrative: string;
  };
  run_id: number;
};

export type SampleEvent = {
  ticker: string;
  headline: string;
  article?: string;
};
```

## `frontend/next-env.d.ts`

```ts
/// <reference types="next" />
/// <reference types="next/image-types/global" />

// This file is auto-generated by Next.js.
```

## `frontend/next.config.js`

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
};

module.exports = nextConfig;
```

## `frontend/package.json`

```json
{
  "name": "market-reaction-simulator-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "clsx": "^2.1.1",
    "lucide-react": "^0.468.0",
    "next": "14.2.24",
    "react": "18.3.1",
    "react-dom": "18.3.1",
    "recharts": "^2.15.0"
  },
  "devDependencies": {
    "@types/node": "^22.10.2",
    "@types/react": "^18.3.12",
    "@types/react-dom": "^18.3.1",
    "autoprefixer": "^10.4.20",
    "postcss": "^8.4.49",
    "tailwindcss": "^3.4.16",
    "typescript": "^5.7.2"
  }
}
```

## `frontend/postcss.config.js`

```js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

## `frontend/tailwind.config.ts`

```ts
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: "#0b1020",
        panel: "#121932",
        panelSoft: "#182242",
        accent: "#66e3c4",
        accent2: "#7aa2ff",
        warn: "#ffb020",
      },
      boxShadow: {
        glow: "0 10px 30px rgba(102,227,196,0.12)",
      },
    },
  },
  plugins: [],
};

export default config;
```

## `frontend/tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": false,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "baseUrl": ".",
    "paths": {
      "@/components/*": ["components/*"],
      "@/lib/*": ["lib/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

