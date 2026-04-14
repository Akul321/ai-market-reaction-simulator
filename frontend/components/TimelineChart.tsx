"use client";

import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

type TimelineChartProps = {
  data: {
    round: string;
    expected_price_move_pct: number;
    volatility_index: number;
  }[];
};

export default function TimelineChart({ data }: TimelineChartProps) {
  const normalized = data.map((item) => ({
    ...item,
    round: item.round.replace("_", " "),
  }));

  return (
    <div className="card p-5">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-white">Timeline Simulation</h3>
        <p className="mt-1 text-sm text-white/60">Price movement and volatility across interaction rounds.</p>
      </div>
      <div className="h-[320px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={normalized}>
            <CartesianGrid stroke="rgba(255,255,255,0.08)" vertical={false} />
            <XAxis dataKey="round" stroke="rgba(255,255,255,0.45)" />
            <YAxis stroke="rgba(255,255,255,0.45)" />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="expected_price_move_pct" name="Expected Move %" strokeWidth={3} />
            <Line type="monotone" dataKey="volatility_index" name="Volatility Index" strokeWidth={3} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
