# app.py
import streamlit as st
from infrastructure.yfinance_client import InvestmentDataClient
from core.engine import InstitutionalQuantEngine, MacroStressEngine, TrumpPredictionEngine, HighFrequencyScannerEngine
from core.exceptions import QuantMatrixError
import presentation.components as ui

st.set_page_config(layout="wide", page_title="Institutional Quant Matrix", page_icon="🏛️")
ui.render_injection_styles()

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
    st.caption("Terminal Ponderada por IA Cuántica (Entorno 2026)")

if seccion == "📡 Radar Escáner 15m":
    st.markdown("<h1 class='main-title'>📡 Escáner de Flujo de Alta Frecuencia</h1>", unsafe_allow_html=True)
    recom_radar = HighFrequencyScannerEngine.ejecutar_escaneo_15m()
    ui.render_high_frequency_radar(recom_radar)

else:
    st.markdown("<h1 class='main-title'>🏛️ Terminal Institutional Alpha Matrix</h1>", unsafe_allow_html=True)
    ticker_input = st.text_input("🔍 Ingrese el Ticker de la Acción para Desglose Profundo:", "AVGO").upper()

    if ticker_input:
        try:
            client = InvestmentDataClient(ticker_input)
            with st.spinner("Desencriptando métricas y orderbooks en Wall Street..."):
                metrics, forecast, insiders = client.fetch_market_snapshot()
            
            catalysts, raw_score = InstitutionalQuantEngine.analizar_catalizadores_y_cronograma(metrics, insiders)
            assessment = InstitutionalQuantEngine.motor_imparcial_ia(client._ticker.news, raw_score, metrics, forecast)
            theses_institucionales = InstitutionalQuantEngine.obtener_tesis_recientes(ticker_input, metrics)
            # Nuevo cálculo estratégico de horizontes
            estrategias_tiempo = InstitutionalQuantEngine.calcular_estrategia_horizontes(ticker_input, metrics, forecast)

            nombre_empresa = client._ticker.info.get('longName', ticker_input)
            ui.render_realtime_price_header(ticker_input, nombre_empresa, metrics)
            
            if seccion == "🏛️ Terminal Institucional":
                st.subheader("🤖 Diagnóstico Cuantitativo de Riesgo Ponderado por IA")
                ui.render_assessment_card(assessment)
                
                # INYECCIÓN DEL COMPONENTE DE HORIZONTES DE INVERSIÓN (CUÁNDO COMPRAR / VENDER / RETENER)
                ui.render_horizon_strategies(estrategias_tiempo)
                st.markdown("---")
                
                st.markdown("### 🧬 Indicadores de Asimetría Justificados Objetivamente")
                col_u1, col_u2, col_u3 = st.columns(3)
                
                with col_u1:
                    fatiga = "⚠️ FATIGA CRÍTICA" if metrics.short_ratio < 1.5 else "🟢 FLUJO SALUDABLE"
                    color_f = "#ef4444" if metrics.short_ratio < 1.5 else "#22c55e"
                    st.markdown(f"""
                    <div class="scenario-card">
                        <h5>⚠️ Saturación de Flujos</h5>
                        <h3 style="color:{color_f};">{fatiga}</h3>
                        <p style="font-size:0.88em;color:#cbd5e1;">Métrica: {metrics.short_ratio:.2f} días de cobertura. Dinámica institucional dominante.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col_u2:
                    opacidad = "🚨 CRÍTICO: ALTO APALANCAMIENTO" if metrics.debt_to_equity > 120.0 else "⚖️ CLARIDAD ESTÁNDAR"
                    color_o = "#ef4444" if metrics.debt_to_equity > 120.0 else "#38bdf8"
                    st.markdown(f"""
                    <div class="scenario-card">
                        <h5>🎭 Opacidad y Estructura</h5>
                        <h3 style="color:{color_o};">{opacidad}</h3>
                        <p style="font-size:0.88em;color:#cbd5e1;">Apalancamiento indexado: {metrics.debt_to_equity:.1f}%. Evaluación extrema de pasivos.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col_u3:
                    st.markdown(f"""
                    <div class="scenario-card">
                        <h5>📉 Valor en Riesgo Dinámico (VaR)</h5>
                        <h3 style="color:#ef4444;">-{assessment.estimated_drawdown:.1f}% Max</h3>
                        <p style="font-size:0.88em;color:#cbd5e1;">Umbral simulado bajo volatilidad implícita del entorno macro actual.</p>
                    </div>
                    """, unsafe_allow_html=True)

            elif seccion == "🎯 Tesis de Fondos e IA Oracle":
                ui.render_audited_institutional_theses(ticker_input, theses_institucionales)
                st.markdown("---")
                ui.render_ai_hyper_forecast_box(ticker_input, metrics, assessment)

            elif seccion == "🦅 Trumprediction":
                impactos_politicos = TrumpPredictionEngine.calculate_political_exposure(metrics, ticker_input)
                ui.render_trump_prediction_dashboard(ticker_input, impactos_politicos, metrics.current_price)

            elif seccion == "📅 Cronograma de Eventos":
                st.subheader("📅 Cronograma Predictivo de Ventanas de Impacto")
                ui.render_timeline(catalysts)

            elif seccion == "📊 Gráfico de Precios":
                st.subheader("📊 Serie Temporal de Cierre (Últimos 3 Meses)")
                historial = client._ticker.history(period="3mo", interval="1d")
                if not historial.empty:
                    st.line_chart(historial['Close'], use_container_width=True)
                    
            elif seccion == "🌋 Simulador de Estrés Macro":
                st.subheader("🌋 Simulador de Regímenes de Estrés")
                shocks_proyectados = MacroStressEngine.simulate_regime_shocks(metrics, forecast)
                ui.render_stress_testing_dashboard(shocks_proyectados)

        except QuantMatrixError as e:
            st.error(f"Error operativo controlado: {str(e)}")
        except Exception as e:
            st.error(f"Error inesperado en los flujos de la terminal: {str(e)}")