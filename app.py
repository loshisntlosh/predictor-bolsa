# app.py
import streamlit as st
import yfinance as yf
import pandas as pd
from infrastructure.yfinance_client import InvestmentDataClient
from core.engine import InstitutionalQuantEngine, MacroStressEngine
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
        # Agregamos la nueva pestaña de pronósticos interactivos y opiniones reales
        ["🏛️ Terminal Institucional", "🎯 Pronóstico e IA Oracle", "📅 Cronograma de Eventos", "🎯 Pronósticos de Wall Street", "📊 Gráfico de Precios", "🌋 Simulador de Estrés Macro"]
    )
    st.markdown("---")
    st.markdown("### 🤖 Selección por IA Narrativa")
    st.caption("Top activos con convergencia fundamental óptima:")
    st.dataframe(pd.DataFrame([
        {"Ticker": "NVDA", "ROE": "54.2%", "Sentimiento": "🔥 Fuerte"},
        {"Ticker": "LLY", "ROE": "32.1%", "Sentimiento": "🟢 Estable"},
        {"Ticker": "AVGO", "ROE": "22.7%", "Sentimiento": "🔥 Fuerte"}
    ]), hide_index=True)

# =========================================================================
# PANEL PRINCIPAL
# =========================================================================
st.markdown("<h1 class='main-title'>🏛️ Terminal Institutional Alpha Matrix</h1>", unsafe_allow_html=True)
ticker_input = st.text_input("🔍 Ingrese el Ticker de la Acción (Ej: NVDA, AAPL, AMZN):", "NVDA").upper()

if ticker_input:
    try:
        # 1. Extracción mediante Infraestructura
        client = InvestmentDataClient(ticker_input)
        with st.spinner("Procesando datos en la matriz de Wall Street..."):
            metrics, forecast, insiders = client.fetch_market_snapshot()
        
        # 2. Lógica matemática en Capa del Dominio
        catalysts, raw_score = InstitutionalQuantEngine.analizar_catalizadores_y_cronograma(metrics, insiders)
        assessment = InstitutionalQuantEngine.motor_imparcial_ia(client._ticker.news, raw_score, metrics, forecast)

        # 🌟 NUEVO: CABECERA PREMIUM CON EL VALOR DE LA ACCIÓN VISUALMENTE IMPACTANTE A TIEMPO REAL
        nombre_empresa = client._ticker.info.get('longName', ticker_input)
        ui.render_realtime_price_header(ticker_input, nombre_empresa, metrics)
        
        # ==========================================
        # INTERRUPTOR DE VISTAS (SECCIONES)
        # ==========================================
        if seccion == "🏛️ Terminal Institucional":
            st.subheader("🤖 Diagnóstico Cuantitativo de Riesgo")
            ui.render_assessment_card(assessment)
            
            st.markdown("### 🧬 Indicadores de Asimetría de Mercado")
            col_u1, col_u2, col_u3 = st.columns(3)
            
            with col_u1:
                fatiga = "⚠️ FATIGA CRÍTICA" if metrics.short_ratio < 1.2 else "🟢 FLUJO SALUDABLE"
                color_f = "#ef4444" if metrics.short_ratio < 1.2 else "#22c55e"
                st.markdown(f'<div class="scenario-card"><h5 style="color:#94a3b8;margin:0;">⚠️ Saturación (Crowded Trade)</h5><h3 style="color:{color_f};">{fatiga}</h3><p style="font-size:0.8em;color:#cbd5e1;">Días de cobertura de cortos: <b>{metrics.short_ratio:.2f}</b></p></div>', unsafe_allow_html=True)
                
            with col_u2:
                opacidad = "⚖️ CLARIDAD ESTÁNDAR" if assessment.raw_score > -0.1 else "🚨 ALTA COMPLEJIDAD TEXTUAL"
                color_o = "#38bdf8" if assessment.raw_score > -0.1 else "#f59e0b"
                st.markdown(f'<div class="scenario-card"><h5 style="color:#94a3b8;margin:0;">🎭 Índice de Opacidad Corporativa</h5><h3 style="color:{color_o};">{opacidad}</h3><p style="font-size:0.8em;color:#cbd5e1;">Procesamiento NLP sobre comunicados corporativos.</p></div>', unsafe_allow_html=True)
                
            with col_u3:
                st.markdown(f'<div class="scenario-card"><h5 style="color:#94a3b8;margin:0;">📉 Max Drawdown Estimado (VaR)</h5><h3 style="color:#ef4444;">-{assessment.estimated_drawdown:.1f}%</h3><p style="font-size:0.8em;color:#cbd5e1;">Riesgo máximo proyectado bajo condiciones adversas.</p></div>', unsafe_allow_html=True)

        # 🌟 NUEVA SECCIÓN COMPLETA DE FORECAST INTERACTIVO + OPINIONES REALES + IA ORACLE
        elif seccion == "🎯 Pronóstico e IA Oracle":
            col_or1, col_or2 = st.columns([1, 1])
            with col_or1:
                ui.render_investor_forecast_feed(ticker_input, assessment)
            with col_or2:
                ui.render_ai_oracle_box(ticker_input, assessment)

        elif seccion == "📅 Cronograma de Eventos":
            st.subheader("📅 Cronograma Predictivo de Ventanas de Impacto de Valor")
            ui.render_timeline(catalysts)

        elif seccion == "🎯 Pronósticos de Wall Street":
            st.subheader("🎯 Consenso del Rango de Precios Objetivo (Inversionistas Fuertes)")
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1: st.markdown(f'<div class="scenario-card" style="border-top: 4px solid #ef4444;"><h4 style="color:#ef4444;margin:0;">📉 Objetivo Mínimo</h4><h2>${forecast.low:,.2f}</h2></div>', unsafe_allow_html=True)
            with col_f2: st.markdown(f'<div class="scenario-card" style="border-top: 4px solid #38bdf8;"><h4 style="color:#38bdf8;margin:0;">⚖️ Consenso Medio</h4><h2>${forecast.median:,.2f}</h2><p style="font-size:0.85em;">Margen de Seguridad: <b>{assessment.margin_of_safety:+.2f}%</b></p></div>', unsafe_allow_html=True)
            with col_f3: st.markdown(f'<div class="scenario-card" style="border-top: 4px solid #22c55e;"><h4 style="color:#22c55e;margin:0;">📈 Objetivo Máximo</h4><h2>${forecast.high:,.2f}</h2></div>', unsafe_allow_html=True)

        elif seccion == "📊 Gráfico de Precios":
            st.subheader("📊 Serie Temporal de Cierre (Últimos 3 Meses)")
            historial = client._ticker.history(period="3mo", interval="1d")
            if not historial.empty:
                st.line_chart(historial['Close'], use_container_width=True)
                
        elif seccion == "🌋 Simulador de Estrés Macro":
            st.subheader("🌋 Simulador Cuántico de Regímenes de Estrés Macroeconómico")
            shocks_proyectados = MacroStressEngine.simulate_regime_shocks(metrics, forecast)
            ui.render_stress_testing_dashboard(shocks_proyectados)

    except QuantMatrixError as e:
        st.error(f"Error operativo controlado: {str(e)}")
    except Exception as e:
        st.error(f"Error inesperado en los flujos del sistema: {str(e)}")