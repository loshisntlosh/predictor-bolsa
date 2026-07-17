# core/domains.py
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class MarketMetrics:
    current_price: float = 0.0
    price_change: float = 0.0
    percentage_change: float = 0.0
    currency: str = "USD"
    short_ratio: float = 0.0
    revenue_growth: float = 0.0
    debt_to_equity: float = 0.0
    previous_close: float = 0.0
    volume: float = 0.0

    def __init__(self, current_price: float = 0.0, price_change: float = 0.0, percentage_change: float = 0.0, 
                 currency: str = "USD", short_ratio: float = 0.0, revenue_growth: float = 0.0, debt_to_equity: float = 0.0, 
                 previous_close: float = 0.0, volume: float = 0.0, **kwargs):
        object.__setattr__(self, 'current_price', current_price)
        object.__setattr__(self, 'price_change', price_change)
        object.__setattr__(self, 'percentage_change', percentage_change)
        object.__setattr__(self, 'currency', currency)
        object.__setattr__(self, 'short_ratio', short_ratio)
        object.__setattr__(self, 'revenue_growth', revenue_growth)
        object.__setattr__(self, 'debt_to_equity', debt_to_equity)
        object.__setattr__(self, 'previous_close', previous_close)
        object.__setattr__(self, 'volume', volume)

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
    hedging_strategy: str  # NUEVO: Estrategia de cobertura institucional
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