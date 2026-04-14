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
