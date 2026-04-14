from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Dict, List, Optional

from app.core.config import settings
from app.schemas.simulation import StructuredEvent
from app.utils.keywords import EVENT_TYPE_KEYWORDS, NEGATIVE_KEYWORDS, POSITIVE_KEYWORDS, SECTOR_KEYWORDS, UNCERTAINTY_KEYWORDS

try:
    from transformers import pipeline
except Exception:  # pragma: no cover
    pipeline = None


@dataclass
class NLPArtifacts:
    sentiment_label: str
    sentiment_confidence: float


class NLPService:
    """Financial NLP parser with a Hugging Face primary path and heuristic fallback."""

    def __init__(self) -> None:
        self._classifier = None
        self._load_failed = False

    def _get_classifier(self):
        if self._classifier is not None:
            return self._classifier
        if self._load_failed or pipeline is None:
            return None
        try:
            self._classifier = pipeline(
                "text-classification",
                model=settings.huggingface_model_name,
                tokenizer=settings.huggingface_model_name,
                truncation=True,
            )
            return self._classifier
        except Exception:
            self._load_failed = True
            return None

    def analyze(self, headline: str, article: Optional[str] = None) -> StructuredEvent:
        text = f"{headline}. {article or ''}".strip()
        cleaned = self._normalize(text)

        positives = self._extract_signals(cleaned, POSITIVE_KEYWORDS)
        negatives = self._extract_signals(cleaned, NEGATIVE_KEYWORDS)
        uncertainty = self._extract_signals(cleaned, UNCERTAINTY_KEYWORDS)
        event_type = self._infer_event_type(cleaned)
        sector = self._infer_sector(cleaned)
        sentiment = self._get_sentiment(cleaned, positives, negatives)
        sentiment_breakdown = self._build_sentiment_breakdown(sentiment, len(positives), len(negatives), len(uncertainty))
        sentiment_score = sentiment_breakdown["positive"] - sentiment_breakdown["negative"]
        summary = self._build_summary(headline, event_type, sector, positives, negatives, uncertainty)

        return StructuredEvent(
            summary=summary,
            positives=positives,
            negatives=negatives,
            uncertainty=uncertainty,
            event_type=event_type,
            sector=sector,
            sentiment_breakdown=sentiment_breakdown,
            sentiment_score=round(sentiment_score, 3),
        )

    def _normalize(self, text: str) -> str:
        return re.sub(r"\s+", " ", text.lower()).strip()

    def _extract_signals(self, text: str, keywords: set[str]) -> List[str]:
        hits = []
        for kw in sorted(keywords):
            if kw in text:
                hits.append(kw)
        return hits[:6]

    def _infer_event_type(self, text: str) -> str:
        best_label, best_score = "general_corporate", 0
        for label, keywords in EVENT_TYPE_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > best_score:
                best_label, best_score = label, score
        return best_label

    def _infer_sector(self, text: str) -> str:
        best_label, best_score = "Broad Market", 0
        for label, keywords in SECTOR_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > best_score:
                best_label, best_score = label, score
        return best_label

    def _get_sentiment(self, text: str, positives: List[str], negatives: List[str]) -> NLPArtifacts:
        classifier = self._get_classifier()
        if classifier is not None:
            try:
                result = classifier(text[:512])[0]
                label = result["label"].lower()
                score = float(result["score"])
                return NLPArtifacts(sentiment_label=label, sentiment_confidence=score)
            except Exception:
                pass

        raw = len(positives) - len(negatives)
        confidence = min(0.95, 0.55 + abs(raw) * 0.08)
        if raw > 0:
            label = "positive"
        elif raw < 0:
            label = "negative"
        else:
            label = "neutral"
        return NLPArtifacts(sentiment_label=label, sentiment_confidence=confidence)

    def _build_sentiment_breakdown(
        self,
        sentiment: NLPArtifacts,
        positive_hits: int,
        negative_hits: int,
        uncertainty_hits: int,
    ) -> Dict[str, float]:
        base_pos = 0.33
        base_neg = 0.33
        base_neu = 0.34

        if sentiment.sentiment_label == "positive":
            base_pos += 0.25 * sentiment.sentiment_confidence
            base_neg -= 0.12
        elif sentiment.sentiment_label == "negative":
            base_neg += 0.25 * sentiment.sentiment_confidence
            base_pos -= 0.12
        else:
            base_neu += 0.18 * sentiment.sentiment_confidence

        base_pos += positive_hits * 0.04
        base_neg += negative_hits * 0.04
        base_neu += uncertainty_hits * 0.03

        values = [max(0.01, v) for v in [base_pos, base_neg, base_neu]]
        total = sum(values)
        normalized = [round(v / total, 3) for v in values]
        correction = 1.0 - sum(normalized)
        normalized[2] = round(normalized[2] + correction, 3)
        return {"positive": normalized[0], "negative": normalized[1], "neutral": normalized[2]}

    def _build_summary(
        self,
        headline: str,
        event_type: str,
        sector: str,
        positives: List[str],
        negatives: List[str],
        uncertainty: List[str],
    ) -> str:
        tone = "mixed"
        if len(positives) > len(negatives):
            tone = "constructive"
        elif len(negatives) > len(positives):
            tone = "cautious"

        return (
            f"{headline} is classified as a {event_type.replace('_', ' ')} event in the {sector} sector. "
            f"The signal mix is {tone}, with {len(positives)} positive cues, {len(negatives)} negative cues, "
            f"and {len(uncertainty)} uncertainty markers influencing market interpretation."
        )
