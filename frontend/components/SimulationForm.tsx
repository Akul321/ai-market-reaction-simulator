"use client";

import { ChangeEvent } from "react";
import { SampleEvent, ScenarioControls } from "@/lib/types";

type SimulationFormProps = {
  ticker: string;
  headline: string;
  article: string;
  scenario: ScenarioControls;
  sampleEvents: SampleEvent[];
  loading: boolean;
  onTickerChange: (value: string) => void;
  onHeadlineChange: (value: string) => void;
  onArticleChange: (value: string) => void;
  onScenarioChange: (key: keyof ScenarioControls, value: number) => void;
  onSampleSelect: (event: SampleEvent) => void;
  onSubmit: () => void;
};

const sliders: Array<{ key: keyof ScenarioControls; label: string; helper: string }> = [
  { key: "shock_intensity", label: "Shock Intensity", helper: "Amplifies directional reaction" },
  { key: "uncertainty_bias", label: "Uncertainty Bias", helper: "Raises narrative ambiguity" },
  { key: "liquidity_stress", label: "Liquidity Stress", helper: "Widens market maker caution" },
  { key: "narrative_persistence", label: "Narrative Persistence", helper: "Extends medium-term follow through" },
];

export default function SimulationForm(props: SimulationFormProps) {
  const {
    ticker,
    headline,
    article,
    scenario,
    sampleEvents,
    loading,
    onTickerChange,
    onHeadlineChange,
    onArticleChange,
    onScenarioChange,
    onSampleSelect,
    onSubmit,
  } = props;

  return (
    <div className="card p-6">
      <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
        <div>
          <h2 className="text-2xl font-semibold text-white">Run Simulation</h2>
          <p className="mt-1 text-sm text-white/60">Input a market-moving event and rerun alternate scenarios instantly.</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {sampleEvents.map((event) => (
            <button
              key={`${event.ticker}-${event.headline}`}
              onClick={() => onSampleSelect(event)}
              className="rounded-full border border-white/10 bg-white/5 px-3 py-2 text-xs font-medium text-white/80 transition hover:bg-white/10"
            >
              {event.ticker}
            </button>
          ))}
        </div>
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <label className="block">
          <span className="mb-2 block text-sm font-medium text-white/75">Ticker</span>
          <input
            value={ticker}
            onChange={(e) => onTickerChange(e.target.value.toUpperCase())}
            placeholder="AAPL"
            className="w-full rounded-xl border border-white/10 bg-ink px-4 py-3 text-white outline-none focus:border-accent"
          />
        </label>

        <label className="block md:col-span-2">
          <span className="mb-2 block text-sm font-medium text-white/75">Headline</span>
          <input
            value={headline}
            onChange={(e) => onHeadlineChange(e.target.value)}
            placeholder="Apple beats earnings expectations but warns of softer demand"
            className="w-full rounded-xl border border-white/10 bg-ink px-4 py-3 text-white outline-none focus:border-accent"
          />
        </label>

        <label className="block md:col-span-2">
          <span className="mb-2 block text-sm font-medium text-white/75">Article / Context</span>
          <textarea
            value={article}
            onChange={(e) => onArticleChange(e.target.value)}
            rows={5}
            placeholder="Paste article details or management commentary here..."
            className="w-full rounded-xl border border-white/10 bg-ink px-4 py-3 text-white outline-none focus:border-accent"
          />
        </label>
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        {sliders.map((slider) => (
          <div key={slider.key} className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm font-medium text-white">{slider.label}</div>
                <div className="mt-1 text-xs text-white/50">{slider.helper}</div>
              </div>
              <div className="text-sm font-semibold text-accent">{scenario[slider.key].toFixed(2)}</div>
            </div>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={scenario[slider.key]}
              onChange={(e: ChangeEvent<HTMLInputElement>) => onScenarioChange(slider.key, Number(e.target.value))}
              className="mt-4 w-full"
            />
          </div>
        ))}
      </div>

      <button
        onClick={onSubmit}
        disabled={loading || !headline.trim()}
        className="mt-6 inline-flex items-center rounded-xl bg-accent px-5 py-3 font-semibold text-ink transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {loading ? "Running simulation..." : "Simulate Market Reaction"}
      </button>
    </div>
  );
}
