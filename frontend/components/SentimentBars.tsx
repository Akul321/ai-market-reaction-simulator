type SentimentBarsProps = {
  breakdown: Record<string, number>;
};

export default function SentimentBars({ breakdown }: SentimentBarsProps) {
  const items = [
    { key: "positive", label: "Positive" },
    { key: "negative", label: "Negative" },
    { key: "neutral", label: "Neutral" },
  ];

  return (
    <div className="card p-5">
      <h3 className="text-lg font-semibold text-white">Sentiment Breakdown</h3>
      <div className="mt-5 space-y-4">
        {items.map((item) => {
          const value = Math.max(0, Math.min(100, Math.round((breakdown[item.key] || 0) * 100)));
          return (
            <div key={item.key}>
              <div className="mb-2 flex items-center justify-between text-sm text-white/70">
                <span>{item.label}</span>
                <span>{value}%</span>
              </div>
              <div className="h-3 overflow-hidden rounded-full bg-white/10">
                <div className="h-full rounded-full bg-gradient-to-r from-accent2 to-accent" style={{ width: `${value}%` }} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
