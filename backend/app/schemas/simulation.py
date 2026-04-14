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
