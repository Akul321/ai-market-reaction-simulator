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
