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
