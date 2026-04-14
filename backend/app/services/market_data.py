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
