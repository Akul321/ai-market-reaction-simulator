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
