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
