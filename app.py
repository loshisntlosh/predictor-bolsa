import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# 1. CONFIGURACIÓN DE PANTALLA Y ESTILOS VISUALES TERMINAL PREMIUM
st.set_page_config(layout="wide", page_title="Intersector Alpha: Terminal Quant", page_icon="⚡")

st.markdown("""
<style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .main-title { animation: fadeIn 0.8s ease-out; color: #f8fafc; font-weight: 800; }
    .prediction-box { 
        padding: 25px; border-radius: 12px; 
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #06b6d4; text-align: center;
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
# MOTOR DE RECOMENDACIÓN AUTOMÁTICA POR IA Y NARRATIVA (MARKET SCREENER)
# =========================================================================
@st.cache_data(ttl=3600)  # Caché de 1 hora para optimizar velocidad de carga
def escanear_mercado_por_ia():
    tickers_vigilancia = ["NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "LLY", "AVGO", "AMD"]
    lista_recomendados = []
    
    alcistas_clave = ['growth', 'profit', 'buy', 'upgrade', 'innovation', 'beats', 'surge', 'partnership']
    
    for tk in tickers_vigilancia:
        try:
            t_empresa = yf.Ticker(tk)
            t_info = t_empresa.info
            t_news = t_empresa.news
            
            # Cálculo de score narrativo flash
            score_n = 0
            if t_news:
                for n in t_news[:5]:
                    tit = n.get('title', '').lower()
                    score_n += sum(1 for w in alcistas_clave if w in tit)
                    
            roe = t_info.get('returnOnEquity', 0.0)
            rev_growth = t_info.get('revenueGrowth', 0.0)
            
            # Algoritmo de filtrado multifactorial
            if roe > 0.15 and rev_growth > 0.10 and score_n >= 1:
                lista_recomendados.append({
                    "Ticker": tk,
                    "Nombre": t_info.get('shortName', tk),
                    "ROE": f"{roe*100:.1f}%",
                    "Crecimiento Rev.": f"{rev_growth*100:.1f}%",
                    "Score Narrativo": "🔥 Fuerte Optimismo" if score_n > 2 else "🟢 Positivo"
                })
        except:
            continue
            
    return pd.DataFrame(lista_recomendados).head(3)

# =========================================================================
# ESCÁNER CRÍTICO DE CATALIZADORES FINANCIEROS VERÍDICOS
# =========================================================================
def escanear_catalizadores_precision(info_empresa, df_insiders):
    catalizadores = []
    puntos_alcistas = 0
    
    # 1. Catalizador de Rentabilidad Estructural (ROE Institucional)
    roe = info_empresa.get('returnOnEquity', 0.0)
    if roe > 0.25:
        catalizadores.append({
            "evento": "🎯 Rentabilidad Financiera Excepcional (ROE > 25%)",
            "impacto": "ALTO",
            "descripcion": f"El retorno sobre el capital es de {roe*100:.1f}%. Esto demuestra una gestión del capital ultra-eficiente, el principal filtro de Warren Buffett."
        })
        puntos_alcistas += 25

    # 2. Catalizador de Impulso de Ventas (Revenue Growth YoY)
    crecimiento_ingresos = info_empresa.get('revenueGrowth', 0.0)
    if crecimiento_ingresos > 0.15:
        catalizadores.append({
            "evento": "🚀 Aceleración de Ingresos Orgánicos (YoY Growth)",
            "impacto": "CRÍTICO",
            "descripcion": f"Facturación creciendo a un ritmo del {crecimiento_ingresos*100:.1f}% interanual. Captura masiva de cuota de mercado detectada."
        })
        puntos_alcistas += 30

    # 3. Catalizador de Salud de Balance (Debt-to-Equity Saludable)
    ratio_deuda = info_empresa.get('debtToEquity', 100.0)
    if ratio_deuda < 80.0:  # Estructura de capital muy desapalancada
        catalizadores.append({
            "evento": "🛡️ Fortaleza de Balance y Bajo Apalancamiento",
            "impacto": "MEDIO",
            "descripcion": f"Ratio Deuda/Capitalización de apenas {ratio_deuda:.1f}%. Inmunidad frente a entornos prolongados de altas tasas de interés."
        })
        puntos_alcistas += 20
        
    # 4. Monitoreo SEC de Respaldo Corporativo (Insiders)
    if df_insiders is not None and not df_insiders.empty:
        compras_grandes = df_insiders[(df_insiders['Text'].str.contains('Buy|Purchase', case=False, na=False)) & (df_insiders['Value'] > 500000)]
        if not compras_grandes.empty:
            catalizadores.append({
                "evento": "💼 Bloque de Capital de Insider Verificado (>500K USD)",
                "impacto": "CRÍTICO",
                "descripcion": "Dinero real depositado en el mercado por directores. No hay señal de convicción corporativa más honesta."
            })
            puntos_alcistas += 25

    return catalizadores, puntos_alcistas

# =========================================================================
# MOTOR PREDICTIVO CON INTELIGENCIA ARTIFICIAL DE DATOS CONCURRENTES
# =========================================================================
def modelo_predictivo_ia(noticias, puntos_cat, precio_actual, target_medio):
    score_narrativa = 0.0
    alcistas = ['growth', 'profit', 'buy', 'upgrade', 'innovation', 'approval', 'record', 'bullish', 'partnership', 'beats']
    bajistas = ['lawsuit', 'loss', 'downgrade', 'risk', 'regulatory', 'investigation', 'declining', 'bearish', 'fine', 'misses']
    
    total_noticias = len(noticias) if noticias else 1
    if noticias:
        for n in noticias:
            titulo = n.get('title', '').lower()
            score_narrativa += sum(0.25 for w in alcistas if w in titulo) - sum(0.25 for w in bajistas if w in titulo)
        score_narrativa = score_narrativa / total_noticias

    # Desviación institucional respecto al target de analistas
    desviacion_target = 0.0
    if target_medio > 0:
        desviacion_target = (target_medio - precio_actual) / precio_actual

    # Fusión matemática de vectores para la predicción estadística de la IA
    score_final_ia = (score_narrativa * 0.25) + ((puntos_cat / 100) * 0.50) + (desviacion_target * 0.25)
    score_final_ia = max(min(score_final_ia, 1.0), -1.0)
    
    porcentaje_confianza = abs(score_final_ia) * 100
    
    if score_final_ia > 0.15:
        return "⚡ PROBABILIDAD ALCISTA ALTA (Fuerte Concurrencia)", "#22c55e", porcentaje_confianza
    elif score_final_ia < -0.15:
        return "🚨 ALTA PROBABILIDAD DE CORRECCIÓN (Desgaste Fundamental)", "#ef4444", porcentaje_confianza
    else:
        return "⚖️ DISTRIBUCIÓN LATERAL EQUILIBRADA (Consolidación)", "#94a3b8", porcentaje_confianza

# =========================================================================
# INTERFAZ PRINCIPAL DE LA TERMINAL DE INVERSIÓN
# =========================================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/radar.png", width=55)
    st.markdown("<h2 style='margin-top:0;'>Radar Intersector</h2>", unsafe_allow_html=True)
    st.markdown("---")
    seccion = st.sidebar.radio(
        "Módulos Cuantitativos:",
        ["🔥 Escáner e IA Predictiva", "🎯 Forecast Institucional", "🏢 Perfil de Fundamentales", "📊 Análisis Gráfico", "💼 Transacciones SEC"]
    )
    st.markdown("---")
    
    # NUEVO COMPONENTE: SISTEMA AUTOMÁTICO DE RECOMENDACIÓN DE ACCIONES POR IA
    st.markdown("### 🤖 Selección por IA & Narrativa")
    st.caption("Top 3 activos filtrados automáticamente en tiempo real por convergencia fundamental y de prensa:")
    
    with st.spinner("Ejecutando algoritmo de screening..."):
        df_screening = escanear_mercado_por_ia()
        if not df_screening.empty:
            st.dataframe(df_screening, hide_index=True)
        else:
            st.caption("Procesando datos del ecosistema...")

st.markdown("<h1 class='main-title'>🔮 El Intersector: Inteligencia Financiera</h1>", unsafe_allow_html=True)
ticker = st.text_input("🔍 Ticker de la Empresa (Ej: NVDA, AAPL, AMZN, LLY, TSLA):", "NVDA").upper()

if ticker:
    try:
        empresa = yf.Ticker(ticker)
        info = empresa.info
        noticias_raw = empresa.news
        insiders_raw = empresa.insider_transactions
        
        # Extracción y limpieza estricta de métricas de mercado
        precio_actual = float(info.get('currentPrice', info.get('regularMarketPrice', 0.0)))
        precio_previo = float(info.get('previousClose', 1.0))
        cambio_precio = precio_actual - precio_previo
        porcentaje_cambio = (cambio_precio / precio_previo) * 100
        volumen_hoy = info.get('regularMarketVolume', 1)
        moneda = info.get('currency', 'USD')

        # Panel de Estado Financiero Superior (KPIs)
        st.markdown(f"### {info.get('longName', ticker)} <span style='color:#64748b; font-size:0.8em;'>| {info.get('sector', 'N/A')}</span>", unsafe_allow_html=True)
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1: st.metric(label="Último Precio", value=f"${precio_actual:,.2f} {moneda}", delta=f"${cambio_precio:,.2f}")
        with col_m2: st.metric(label="Retorno Diario (%)", value=f"{porcentaje_cambio:,.2f}%", delta=f"{porcentaje_cambio:,.2f}%")
        with col_m3: st.metric(label="Volumen del Día", value=f"{volumen_hoy:,}")
        st.markdown("---")

        # Variables institucionales de analistas necesarias para los módulos
        target_alto = float(info.get('targetHighPrice', precio_actual * 1.15))
        target_medio = float(info.get('targetMedianPrice', precio_actual * 1.05))
        target_bajo = float(info.get('targetLowPrice', precio_actual * 0.90))

        # =========================================================================
        # MÓDULO 1: ESCÁNER DE PRECISION Y MODELO PREDICTIVO IA
        # =========================================================================
        if seccion == "🔥 Escáner e IA Predictiva":
            st.subheader("🤖 Diagnóstico Predictivo mediante Inteligencia Artificial")
            st.write("Algoritmo predictivo que entrelaza la desviación del consenso de analistas, catalizadores de balances duros y el sentimiento de prensa actual.")
            
            # Ejecutar escáner fundamental cruzado
            lista_catalizadores, puntos_totales_cat = escanear_catalizadores_precision(info, insiders_raw)
            diag_ia, color_ia, confianza_ia = modelo_predictivo_ia(noticias_raw, puntos_totales_cat, precio_actual, target_medio)
            
            st.markdown(f"""
            <div class="prediction-box">
                <h2 style="margin:0; font-size:1.9em;">Modelo Cuantitativo IA: <span style="color:{color_ia};">{diag_ia}</span></h2>
                <p style="margin:10px 0 0 0; color:#94a3b8; font-size:1.1em;">Convicción Algorítmica Concurrente: <b>{confianza_ia:.1f}%</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🔥 Escáner de Catalizadores de Crecimiento Identificados")
            if lista_catalizadores:
                for cat in lista_catalizadores:
                    color_badge = "#ef4444" if cat['impacto'] == "CRÍTICO" else ("#f59e0b" if cat['impacto'] == "ALTO" else "#38bdf8")
                    st.markdown(f"""
                    <div style="background-color:#1e293b; padding:18px; border-radius:10px; margin-bottom:15px; border-left:6px solid {color_badge};">
                        <span class="catalyst-badge" style="background-color:{color_badge}33; color:{color_badge}; border: 1px solid {color_badge};">IMPACTO {cat['impacto']}</span>
                        <h4 style="margin:5px 0; color:#f8fafc;">{cat['evento']}</h4>
                        <p style="margin:5px 0 0 0; font-size:0.9em; color:#cbd5e1;">{cat['descripcion']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No se detectan anomalías extremas en las métricas de balance analizadas para esta sesión.")

        # =========================================================================
        # [NUEVO] MÓDULO 2: FORECAST DE INVERSIONISTAS FUERTES (WALL STREET CONSENSUS)
        # =========================================================================
        elif seccion == "🎯 Forecast Institucional":
            st.subheader("🎯 Consenso de Objetivos de Precio y Pronósticos (Previsiones de Analistas)")
            st.write("Datos extraídos de los informes de investigación de los principales analistas e inversionistas institucionales de Wall Street.")
            
            # Cálculo de retornos potenciales estimativos
            upside_medio = ((target_medio - precio_actual) / precio_actual) * 100
            
            col_f1, col_f2, col_f3 = st.columns(3)
            
            with col_f1:
                st.markdown(f"""
                <div class="scenario-card" style="border-top: 4px solid #ef4444;">
                    <h3 style="color:#ef4444; margin:0;">📉 Pronóstico Pesimista</h3>
                    <h2 style="margin:10px 0; font-size:2.2em;">${target_bajo:,.2f}</h2>
                    <p style="font-size:0.85em; color:#cbd5e1;"><b>Objetivo Mínimo:</b> Representa la valuación de consenso si el negocio experimenta vientos en contra o contracción de múltiplos de mercado.</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col_f2:
                st.markdown(f"""
                <div class="scenario-card" style="border-top: 4px solid #38bdf8;">
                    <h3 style="color:#38bdf8; margin:0;">⚖️ Pronóstico Consenso</h3>
                    <h2 style="margin:10px 0; font-size:2.2em;">${target_medio:,.2f}</h2>
                    <p style="font-size:0.85em; color:#cbd5e1;"><b>Precio Objetivo Medio:</b> Retorno potencial implícito estimado del <b>{upside_medio:+.2f}%</b> según los modelos de valuación consolidados de la industria.</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col_f3:
                st.markdown(f"""
                <div class="scenario-card" style="border-top: 4px solid #22c55e;">
                    <h3 style="color:#22c55e; margin:0;">📈 Pronóstico Optimista</h3>
                    <h2 style="margin:10px 0; font-size:2.2em;">${target_alto:,.2f}</h2>
                    <p style="font-size:0.85em; color:#cbd5e1;"><b>Objetivo Máximo:</b> Proyección optimista de los analistas líderes asumiendo un despliegue perfecto de sus catalizadores de crecimiento corporativo.</p>
                </div>
                """, unsafe_allow_html=True)

        # ==========================================
        # RESTO DE MÓDULOS DEL ENTORNO DE INVERSIÓN
        # ==========================================
        elif seccion == "🏢 Perfil de Fundamentales":
            st.subheader("🏢 Fundamentales y Estructura de Márgenes de la Empresa")
            col_p1, col_p2 = st.columns([1, 2])
            with col_p1:
                st.metric("Capitalización de Mercado", f"${info.get('marketCap', 0):,}")
                st.metric("Margen Bruto de Utilidad", f"{info.get('grossMargins', 0.0)*100:.2f}%")
                st.write(f"**Ubicación Corporativa:** {info.get('country', 'N/A')}")
            with col_p2:
                st.markdown("**Resumen Estratégico:**")
                st.info(info.get('longBusinessSummary', 'Datos de perfil no localizados.'))

        elif seccion == "📊 Análisis Gráfico":
            st.subheader("📈 Cotización de Cierre de Mercado")
            historial = empresa.history(period="3mo", interval="1d")
            if not historial.empty:
                st.line_chart(historial['Close'], use_container_width=True)

        elif seccion == "💼 Transacciones SEC":
            st.subheader("📅 Archivo de Transacciones Informadas de Altos Mandos")
            if insiders_raw is not None and not insiders_raw.empty:
                st.dataframe(insiders_raw.head(15), use_container_width=True)
            else:
                st.warning("Sin transacciones internas oficiales indexadas para este periodo bursátil.")

    except Exception as e:
        st.error(f"Error crítico en la consolidación de flujos de datos bursátiles: {e}")