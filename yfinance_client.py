import yfinance as yf
import pandas as pd
from typing import Tuple, Optional
from core.domains import MarketMetrics, TargetForecast
from core.exceptions import MarketDataFetchError

class InvestmentDataClient:
    def __init__(self, ticker_symbol: str):
        self.symbol = ticker_symbol.upper()
        self._ticker = yf.Ticker(self.symbol)

    def fetch_market_snapshot(self) -> Tuple[MarketMetrics, TargetForecast, Optional[pd.DataFrame]]:
        try:
            info = self._ticker.info
            if not info or ('regularMarketPrice' not in info and 'currentPrice' not in info):
                raise MarketDataFetchError(f"Métricas insuficientes o ticker inválido: {self.symbol}")
            
            current_price = float(info.get('currentPrice', info.get('regularMarketPrice', 0.0)))
            
            metrics = MarketMetrics(
                current_price=current_price,
                previous_close=float(info.get('previousClose', current_price)),
                volume=int(info.get('regularMarketVolume', 0)),
                revenue_growth=float(info.get('revenueGrowth', 0.0)),
                roe=float(info.get('returnOnEquity', 0.0)),
                debt_to_equity=float(info.get('debtToEquity', 0.0)),
                short_ratio=float(info.get('shortRatio', 1.5)),
                currency=info.get('currency', 'USD')
            )
            
            forecast = TargetForecast(
                low=float(info.get('targetLowPrice', current_price * 0.9)),
                median=float(info.get('targetMedianPrice', current_price * 1.05)),
                high=float(info.get('targetHighPrice', current_price * 1.15))
            )
            
            try:
                insiders = self._ticker.insider_transactions
            except Exception:
                insiders = None

            return metrics, forecast, insiders
            
        except Exception as e:
            raise MarketDataFetchError(f"Fallo en infraestructura de datos: {str(e)}") from e