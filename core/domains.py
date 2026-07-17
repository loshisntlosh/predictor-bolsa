# core/domains.py
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class MarketMetrics:
    current_price: float
    price_change: float
    percentage_change: float
    currency: str
    short_ratio: float
    revenue_growth: float
    debt_to_equity: float

@dataclass(frozen=True)
class TargetForecast:
    low: float
    median: float
    high: float

@dataclass(frozen=True)
class CatalystEvent:
    event_name: str
    projected_date: str
    direction: str  # "BULL" o "BEAR"
    impact_level: str
    desc: str

@dataclass(frozen=True)
class QuantAssessment:
    verdict: str
    confidence_score: float
    hex_color: str
    margin_of_safety: float
    estimated_drawdown: float
    raw_score: float

@dataclass(frozen=True)
class TrumpPredictionResult:
    policy_vector: str
    impact_score: float
    sentiment_label: str
    analysis_justification: str
    last_update_date: str

@dataclass(frozen=True)
class InstitutionalThesis:
    date: str
    author: str
    stance: str  # "Bullish", "Bearish", "Neutral"
    thesis_text: str
    ai_critique: str
    is_valid: bool

@dataclass(frozen=True)
class RadarRecommendation:
    ticker: str
    sector: str
    action: str  # "COMPRA FUERTE", "EVITAR/CORTO"
    justification: str
    score: float