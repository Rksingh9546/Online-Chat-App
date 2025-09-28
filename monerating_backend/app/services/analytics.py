from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

import numpy as np
from nltk.sentiment import SentimentIntensityAnalyzer


_sentiment_analyzer: SentimentIntensityAnalyzer | None = None


def _get_vader() -> SentimentIntensityAnalyzer:
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        try:
            _sentiment_analyzer = SentimentIntensityAnalyzer()
        except LookupError:
            import nltk

            nltk.download("vader_lexicon")
            _sentiment_analyzer = SentimentIntensityAnalyzer()
    return _sentiment_analyzer


def compute_sentiment(text: str) -> float:
    if not text:
        return 0.0
    analyzer = _get_vader()
    scores = analyzer.polarity_scores(text)
    return float(scores.get("compound", 0.0))


def linear_trend(values: Sequence[float]) -> float:
    if len(values) < 2:
        return 0.0
    x = np.arange(len(values))
    y = np.array(values, dtype=float)
    slope, _ = np.polyfit(x, y, 1)
    return float(slope)


@dataclass
class AnomalyResult:
    indices: List[int]
    threshold: float


def zscore_anomalies(values: Sequence[float], z_threshold: float = 2.5) -> AnomalyResult:
    if len(values) == 0:
        return AnomalyResult(indices=[], threshold=z_threshold)
    arr = np.array(values, dtype=float)
    mean = arr.mean()
    std = arr.std() or 1.0
    z = (arr - mean) / std
    idx = [int(i) for i, val in enumerate(z) if abs(val) >= z_threshold]
    return AnomalyResult(indices=idx, threshold=z_threshold)

