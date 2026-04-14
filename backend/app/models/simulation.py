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
