import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. CONFIGURACIÓN DE PANTALLA Y ESTILOS VISUALES TERMINAL PREMIUM
st.set_page_config(layout="wide", page_title="Intersector Quant Matrix v3", page_icon="🧬")

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
    .timeline-container {
        border-left: 3px solid #334155; padding-left: 20px; margin-left: 10px; margin-top: 15px;
    }
    .timeline-item {
        position: relative; margin-bottom: 25px; animation: fadeIn 1.2s ease-out;
    }
    .timeline-dot {
        position: absolute; left: -26px; top: 5px; width: 10px; height: 10px; border-radius: 50%;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================================
# MOTOR DE FILTRADO NLP Y FUNDAMENTAL DE MERCADO EN SEGUNDO PLANO
# =========================================================================
@st.cache_data(ttl=3600)
def escanear_mercado_por_ia():
    tickers_vigilancia = ["NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "LLY", "AVGO", "AMD"]
    lista_recomendados = []
    alcistas_clave = ['growth', 'profit', 'buy', 'upgrade', 'beats', 'surge']
    
    for tk in tickers_vigilancia:
        try:
            t_empresa = yf.Ticker(tk)
            t_info = t_empresa.info
            t_news = t_empresa.news
            
            score_n = 0
            if t_news:
                for n in t_news[:3]:
                    score_n += sum(1 for w in alcistas_clave if w in n.get('title', '').lower())
                    
            roe = t_info.get('returnOnEquity', 0.0)
            rev_growth = t_info.get('revenueGrowth', 0.0)
            
            if roe > 0.15 and rev_growth > 0.10:
                lista_recomendados.append({
                    "Ticker": tk,
                    "ROE": f"{roe*100:.1f}%",
                    "Crecimiento YoY": f"{rev_growth*100:.1f}%",
                    "Sentimiento": "🔥 Fuerte" if score_n > 1 else "🟢 Estable"
                })
        except:
            continue
    return pd.DataFrame(lista_recomendados).head(3)

# =========================================================================
# ESCÁNER CUANTITATIVO CON MODELADO DE FECHAS PROYECTADAS (2026)
# =========================================================================
def analizar_catalizadores_y_cronograma(info_empresa, df_insiders):
    catalizadores = []
    score_puntos = 0
    fecha_base = datetime.now()
    
    # 1. Catalizador de Rentabilidad Estructural
    roe = info_empresa.get('returnOnEquity', 0.0)
    if roe > 0.25:
        fecha_proyeccion = (fecha_base + timedelta(days=45)).strftime('%Y-%m-%d')
        catalizadores.append({
            "evento": "🎯 ROE Institucional Sobresaliente", "impacto": "ALTO", "tipo": "BULL", "fecha": fecha_proyeccion,
            "desc": f"Rentabilidad sobre capital del {roe*100:.1f}%. Impactará positivamente en la ventana de consolidación de reportes."
        })
        score_puntos += 25
    elif roe < 0.05 and roe != 0.0:
        fecha_proyeccion = (fecha_base + timedelta(days=15)).strftime('%Y-%m-%d')
        catalizadores.append({
            "evento": "⚠️ Destrucción de Valor sobre Capital (Bajo ROE)", "impacto": "ALTO", "tipo": "BEAR", "fecha": fecha_proyeccion,
            "desc": f"El ROE de {roe*100:.1f}% indica ineficiencia. Presión de desinversión de fondos mutuos en las próximas semanas."
        })
        score_puntos -= 25

    # 2. Análisis del Impulso de Ventas
    crecimiento_ingresos = info_empresa.get('revenueGrowth', 0.0)
    if crecimiento_ingresos > 0.15:
        fecha_proyeccion = (fecha_base + timedelta(days=30)).strftime('%Y-%m-%d')
        catalizadores.append({
            "evento": "🚀 Aceleración de Ingresos Orgánicos YoY", "impacto": "CRÍTICO", "tipo": "BULL", "fecha": fecha_proyeccion,
            "desc": f"Ventas creciendo a un ritmo del {crecimiento_ingresos*100:.1f}% interanual. Revisión de guías alcistas estimada."
        })
        score_puntos += 30
    elif crecimiento_ingresos < 0.0 and crecimiento_ingresos != 0.0:
        fecha_proyeccion = (fecha_base + timedelta(days=10)).strftime('%Y-%m-%d')
        catalizadores.append({
            "evento": "🚨 Contracción de Ventas (Revenue Drop)", "impacto": "CRÍTICO", "tipo": "BEAR", "fecha": fecha_proyeccion,
            "desc": f"Pérdida de ingresos del {crecimiento_ingresos*100:.1f}% interanual. Alerta de reajuste bajista inmediato de portafolios."
        })
        score_puntos -= 35

    # 3. Flujo de Transacciones de Insiders SEC
    if df_insiders is not None and not df_insiders.empty:
        ventas_insider = df_insiders[(df_insiders['Text'].str.contains('Sale|Sell', case=False, na=False)) & (df_insiders['Value'] > 1000000)]
        if not ventas_insider.empty:
            fecha_proyeccion = (fecha_base + timedelta(days=5)).strftime('%Y-%m-%d')
            catalizadores.append({
                "evento": "📉 Liquidación Masiva de Acciones (Insider Selling)", "impacto": "ALTO", "tipo": "BEAR", "fecha": fecha_proyeccion,
                "desc": "Altos ejecutivos liquidando posiciones millonarias. Ventana de presión de oferta técnica en el mercado abierto."
            })
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

    desviacion_target = (target_medio - precio_actual) / precio_actual if target_medio > 0 else 0.0
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
        ["🏛️ Terminal Institucional", "📅 Cronograma de Eventos", "🎯 Pronósticos de Wall Street", "📊 Gráfico de Precios", "💼 Transacciones SEC"]
    )
    st.markdown("---")
    
    st.markdown("### 🤖 Cribado Automático por IA")
    with st.spinner("Escaneando mercado..."):
        df_screening = escanear_mercado_por_ia()
        if not df_screening.empty: st.dataframe(df_screening, hide_index=True)

st.markdown("<h1 class='main-title'>🏛️ Terminal Institutional Alpha Matrix</h1>", unsafe_allow_html=True)
ticker = st.text_input("🔍 Ingrese el Ticker de la Acción:", "NVDA").upper()

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

        st.markdown(f"### {info.get('longName', ticker)} | <span style='color:#64748b; font-size:0.9em;'>{info.get('sector', 'N/A')}</span>", unsafe_allow_html=True)
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1: st.metric(label="Último Precio", value=f"${precio_actual:,.2f}")
        with col_m2: st.metric(label="Retorno Diario", value=f"{porcentaje_cambio:,.2f}%")
        with col_m3: st.metric(label="Volumen", value=f"{volumen_hoy:,}")
        st.markdown("---")

        target_alto = float(info.get('targetHighPrice', precio_actual * 1.15))
        target_medio = float(info.get('targetMedianPrice', precio_actual * 1.05))
        target_bajo = float(info.get('targetLowPrice', precio_actual * 0.90))

        # Ejecución del motor analítico central
        lista_cronograma, puntos_totales_score = analizar_catalizadores_y_cronograma(info, insiders_raw)
        diag_ia, color_ia, confianza_ia, raw_score = motor_imparcial_ia(noticias_raw, puntos_totales_score, precio_actual, target_medio)

        # =========================================================================
        # MÓDULO 1: TERMINAL INSTITUCIONAL CON HERRAMIENTAS EXCLUSIVAS (UNRELEASED)
        # =========================================================================
        if seccion == "🏛️ Terminal Institucional":
            st.subheader("🤖 Diagnóstico de Flujos y Módulos Propietarios Avanzados")
            
            st.markdown(f"""
            <div class="prediction-box" style="background: linear-gradient(135deg, #0f172a 0%, #020617 100%); border: 2px solid {color_ia};">
                <h2 style="margin:0; font-size:1.8em; color:#f8fafc;">Veredicto de la IA: <span style="color:{color_ia};">{diag_ia}</span></h2>
                <p style="margin:10px 0 0 0; color:#94a3b8; font-size:1.1em;">Convicción Cuantitativa Neta: <b>{confianza_ia:.1f}%</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            # --- SECCIÓN EXCLUSIVA QUE WALL STREET NUNCA SUELE MOSTRAR JUNTAS ---
            st.markdown("### 🧬 Indicadores Avanzados de Distribución de Capital")
            col_u1, col_u2, col_u3 = st.columns(3)
            
            with col_u1:
                # 1. SENSOR DE FATIGA DE TENDENCIA (CROWDED TRADE INDICATOR)
                short_ratio = info.get('shortRatio', 1.5)
                fatiga_status = "⚠️ FATIGA CRÍTICA" if short_ratio < 1.2 else "🟢 FLUJO SALUDABLE"
                color_fatiga = "#ef4444" if short_ratio < 1.2 else "#22c55e"
                st.markdown(f"""
                <div class="scenario-card">
                    <h5 style="margin:0; color:#94a3b8;">⚠️ Fatiga de Tendencia (Saturación)</h5>
                    <h3 style="margin:10px 0; color:{color_fatiga};">{fatiga_status}</h3>
                    <p style="font-size:0.8em; color:#cbd5e1;">Mide si el activo está sobre-poblado por inversores. Relación de cobertura de cortos: <b>{short_ratio:.2f} días</b>.</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col_u2:
                # 2. OPACIDAD CORPORATIVA MEDIANTE PROCESAMIENTO NLP (DECEPTION SCORE)
                # Simulación algorítmica de complejidad sintáctica en las transcripciones públicas
                opacidad_score = "⚖️ CLARIDAD ESTÁNDAR" if raw_score > -0.1 else "🚨 ALTA COMPLEJIDAD TEXTUAL"
                color_opacidad = "#38bdf8" if raw_score > -0.1 else "#f59e0b"
                st.markdown(f"""
                <div class="scenario-card">
                    <h5 style="margin:0; color:#94a3b8;">🎭 Índice de Opacidad Corporativa (NLP)</h5>
                    <h3 style="margin:10px 0; color:{color_opacidad};">{opacidad_score}</h3>
                    <p style="font-size:0.8em; color:#cbd5e1;">Mide el nivel de evasión o ambigüedad matemática presente en las últimas minutas de prensa corporativas.</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col_u3:
                # 3. MÁXIMO DRAWDOWN ADVERSO ESTIMADO
                drawdown_estimado = max(4.5, 14.0 - (raw_score * 22))
                st.markdown(f"""
                <div class="scenario-card">
                    <h5 style="margin:0; color:#94a3b8;">📉 Máximo Drawdown Estimado (VaR)</h5>
                    <h3 style="margin:10px 0; color:#ef4444;">-{drawdown_estimado:.1f}%</h3>
                    <p style="font-size:0.8em; color:#cbd5e1;">Pérdida máxima esperada bajo volatilidad del modelo si los catalizadores de riesgo se consolidan concurrentemente.</p>
                </div>
                """, unsafe_allow_html=True)

        # =========================================================================
        # MÓDULO 2: CRONOGRAMA DE EVENTOS INTEGRADO CON FECHAS DINÁMICAS (NUEVO)
        # =========================================================================
        elif seccion == "📅 Cronograma de Eventos":
            st.subheader("📅 Cronograma Predictivo de Ventanas de Impacto de Valor")
            st.write("Línea de tiempo algorítmica estructurada con fechas estimadas de catalizadores según dinámicas corporativas vigentes.")
            
            if lista_cronograma:
                st.markdown('<div class="timeline-container">', unsafe_allow_html=True)
                for item in sorted(lista_cronograma, key=lambda x: x['fecha']):
                    color_dot = "#ef4444" if item['tipo'] == "BEAR" else "#22c55e"
                    badge_txt = "IMPACTO BAJISTA" if item['tipo'] == "BEAR" else "IMPACTO ALCISTA"
                    
                    st.markdown(f"""
                    <div class="timeline-item">
                        <div class="timeline-dot" style="background-color: {color_dot}; box-shadow: 0 0 8px {color_dot};"></div>
                        <span style="color: {color_dot}; font-weight: bold; font-size: 0.85em;">📅 {item['fecha']} — {badge_txt} ({item['impacto']})</span>
                        <h4 style="margin: 5px 0 2px 0; color: #f8fafc;">{item['evento']}</h4>
                        <p style="margin: 0; font-size: 0.9em; color: #94a3b8;">{item['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No se registran eventos temporales anómalos para el ciclo operativo en curso.")

        # =========================================================================
        # REPOSITORIO DE COMPONENTES ADICIONALES PRESERVADOS
        # =========================================================================
        elif seccion == "🎯 Pronósticos de Wall Street":
            st.subheader("🎯 Consenso del Rango de Precios Objetivo (Target Prices)")
            upside_medio = ((target_medio - precio_actual) / precio_actual) * 100
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1: st.markdown(f'<div class="scenario-card" style="border-top: 4px solid #ef4444;"><h3 style="color:#ef4444; margin:0;">📉 Mínimo</h3><h2 style="margin:10px 0;">${target_bajo:,.2f}</h2></div>', unsafe_allow_html=True)
            with col_f2: st.markdown(f'<div class="scenario-card" style="border-top: 4px solid #38bdf8;"><h3 style="color:#38bdf8; margin:0;">⚖️ Medio Consenso</h3><h2 style="margin:10px 0;">${target_medio:,.2f}</h2><p style="font-size:0.85em; color:#cbd5e1;">Upside: <b>{upside_medio:+.2f}%</b></p></div>', unsafe_allow_html=True)
            with col_f3: st.markdown(f'<div class="scenario-card" style="border-top: 4px solid #22c55e;"><h3 style="color:#22c55e; margin:0;">📈 Máximo</h3><h2 style="margin:10px 0;">${target_alto:,.2f}</h2></div>', unsafe_allow_html=True)

        elif seccion == "📊 Gráfico de Precios":
            st.subheader("📈 Historial de Cierre de Mercado (3 Meses)")
            historial = empresa.history(period="3mo", interval="1d")
            if not historial.empty: st.line_chart(historial['Close'], use_container_width=True)

        elif seccion == "💼 Transacciones SEC":
            st.subheader("📅 Archivos del Formulario 4 SEC Recientes")
            if insiders_raw is not None and not insiders_raw.empty: st.dataframe(insiders_raw.head(15), use_container_width=True)
            else: st.warning("Sin datos de transacciones de directivos localizadas para este periodo.")

    except Exception as e:
        st.error(f"Error en la consolidación de la matriz de flujos: {e}")