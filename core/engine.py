from datetime import datetime, timedelta
from typing import List, Tuple, Optional
import pandas as pd
from core.domains import MarketMetrics, TargetForecast, CatalystEvent, QuantAssessment

class InstitutionalQuantEngine:
    @staticmethod
    def analizar_catalizadores_y_cronograma(metrics: MarketMetrics, df_insiders: Optional[pd.DataFrame]) -> Tuple[List[CatalystEvent], float]:
        catalizadores: List[CatalystEvent] = []
        score_puntos = 0.0
        fecha_base = datetime.now().date()
        
        # 1. Análisis de ROE
        if metrics.roe > 0.25:
            catalizadores.append(CatalystEvent(
                event_name="🎯 ROE Institucional Sobresaliente", impact_level="ALTO", direction="BULL",
                projected_date=fecha_base + timedelta(days=45),
                desc=f"Rentabilidad sobre capital del {metrics.roe*100:.1f}%. Alta eficiencia estructural."
            ))
            score_puntos += 25
        elif metrics.roe < 0.05 and metrics.roe != 0.0:
            catalizadores.append(CatalystEvent(
                event_name="⚠️ Destrucción de Valor sobre Capital (Bajo ROE)", impact_level="ALTO", direction="BEAR",
                projected_date=fecha_base + timedelta(days=15),
                desc=f"El ROE de {metrics.roe*100:.1f}% indica ineficiencia severa en el uso del dinero."
            ))
            score_puntos -= 25

        # 2. Análisis de Ingresos YoY
        if metrics.revenue_growth > 0.15:
            catalizadores.append(CatalystEvent(
                event_name="🚀 Aceleración de Ingresos Orgánicos YoY", impact_level="CRÍTICO", direction="BULL",
                projected_date=fecha_base + timedelta(days=30),
                desc=f"Ventas creciendo a un ritmo del {metrics.revenue_growth*100:.1f}% interanual."
            ))
            score_puntos += 30
        elif metrics.revenue_growth < 0.0:
            catalizadores.append(CatalystEvent(
                event_name="🚨 Contracción de Ventas (Revenue Drop)", impact_level="CRÍTICO", direction="BEAR",
                projected_date=fecha_base + timedelta(days=10),
                desc=f"Pérdida de ingresos del {abs(metrics.revenue_growth*100):.1f}% interanual. Alerta de mercado."
            ))
            score_puntos -= 35

        # 3. Ratio de Apalancamiento Financiero
        if metrics.debt_to_equity > 150.0:
            catalizadores.append(CatalystEvent(
                event_name="🚨 Apalancamiento Financiero Crítico (D/E Alto)", impact_level="ALTO", direction="BEAR",
                projected_date=fecha_base + timedelta(days=20),
                desc=f"Deuda equivale al {metrics.debt_to_equity:.1f}% del capital. Alto riesgo ante tasas elevadas."
            ))
            score_puntos -= 25
        elif metrics.debt_to_equity < 70.0 and metrics.debt_to_equity > 0:
            score_puntos += 15

        # 4. Monitoreo SEC Insiders
        if df_insiders is not None and not df_insiders.empty:
            ventas_insider = df_insiders[(df_insiders['Text'].str.contains('Sale|Sell', case=False, na=False)) & (df_insiders['Value'] > 1000000)]
            if not ventas_insider.empty:
                catalizadores.append(CatalystEvent(
                    event_name="📉 Liquidación Masiva de Acciones (Insider Selling)", impact_level="ALTO", direction="BEAR",
                    projected_date=fecha_base + timedelta(days=5),
                    desc="Altos ejecutivos liquidando posiciones millonarias. Riesgo de toma de utilidades interna."
                ))
                score_puntos -= 20

        return catalizadores, score_puntos

    @staticmethod
    def motor_imparcial_ia(noticias: Optional[List[dict]], score_puntos: float, metrics: MarketMetrics, forecast: TargetForecast) -> QuantAssessment:
        score_narrativa = 0.0
        alcistas = ['growth', 'profit', 'buy', 'upgrade', 'beats', 'surge']
        bajistas = ['lawsuit', 'loss', 'downgrade', 'regulatory', 'investigation', 'misses', 'drop']
        
        if noticias:
            for n in noticias:
                titulo = n.get('title', '').lower()
                score_narrativa += sum(0.2 for w in alcistas if w in titulo) - sum(0.2 for w in bajistas if w in titulo)
            score_narrativa = score_narrativa / len(noticias)

        desviacion_target = (forecast.median - metrics.current_price) / metrics.current_price if forecast.median > 0 else 0.0
        score_final_ia = (score_narrativa * 0.20) + ((score_puntos / 100) * 0.55) + (desviacion_target * 0.25)
        score_final_ia = max(min(score_final_ia, 1.0), -1.0)
        
        porcentaje_confianza = abs(score_final_ia) * 100
        margin_of_safety = ((forecast.median - metrics.current_price) / forecast.median) * 100 if forecast.median > 0 else 0.0
        estimated_drawdown = max(4.5, 14.0 - (score_final_ia * 22))
        
        if score_final_ia > 0.12:
            return QuantAssessment("⚡ ALCISTA ESTRUCTURAL", "#22c55e", porcentaje_confianza, score_final_ia, margin_of_safety, estimated_drawdown)
        elif score_final_ia < -0.12:
            return QuantAssessment("🚨 RIESGO BAJISTA SEVERO", "#ef4444", porcentaje_confianza, score_final_ia, margin_of_safety, estimated_drawdown)
        else:
            return QuantAssessment("⚖️ DISTRIBUCIÓN LATERAL", "#94a3b8", porcentaje_confianza, score_final_ia, margin_of_safety, estimated_drawdown)