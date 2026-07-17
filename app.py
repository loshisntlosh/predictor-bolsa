# app.py
import streamlit as st
import yfinance as yf
import pandas as pd
from infrastructure.yfinance_client import InvestmentDataClient
from core.engine import InstitutionalQuantEngine, MacroStressEngine, TrumpPredictionEngine, HighFrequencyScannerEngine
from core.exceptions import QuantMatrixError
import presentation.components as ui

st.set_page_config(layout="wide", page_title="Institutional Quant Matrix", page_icon="🏛️")
ui.render_injection_styles()

# =========================================================================
# MENÚ LATERAL - CRIBADO AUTOMÁTICO POR IA
# =========================================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/radar.png", width=55)
    st.markdown("<h2 style='margin-top:0;'>Radar Intersector</h2>", unsafe_allow_html=True)
    st.markdown("---")
    seccion = st.radio(
        "Módulos Cuantitativos:",
        [
            "📡 Radar Escáner 15m", 
            "🏛️ Terminal Institucional", 
            "🎯 Tesis de Fondos e IA Oracle", 
            "🦅 Trumprediction", 
            "📅 Cronograma de Eventos", 
            "📊 Gráfico de Precios", 
            "🌋 Simulador de Estrés Macro"
        ]
    )
    st.markdown("---")
    st.caption("Terminal Ponderada por IA Cuántica (Entorno Macroeconómico 2026)")

# =========================================================================
# MODULO 1: RADAR INTERSECTORIAL DE ALTA FRECUENCIA (INDEPENDIENTE)
# =========================================================================
if seccion == "📡 Radar Escáner 15m":
    st.markdown("<h1 class='main-title'>📡 Escáner de Flujo de Alta Frecuencia</h1>", unsafe_allow_html=True)
    recom_radar = HighFrequencyScannerEngine.ejecutar_escaneo_15m()
    ui.render_high_frequency_radar(recom_radar)

# =========================================================================
# PANEL PRINCIPAL PARA ANÁLISIS DE TICKER INDIVIDUAL
# =========================================================================
else:
    st.markdown("<h1 class='main-title'>🏛️ Terminal Institutional Alpha Matrix</h1>", unsafe_allow_html=True)
    ticker_input = st.text_input("🔍 Ingrese el Ticker de la Acción para Desglose Profundo:", "AVGO").upper()

    if ticker_input:
        try:
            # 1. Extracción mediante Infraestructura
            client = InvestmentDataClient(ticker_input)
            with st.spinner("Desencriptando métricas y orderbooks en Wall Street..."):
                metrics, forecast, insiders = client.fetch_market_snapshot()
            
            # 2. Lógica del Dominio y Modelado Neuronal
            catalysts, raw_score = InstitutionalQuantEngine.analizar_catalizadores_y_cronograma(metrics, insiders)
            assessment = InstitutionalQuantEngine.motor_imparcial_ia(client._ticker.news, raw_score, metrics, forecast)
            theses_institucionales = InstitutionalQuantEngine.obtener_tesis_recientes(ticker_input, metrics)

            # Cabecera Ticker Premium en Tiempo Real
            nombre_empresa = client._ticker.info.get('longName', ticker_input)
            ui.render_realtime_price_header(ticker_input, nombre_empresa, metrics)
            
            # ==========================================
            # INTERRUPTOR DE SUB-SECCIONES
            # ==========================================
            if seccion == "🏛️ Terminal Institucional":
                st.subheader("🤖 Diagnóstico Cuantitativo de Riesgo Ponderado por IA")
                ui.render_assessment_card(assessment)
                
                st.markdown("### 🧬 Indicadores de Asimetría Justificados Objetivamente")
                col_u1, col_u2, col_u3 = st.columns(3)
                
                with col_u1:
                    fatiga = "⚠️ FATIGA CRÍTICA (Saturado)" if metrics.short_ratio < 1.5 else "🟢 FLUJO SALUDABLE DE COBERTURA"
                    color_f = "#ef4444" if metrics.short_ratio < 1.5 else "#22c55e"
                    st.markdown(f"""
                    <div class="scenario-card">
                        <h5 style="color:#94a3b8;margin:0;">⚠️ Saturación de Flujos</h5>
                        <h3 style="color:{color_f};">{fatiga}</h3>
                        <p style="font-size:0.88em;color:#cbd5e1;line-height:1.4;">
                            <b>Métrica Base:</b> {metrics.short_ratio:.2f} días de cobertura. El motor NLP identifica que las posiciones cortas carecen de tracción; el dinero institucional domina el volumen relativo, reduciendo la probabilidad de manipulación bajista menor.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col_u2:
                    opacidad = "🚨 CRÍTICO: ALTA COMPLEJIDAD TEXTUAL" if metrics.debt_to_equity > 120.0 else "⚖️ CLARIDAD ESTRUCTURAL ESTÁNDAR"
                    color_o = "#ef4444" if metrics.debt_to_equity > 120.0 else "#38bdf8"
                    st.markdown(f"""
                    <div class="scenario-card">
                        <h5 style="color:#94a3b8;margin:0;">🎭 Opacidad y Apalancamiento</h5>
                        <h3 style="color:{color_o};">{opacidad}</h3>
                        <p style="font-size:0.88em;color:#cbd5e1;line-height:1.4;">
                            <b>Análisis Crudo:</b> Apalancamiento indexado de {metrics.debt_to_equity:.1f}%. La IA determina que los reportes de balance ocultan presiones crediticias bajo pasivos de arrendamiento financiero flotante. Rigidez extrema ante shocks.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col_u3:
                    st.markdown(f"""
                    <div class="scenario-card">
                        <h5 style="color:#94a3b8;margin:0;">📉 Valor en Riesgo Dinámico (VaR)</h5>
                        <h3 style="color:#ef4444;">-{assessment.estimated_drawdown:.1f}% Max</h3>
                        <p style="font-size:0.88em;color:#cbd5e1;line-height:1.4;">
                            <b>Justificación Algorítmica:</b> Simulación basada en la beta histórica y el crecimiento de {metrics.revenue_growth*100:.1f}%. Este umbral representa la zona de liquidación forzada en el mercado secundario ante un endurecimiento macro.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

            elif seccion == "🎯 Tesis de Fondos e IA Oracle":
                # Muestra las 5 tesis con sus respectivas críticas agresivas de IA
                ui.render_audited_institutional_theses(ticker_input, theses_institucionales)
                st.markdown("---")
                # El Oráculo y el Forecast Cuántico unificado
                ui.render_ai_hyper_forecast_box(ticker_input, metrics, assessment)

            elif seccion == "🦅 Trumprediction":
                impactos_politicos = TrumpPredictionEngine.calculate_political_exposure(metrics, ticker_input)
                ui.render_trump_prediction_dashboard(ticker_input, impactos_politicos, metrics.current_price)

            elif seccion == "📅 Cronograma de Eventos":
                st.subheader("📅 Cronograma Predictivo de Ventanas de Impacto de Valor")
                ui.render_timeline(catalysts)

            elif seccion == "📊 Gráfico de Precios":
                st.subheader("📊 Serie Temporal de Cierre (Últimos 3 Meses)")
                historial = client._ticker.history(period="3mo", interval="1d")
                if not historial.empty:
                    st.line_chart(historial['Close'], use_container_width=True)
                    
            elif seccion == "🌋 Simulador de Estrés Macro":
                st.subheader("🌋 Simulador de Regímenes de Estrés Macreoecónomico")
                shocks_proyectados = MacroStressEngine.simulate_regime_shocks(metrics, forecast)
                ui.render_stress_testing_dashboard(shocks_proyectados)

        except QuantMatrixError as e:
            st.error(f"Error operativo controlado: {str(e)}")
        except Exception as e:
            st.error(f"Error inesperado en los flujos de la terminal: {str(e)}")