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
