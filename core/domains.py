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
    previous_close: float = 0.0
    volume: float = 0.0  # Corrección: Añadido soporte para el argumento inesperado enviado por la infraestructura

@dataclass(frozen=True)
class TargetForecast:
    low: float
    median: float
    high: float

@dataclass(frozen=True)
class CatalystEvent:
    event_name: str
    projected_date: str
    direction: str  
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
class HorizonStrategy:
    horizon: str  
    action: str   
    rationale: str
    target_window: str

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
    stance: str  
    thesis_text: str
    ai_critique: str
    is_valid: bool

@dataclass(frozen=True)
class RadarRecommendation:
    ticker: str
    sector: str
    action: str  
    justification: str
    score: float