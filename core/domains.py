from dataclasses import dataclass
from typing import List, Optional
from datetime import date

@dataclass(frozen=True)
class MarketMetrics:
    current_price: float
    previous_close: float
    volume: int
    revenue_growth: float
    roe: float
    debt_to_equity: float
    short_ratio: float
    currency: str = "USD"

    @property
    def price_change(self) -> float:
        return self.current_price - self.previous_close

    @property
    def percentage_change(self) -> float:
        return (self.price_change / self.previous_close) * 100

@dataclass(frozen=True)
class TargetForecast:
    low: float
    median: float
    high: float

@dataclass(frozen=True)
class CatalystEvent:
    event_name: str
    impact_level: str  # CRITICAL, HIGH, MEDIUM
    direction: str     # BULL, BEAR
    projected_date: date
    desc: str

@dataclass(frozen=True)
class QuantAssessment:
    verdict: str
    hex_color: str
    confidence_score: float
    raw_score: float
    margin_of_safety: float
    estimated_drawdown: float

@dataclass(frozen=True)
class MacroShockResult:
    scenario_name: str
    implied_beta_shift: float
    projected_price: float
    risk_level: str  # EXTREME, ELEVATED, MITIGATED
    vulnerability_index: float  # 0.0 a 100.0

@dataclass(frozen=True)
class TrumpPredictionResult:
    policy_vector: str        # E.g., "Aranceles Agresivos", "Desregulación"
    impact_score: float       # Escala de -100 a +100
    sentiment_label: str      # "BENEFICIARIO DIRECTO", "BAJO FUEGO CRUZADO", "NEUTRAL"
    analysis_justification: str
    last_update_date: str     # Fecha de verificación estricta (Julio 2026)
