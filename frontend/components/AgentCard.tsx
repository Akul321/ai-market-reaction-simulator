import { Brain, Clock3, ShieldAlert, TrendingDown, TrendingUp } from "lucide-react";

const actionStyles = {
  buy: "bg-emerald-500/15 text-emerald-300 border-emerald-400/20",
  sell: "bg-rose-500/15 text-rose-300 border-rose-400/20",
  hold: "bg-white/10 text-white/80 border-white/10",
};

type AgentCardProps = {
  agent: {
    agent_name: string;
    interpretation: string;
    action: "buy" | "sell" | "hold";
    confidence: number;
    time_horizon: string;
    round: string;
    conviction_score: number;
  };
};

export default function AgentCard({ agent }: AgentCardProps) {
  const trendIcon = agent.action === "buy" ? TrendingUp : agent.action === "sell" ? TrendingDown : ShieldAlert;
  const Icon = trendIcon;

  return (
    <div className="card p-5">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="text-lg font-semibold text-white">{agent.agent_name}</h3>
          <p className="mt-1 text-sm capitalize text-white/50">{agent.round.replace("_", " ")} round</p>
        </div>
        <span className={`rounded-full border px-3 py-1 text-xs font-semibold uppercase ${actionStyles[agent.action]}`}>
          {agent.action}
        </span>
      </div>

      <p className="mt-4 text-sm leading-6 text-white/75">{agent.interpretation}</p>

      <div className="mt-4 grid grid-cols-3 gap-3 text-sm">
        <div className="rounded-xl bg-white/5 p-3">
          <div className="flex items-center gap-2 text-white/50"><Brain size={14} /> Confidence</div>
          <div className="mt-2 font-semibold text-white">{Math.round(agent.confidence * 100)}%</div>
        </div>
        <div className="rounded-xl bg-white/5 p-3">
          <div className="flex items-center gap-2 text-white/50"><Clock3 size={14} /> Horizon</div>
          <div className="mt-2 font-semibold capitalize text-white">{agent.time_horizon}</div>
        </div>
        <div className="rounded-xl bg-white/5 p-3">
          <div className="flex items-center gap-2 text-white/50"><Icon size={14} /> Conviction</div>
          <div className="mt-2 font-semibold text-white">{agent.conviction_score.toFixed(2)}</div>
        </div>
      </div>
    </div>
  );
}
