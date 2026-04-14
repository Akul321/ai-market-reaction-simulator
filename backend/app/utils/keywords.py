POSITIVE_KEYWORDS = {
    "beats", "beat", "surge", "growth", "record", "raises", "upgrade", "profit", "expands",
    "strong", "outperform", "wins", "contract", "accelerates", "optimistic", "improves", "approval",
    "partnership", "rebound", "recover", "upside", "bullish", "guidance raised"
}

NEGATIVE_KEYWORDS = {
    "misses", "miss", "cuts", "cut", "warning", "warns", "weak", "slows", "lawsuit", "probe",
    "decline", "drops", "drop", "lower", "downgrade", "recall", "loss", "headwind", "soft",
    "delays", "risk", "uncertain", "pressure", "fall", "bearish", "demand slowdown"
}

UNCERTAINTY_KEYWORDS = {
    "may", "could", "uncertain", "mixed", "volatile", "guidance", "outlook", "possible", "watch",
    "pending", "regulatory", "macro", "seasonal", "depends", "if", "however", "but"
}

EVENT_TYPE_KEYWORDS = {
    "earnings": ["earnings", "revenue", "guidance", "quarter", "profit"],
    "merger_acquisition": ["acquire", "merger", "buyout", "takeover"],
    "product_launch": ["launch", "release", "rollout", "debut"],
    "regulatory": ["regulator", "antitrust", "probe", "approval", "lawsuit"],
    "pricing": ["price cut", "pricing", "discount", "tariff"],
    "contract": ["contract", "deal", "agreement", "partnership"],
    "macro": ["inflation", "rates", "fed", "macro", "economy"],
}

SECTOR_KEYWORDS = {
    "Technology": ["ai", "software", "semiconductor", "chip", "cloud", "iphone", "data center"],
    "Automotive": ["ev", "vehicle", "auto", "battery", "tesla"],
    "Financials": ["bank", "insurance", "fintech", "credit", "brokerage"],
    "Healthcare": ["drug", "fda", "biotech", "hospital", "medical"],
    "Energy": ["oil", "gas", "solar", "energy"],
    "Consumer": ["retail", "consumer", "demand", "brand", "ecommerce"],
}
