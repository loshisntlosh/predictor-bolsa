import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# 1. CONFIGURACIÓN DE PANTALLA Y ESTILOS VISUALES TERMINAL PREMIUM
st.set_page_config(layout="wide", page_title="Intersector Institutional Analytics", page_icon="🏛️")

st.markdown("""
<style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .main-title { animation: fadeIn 0.8s ease-out; color: #f8fafc; font-weight: 800; }
    .prediction-box { 
        padding: 25px; border-radius: 12px; 
        text-align: center;
        animation: fadeIn 1s ease-out; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        margin-bottom: 25px;
    }
    .scenario-card {
        padding: 20px; border-radius: 12px; background-color: #0f172a;
        border: 1px solid #334155; animation: fadeIn 1.1s ease-out;
    }
    .catalyst-badge {
        padding: 6px 12px; border-radius: 6px; font-size: 0.85em; font-weight: bold;
        display: inline-block; margin-bottom: 8px;
    }
    .news-card {
        padding: 18px; border-radius: 10px; background-color: #1e293b; margin-bottom: 15px;
        border-left: 5px solid #06b6d4; animation: fadeIn 1.1s ease-out;
        transition: transform 0.2s, border-left 0.2s;
    }
    .news-card:hover { transform: scale(1.015); border-left: 5px solid #22c55e; background-color: #1e293bfa; }
</style>
""", unsafe_allow_html=True)

# =========================================================================
# MOTOR DE FILTRADO NLP Y FUNDAMENTAL DE MERCADO EN SEGUNDO PLANO
# =========================================================================
@st.cache_data(ttl=3600)
def escanear_mercado_por_ia():
    tickers_vigilancia = ["NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "LLY", "AVGO", "AMD"]
    lista_recomendados = []
    alcistas_clave = ['growth', 'profit', 'buy', 'upgrade', 'innovation', 'beats', 'surge']
    
    for tk in tickers_vigilancia:
        try:
            t_empresa = yf.Ticker(tk)
            t_info = t_empresa.info
            t_news = t_empresa.news
            
            score_n = 0
            if t_news:
                for n in t_news[:5]:
                    score_n += sum(1 for w in alcistas_clave if w in n.get('title', '').lower())
                    
            roe = t_info.get('returnOnEquity', 0.0)
            rev_growth = t_info.get('revenueGrowth', 0.0)
            
            if roe > 0.15 and rev_growth > 0.10:
                lista_recomendados.append({
                    "Ticker": tk,
                    "ROE": f"{roe*100:.1f}%",
                    "Crecimiento YoY": f"{rev_growth*100:.1f}%",
                    "Sentimiento": "🔥 Fuerte" if score_n > 2 else "🟢 Estable"
                })
        except:
            continue
    return pd.DataFrame(lista_recomendados).head(3)

# =========================================================================
# ESCÁNER CLÍTICO DE EQUILIBRIO DE CONTROL CORPORATIVO
# =========================================================================
def analizar_catalizadores_y_riesgos(info_empresa, df_insiders):
    catalizadores = []
    score_puntos = 0  # Escala balanceada: valores positivos son alcistas, negativos son bajistas
    
    # 1. Análisis Técnico de Múltiplos (PER y Margen)
    roe = info_empresa.get('returnOnEquity', 0.0)
    if roe > 0.25:
        catalizadores.append({"evento": "🎯 ROE Institucional Sobresaliente", "impacto": "ALTO", "tipo": "BULL", "desc": f"Rentabilidad sobre capital del {roe*100:.1f}%. Alta eficiencia."})
        score_puntos += 25
    elif roe < 0.05 and roe != 0.0:
        catalizadores.append({"evento": "⚠️ Destrucción de Valor sobre Capital (Bajo ROE)", "impacto": "ALTO", "tipo": "BEAR", "desc": f"El ROE de {roe*100:.1f}% indica ineficiencia severa en el uso del dinero de los inversionistas."})
        score_puntos -= 25

    # 2. Análisis del Impulso de Ventas
    crecimiento_ingresos = info_empresa.get('revenueGrowth', 0.0)
    if crecimiento_ingresos > 0.15:
        catalizadores.append({"evento": "🚀 Aceleración de Ingresos Orgánicos YoY", "impacto": "CRÍTICO", "tipo": "BULL", "desc": f"Ventas creciendo a un ritmo del {crecimiento_ingresos*100:.1f}% interanual."})
        score_puntos += 30
    elif crecimiento_ingresos < 0.0 and crecimiento_ingresos != 0.0:
        catalizadores.append({"evento": "🚨 Contracción de Ventas (Revenue Drop)", "impacto": "CRÍTICO", "tipo": "BEAR", "desc": f"Pérdida de ingresos del {crecimiento_ingresos*100:.1f}% interanual. Alerta de pérdida de mercado."})
        score_puntos -= 35

    # 3. Ratio de Apalancamiento Financiero
    ratio_deuda = info_empresa.get('debtToEquity', 100.0)
    if ratio_deuda > 150.0:
        catalizadores.append({"evento": "🚨 Apalancamiento Financiero Crítico (D/E Alto)", "impacto": "ALTO", "tipo": "BEAR", "desc": f"Deuda equivale al {ratio_deuda:.1f}% del capital. Alto riesgo ante tasas elevadas."})
        score_puntos -= 25
    elif ratio_deuda < 70.0:
        score_puntos += 15

    # 4. Flujo de Transacciones de Insiders SEC
    if df_insiders is not None and not df_insiders.empty:
        compras_insider = df_insiders[(df_insiders['Text'].str.contains('Buy|Purchase', case=False, na=False)) & (df_insiders['Value'] > 300000)]
        ventas_insider = df_insiders[(df_insiders['Text'].str.contains('Sale|Sell', case=False, na=False)) & (df_insiders['Value'] > 1000000)]
        
        if not compras_insider.empty:
            catalizadores.append({"evento": "💼 Respaldo Interno por Compras de Altos Mandos", "impacto": "CRÍTICO", "tipo": "BULL", "desc": "Directores adquiriendo acciones de gran volumen con su propio dinero."})
            score_puntos += 20
        if not ventas_insider.empty:
            catalizadores.append({"evento": "📉 Liquidación Masiva de Acciones (Insider Selling)", "impacto": "ALTO", "tipo": "BEAR", "desc": "Altos ejecutivos liquidando posiciones millonarias. Riesgo de toma de utilidades interna."})
            score_puntos -= 20

    return catalizadores, score_puntos

# =========================================================================
# MOTOR FINANCIERO CRUDO E IMPARCIAL DE IA
# =========================================================================
def motor_imparcial_ia(noticias, score_puntos, precio_actual, target_medio):
    score_narrativa = 0.0
    alcistas = ['growth', 'profit', 'buy', 'upgrade', 'beats', 'surge']
    bajistas = ['lawsuit', 'loss', 'downgrade', 'regulatory', 'investigation', 'misses', 'drop']
    
    if noticias:
        for n in noticias:
            titulo = n.get('title', '').lower()
            score_narrativa += sum(0.2 for w in alcistas if w in titulo) - sum(0.2 for w in bajistas if w in titulo)
        score_narrativa = score_narrativa / len(noticias)

    # Desviación implícita de Wall Street
    desviacion_target = (target_medio - precio_actual) / precio_actual if target_medio > 0 else 0.0

    # Ponderación Cuantitativa de Riesgo Integral
    score_final_ia = (score_narrativa * 0.20) + ((score_puntos / 100) * 0.55) + (desviacion_target * 0.25)
    score_final_ia = max(min(score_final_ia, 1.0), -1.0)
    
    porcentaje_confianza = abs(score_final_ia) * 100
    
    if score_final_ia > 0.12:
        return "⚡ ALCISTA ESTRUCTURAL (Alta Convicción)", "#22c55e", porcentaje_confianza, score_final_ia
    elif score_final_ia < -0.12:
        return "🚨 RIESGO BAJISTA SEVERO (Alerta Institucional)", "#ef4444", porcentaje_confianza, score_final_ia
    else:
        return "⚖️ DISTRIBUCIÓN LATERAL (Sin Ventaja Estadística)", "#94a3b8", porcentaje_confianza, score_final_ia

# =========================================================================
# INTERFAZ PRINCIPAL DE LA TERMINAL DE INVERSIÓN
# =========================================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/radar.png", width=55)
    st.markdown("<h2 style='margin-top:0;'>Radar Intersector</h2>", unsafe_allow_html=True)
    st.markdown("---")
    seccion = st.sidebar.radio(
        "Módulos Cuantitativos:",
        ["🏛️ Terminal Institucional", "🎯 Pronósticos de Wall Street", "🏢 Análisis de Balance", "📊 Gráfico de Precios", "💼 Transacciones SEC"]
    )
    st.markdown("---")
    
    st.markdown("### 🤖 Cribado Automático por IA")
    with st.spinner("Escaneando el mercado..."):
        df_screening = escanear_mercado_por_ia()
        if not df_screening.empty: st.dataframe(df_screening, hide_index=True)
        else: st.caption("Consolidando métricas...")

st.markdown("<h1 class='main-title'>🏛️ Terminal Institutional Alpha</h1>", unsafe_allow_html=True)
ticker = st.text_input("🔍 Ingrese el Ticker de la Acción (Ej: NVDA, AAPL, AMZN, LLY, TSLA):", "NVDA").upper()

if ticker:
    try:
        empresa = yf.Ticker(ticker)
        info = empresa.info
        noticias_raw = empresa.news
        insiders_raw = empresa.insider_transactions
        
        precio_actual = float(info.get('currentPrice', info.get('regularMarketPrice', 0.0)))
        precio_previo = float(info.get('previousClose', 1.0))
        cambio_precio = precio_actual - precio_previo
        porcentaje_cambio = (cambio_precio / precio_previo) * 100
        volumen_hoy = info.get('regularMarketVolume', 1)
        moneda = info.get('currency', 'USD')

        # KPI Panel Superior
        st.markdown(f"### {info.get('longName', ticker)} <span style='color:#64748b; font-size:0.8em;'>| {info.get('sector', 'N/A')}</span>", unsafe_allow_html=True)
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1: st.metric(label="Último Precio", value=f"${precio_actual:,.2f} {moneda}", delta=f"${cambio_precio:,.2f}")
        with col_m2: st.metric(label="Retorno Diario", value=f"{porcentaje_cambio:,.2f}%", delta=f"{porcentaje_cambio:,.2f}%")
        with col_m3: st.metric(label="Volumen Negociado", value=f"{volumen_hoy:,}")
        st.markdown("---")

        target_alto = float(info.get('targetHighPrice', precio_actual * 1.15))
        target_medio = float(info.get('targetMedianPrice', precio_actual * 1.05))
        target_bajo = float(info.get('targetLowPrice', precio_actual * 0.90))

        # Ejecución del núcleo algorítmico cruzado
        lista_catalizadores, puntos_totales_score = analizar_catalizadores_y_riesgos(info, insiders_raw)
        diag_ia, color_ia, confianza_ia, raw_score = motor_imparcial_ia(noticias_raw, puntos_totales_score, precio_actual, target_medio)

        # =========================================================================
        # MÓDULO 1: DIAGNÓSTICO INSTITUCIONAL CRUDO Y REALISTA
        # =========================================================================
        if seccion == "🏛️ Terminal Institucional":
            st.subheader("🤖 Diagnóstico Estadístico e Imparcial de la IA")
            st.write("Análisis directo sin filtros optimistas. Combina el comportamiento de los fundamentales corporativos y la presión de los flujos.")
            
            # Caja predictiva principal
            st.markdown(f"""
            <div class="prediction-box" style="background: linear-gradient(135deg, #0f172a 0%, #020617 100%); border: 2px solid {color_ia};">
                <h2 style="margin:0; font-size:1.8em; color:#f8fafc;">Veredicto del Algoritmo: <span style="color:{color_ia};">{diag_ia}</span></h2>
                <p style="margin:10px 0 0 0; color:#94a3b8; font-size:1.1em;">Convicción Cuantitativa Neta: <b>{confianza_ia:.1f}%</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            # NUEVO PANEL CRÍTICO: ASIMETRÍA DE RIESGO Y DRAWDOWN ESTIMADO
            st.subheader("🛡️ Gestión de Riesgo y Margen de Seguridad")
            col_r1, col_r2 = st.columns(2)
            
            with col_r1:
                # Margen de seguridad respecto al consenso medio de analistas
                margen_seguridad = ((target_medio - precio_actual) / target_medio) * 100
                color_margen = "#22c55e" if margen_seguridad > 0 else "#ef4444"
                st.markdown(f"""
                <div class="scenario-card">
                    <h4 style="margin:0; color:#94a3b8;">📐 Margen de Seguridad Teórico</h4>
                    <h2 style="margin:10px 0; color:{color_margen};">{margen_seguridad:+.2f}%</h2>
                    <p style="font-size:0.85em; color:#cbd5e1;">Distancia matemática porcentual frente al valor de consenso de Wall Street. Un porcentaje positivo indica potencial subvaluación.</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col_r2:
                # Estimación implícita de Drawdown adverso en base a fundamentales débiles y volatilidad básica
                drawdown_estimado = max(5.0, 15.0 - (raw_score * 20))
                st.markdown(f"""
                <div class="scenario-card">
                    <h4 style="margin:0; color:#94a3b8;">📉 Riesgo Estimado de Caída (Max Drawdown Est.)</h4>
                    <h2 style="margin:10px 0; color:#ef4444;">-{drawdown_estimado:.1f}%</h2>
                    <p style="font-size:0.85em; color:#cbd5e1;">Pérdida máxima estimada de capital bajo condiciones normales si se activan los catalizadores bajistas identificados por el modelo.</p>
                </div>
                """, unsafe_allow_html=True)

            # Despliegue Crudo de Eventos / Catalizadores
            st.markdown("---")
            st.subheader("🔥 Escáner Crudo de Catalizadores y Eventos Activos")
            if lista_catalizadores:
                for cat in lista_catalizadores:
                    color_b = "#ef4444" if cat['tipo'] == "BEAR" else "#22c55e"
                    badge_texto = "ALERTA BAJISTA" if cat['tipo'] == "BEAR" else "CATALIZADOR ALCISTA"
                    st.markdown(f"""
                    <div style="background-color:#1e293b; padding:18px; border-radius:10px; margin-bottom:15px; border-left:6px solid {color_b};">
                        <span class="catalyst-badge" style="background-color:{color_b}22; color:{color_b}; border: 1px solid {color_b};">{badge_texto} | {cat['impacto']}</span>
                        <h4 style="margin:5px 0; color:#f8fafc;">{cat['evento']}</h4>
                        <p style="margin:5px 0 0 0; font-size:0.9em; color:#cbd5e1;">{cat['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No se registran distorsiones operativas críticas o anomalías en la estructura del balance actual.")

        # =========================================================================
        # MÓDULO 2: PRONÓSTICOS DE WALL STREET
        # =========================================================================
        elif seccion == "🎯 Pronósticos de Wall Street":
            st.subheader("🎯 Consenso del Rango de Precios Objetivo (Target Prices)")
            upside_medio = ((target_medio - precio_actual) / precio_actual) * 100
            
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                st.markdown(f'<div class="scenario-card" style="border-top: 4px solid #ef4444;"><h3 style="color:#ef4444; margin:0;">📉 Objetivo Mínimo</h3><h2 style="margin:10px 0; font-size:2.2em;">${target_bajo:,.2f}</h2><p style="font-size:0.85em; color:#cbd5e1;">Límite inferior proyectado por analistas si el ciclo corporativo entra en contracción estructural.</p></div>', unsafe_allow_html=True)
            with col_f2:
                st.markdown(f'<div class="scenario-card" style="border-top: 4px solid #38bdf8;"><h3 style="color:#38bdf8; margin:0;">⚖️ Objetivo Medio</h3><h2 style="margin:10px 0; font-size:2.2em;">${target_medio:,.2f}</h2><p style="font-size:0.85em; color:#cbd5e1;">Consenso general de la industria. Ofrece una perspectiva de retorno implícito del <b>{upside_medio:+.2f}%</b>.</p></div>', unsafe_allow_html=True)
            with col_f3:
                st.markdown(f'<div class="scenario-card" style="border-top: 4px solid #22c55e;"><h3 style="color:#22c55e; margin:0;">📈 Objetivo Máximo</h3><h2 style="margin:10px 0; font-size:2.2em;">${target_alto:,.2f}</h2><p style="font-size:0.85em; color:#cbd5e1;">Límite superior estimado asumiendo un escenario operativo de perfecta ejecución e ingresos récord.</p></div>', unsafe_allow_html=True)

        # =========================================================================
        # MÓDULO 3: ANÁLISIS DE BALANCE
        # =========================================================================
        elif seccion == "🏢 Análisis de Balance":
            st.subheader("🏢 Estructura de Capital y Eficiencia")
            col_p1, col_p2 = st.columns([1, 2])
            with col_p1:
                st.metric("Capitalización bursátil", f"${info.get('marketCap', 0):,}")
                st.metric("Rentabilidad s/ Capital (ROE)", f"{info.get('returnOnEquity', 0.0)*100:.2f}%")
                st.metric("Crecimiento de Ventas YoY", f"{info.get('revenueGrowth', 0.0)*100:.2f}%")
            with col_p2:
                st.markdown("**Resumen de Negocio:**")
                st.info(info.get('longBusinessSummary', 'No disponible.'))

        # =========================================================================
        # MÓDULOS TRADICIONALES PRESERVADOS
        # =========================================================================
        elif seccion == "📊 Gráfico de Precios":
            st.subheader("📈 Serie Temporal de Cierre")
            historial = empresa.history(period="3mo", interval="1d")
            if not historial.empty: st.line_chart(historial['Close'], use_container_width=True)

        elif seccion == "💼 Transacciones SEC":
            st.subheader("📅 Registro de Transacciones Formulario 4 SEC")
            if insiders_raw is not None and not insiders_raw.empty:
                st.dataframe(insiders_raw.head(20), use_container_width=True)
            else:
                st.warning("No hay transacciones internas registradas recientemente para este activo.")

    except Exception as e:
        st.error(f"Error crítico en el procesamiento del activo: {e}")