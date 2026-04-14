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
