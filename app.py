import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN DE PANTALLA Y ESTILOS VISUALES PREMIUM
st.set_page_config(layout="wide", page_title="El Intersector Pro: Inteligencia de Mercados", page_icon="🔮")

st.markdown("""
<style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .main-title { animation: fadeIn 0.8s ease-out; color: #f8fafc; font-weight: 800; }
    .prediction-box { 
        padding: 25px; 
        border-radius: 12px; 
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #06b6d4; 
        text-align: center;
        animation: fadeIn 1s ease-out;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        margin-bottom: 25px;
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
# NUEVO MOTOR PREDICTIVO AVANZADO (PRO QUANT ALGORITHM)
# =========================================================================
def algoritmo_predictivo_institucional(noticias, df_insiders, volumen_mercado):
    score_narrativa = 0.0
    score_insider = 0.0
    
    # 1. Matriz de Impacto Semántico Financiero/Político
    alcistas = ['growth', 'profit', 'buy', 'upgrade', 'innovation', 'approval', 'record', 'bullish', 'expansion', 'partnership', 'beats', 'surge']
    bajistas = ['lawsuit', 'loss', 'downgrade', 'risk', 'regulatory', 'investigation', 'declining', 'bearish', 'fine', 'deficit', 'misses', 'drop']
    
    total_noticias = len(noticias) if noticias else 1
    if noticias:
        for n in noticias:
            titulo = n.get('title', '').lower()
            menciones_pos = sum(1 for word in alcistas if word in titulo)
            menciones_neg = sum(1 for word in bajistas if word in titulo)
            score_narrativa += (menciones_pos * 0.2) - (menciones_neg * 0.2)
        # Normalizamos la narrativa según el volumen de prensa analizado
        score_narrativa = score_narrativa / total_noticias

    # 2. Análisis del Tamaño del Bloque de Capital (Insider Volume Weighted)
    if df_insiders is not None and not df_insiders.empty:
        for _, row in df_insiders.head(10).iterrows():
            texto_accion = str(row.get('Text', '')).lower()
            valor_transaccion = float(row.get('Value', 0))
            acciones_operadas = float(row.get('Shares', 0))
            
            # Clasificación por tamaño del capital puesto en riesgo por el directivo
            peso_capital = 0.1
            if valor_transaccion > 1000000: peso_capital = 0.4  # Transacción institucional masiva (>1M USD)
            elif valor_transaccion > 250000: peso_capital = 0.25 # Compra relevante (>250k USD)
            
            if 'buy' in texto_accion or 'purchase' in texto_accion:
                # Si compran y el volumen es alto respecto al promedio diario, es una fuerte anomalía
                impacto_volumen = (acciones_operadas / volumen_mercado) * 10
                score_insider += peso_capital + min(impacto_volumen, 0.2)
            elif 'sale' in texto_accion or 'sell' in texto_accion:
                score_insider -= (peso_capital * 0.3) # Penalización menor por venta de liquidez

    # 3. Consolidación de la Matriz Predictiva
    score_total = (score_narrativa * 0.4) + (score_insider * 0.6)
    score_total = max(min(score_total, 1.0), -1.0)
    
    porcentaje_fiabilidad = abs(score_total) * 100
    
    # Asignación de perfil según tolerancia al riesgo del inversionista
    if score_total > 0.20:
        perfil = "🟢 ALCISTA CONVERGENTE (Señal de Alta Convicción)"
        color = "#22c55e"
    elif score_total < -0.20:
        perfil = "🔴 DISTRIBUCIÓN / BAJISTA (Fuerte Presión de Venta Interna)"
        color = "#ef4444"
    else:
        perfil = "🟡 ACUMULACIÓN NEUTRA (Baja Convicción de Datos)"
        color = "#94a3b8"
        
    return perfil, color, porcentaje_fiabilidad, score_narrativa, score_insider

# =========================================================================
# INTERFAZ DE USUARIO Y CONFIGURACIÓN DEL NAVBAR
# =========================================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/radar.png", width=55)
    st.markdown("<h2 style='margin-top:0;'>Radar Intersector</h2>", unsafe_allow_html=True)
    st.markdown("---")
    seccion = st.sidebar.radio(
        "Módulos del Sistema:",
        ["🔮 Inteligencia Predictiva", "🏢 Perfil Corporativo", "📊 Análisis Técnico", "💼 Transacciones SEC", "📰 Flujo Informativo"]
    )
    st.markdown("---")
    st.caption("Filtros Profesionales Activos")

st.markdown("<h1 class='main-title'>🔮 El Intersector: Inteligencia Financiera</h1>", unsafe_allow_html=True)
ticker = st.text_input("🔍 Ingresa el Ticker de la Empresa (Ej: NVDA, AAPL, AMZN, LLY):", "NVDA").upper()

if ticker:
    try:
        # Descarga de estructuras de datos bursátiles
        empresa = yf.Ticker(ticker)
        info = empresa.info
        noticias_raw = empresa.news
        insiders_raw = empresa.insider_transactions
        
        # Variables numéricas clave en tiempo real
        precio_actual = float(info.get('currentPrice', info.get('regularMarketPrice', 0.0)))
        precio_previo = float(info.get('previousClose', 1.0))
        cambio_precio = precio_actual - precio_previo
        porcentaje_cambio = (cambio_precio / precio_previo) * 100
        volumen_hoy = info.get('regularMarketVolume', 1)
        moneda = info.get('currency', 'USD')

        # Panel de Estado Financiero Superior (KPIs de Mercado)
        st.markdown(f"### {info.get('longName', ticker)} <span style='color:#64748b; font-size:0.8em;'>| {info.get('sector', 'N/A')}</span>", unsafe_allow_html=True)
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric(label="Último Precio", value=f"${precio_actual:,.2f} {moneda}", delta=f"${cambio_precio:,.2f}")
        with col_m2:
            st.metric(label="Retorno Diario (%)", value=f"{porcentaje_cambio:,.2f}%", delta=f"{porcentaje_cambio:,.2f}%")
        with col_m3:
            st.metric(label="Volumen del Día", value=f"{volumen_hoy:,}")
            
        st.markdown("---")

        # ==========================================
        # MODULO 1: INTELIGENCIA PREDICTIVA AVANZADA
        # ==========================================
        if seccion == "🔮 Inteligencia Predictiva":
            st.subheader("🤖 Diagnóstico Cuantitativo del Algoritmo")
            st.write("Cálculo ponderado por volumen transaccional neto y análisis de sentimiento macroeconómico.")
            
            # Ejecución del nuevo motor algorítmico
            resultado, color_r, confianza, sub_narrativa, sub_insider = algoritmo_predictivo_institucional(noticias_raw, insiders_raw, volumen_hoy)
            
            st.markdown(f"""
            <div class="prediction-box">
                <h2 style="margin:0; font-size:1.9em;">Vector de Inversión: <span style="color:{color_r};">{resultado}</span></h2>
                <p style="margin:10px 0 0 0; color:#94a3b8; font-size:1.1em;">Convicción Matemática del Modelo: <b>{confianza:.1f}%</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Desglose de sub-métricas estructurales que exige un analista
            st.markdown("#### 📊 Desglose de Componentes del Modelo")
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.write(f"**Índice de Sentimiento de Prensa (40% peso):** `{sub_narrativa:+.2f}`")
                st.caption("Puntuación sobre el tono de las últimas 10 noticias políticas y del sector.")
            with col_d2:
                st.write(f"**Convicción de Flujo Corporativo (60% peso):** `{sub_insider:+.2f}`")
                st.caption("Mide el tamaño del capital monetario real que los directores ejecutivos están arriesgando.")

        # ==========================================
        # MODULO 2: PERFIL CORPORATIVO
        # ==========================================
        elif seccion == "🏢 Perfil Corporativo":
            st.subheader("🏢 Fundamentales Básicos de la Empresa")
            col_p1, col_p2 = st.columns([1, 2])
            with col_p1:
                st.metric("Capitalización bursátil", f"${info.get('marketCap', 0):,}")
                st.write(f"**Ubicación:** {info.get('country', 'N/A')}")
                st.write(f"**Sitio Corporativo:** [Link]({info.get('website', '#')})")
            with col_p2:
                st.markdown("**Resumen de Operaciones:**")
                st.info(info.get('longBusinessSummary', 'No disponible.'))

        # ==========================================
        # MODULO 3: ANÁLISIS TÉCNICO DE PRECIOS
        # ==========================================
        elif seccion == "📊 Análisis Técnico":
            st.subheader("📈 Gráfico de Cotización Estructurado")
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                periodo = st.selectbox("Rango Temporal:", ["1 Día", "5 Días", "1 Mes", "6 Meses", "1 Año", "Máximo Histórico"], index=2)
            with col_t2:
                intervalo = st.selectbox("Intervalo de Barras:", ["1 Minuto", "5 Minutos", "15 Minutos", "30 Minutos", "1 Hora", "1 Día", "1 Mes"], index=5)

            mapa_p = {"1 Día": "1d", "5 Días": "5d", "1 Mes": "1mo", "6 Meses": "6mo", "1 Año": "1y", "Máximo Histórico": "max"}
            mapa_i = {"1 Minuto": "1m", "5 Minutos": "5m", "15 Minutos": "15m", "30 Minutos": "30m", "1 Hora": "1h", "1 Día": "1d", "1 Mes": "1mo"}
            p_api, i_api = mapa_p[periodo], mapa_i[intervalo]

            if ("Minuto" in intervalo or "Hora" in intervalo) and p_api in ["6mo", "1y", "max"]:
                st.warning("⚠️ Ajuste automático: Las temporalidades intradía altas se limitan a rangos de 5 días.")
                p_api = "5d"

            historial = empresa.history(period=p_api, interval=i_api)
            if not historial.empty:
                st.line_chart(historial['Close'], use_container_width=True)

        # ==========================================
        # MODULO 4: TRANSACCIONES SEC (INSIDERS)
        # ==========================================
        elif seccion == "💼 Transacciones SEC":
            st.subheader("📅 Historial Cronológico de Compras y Ventas Oficiales")
            if insiders_raw is not None and not insiders_raw.empty:
                df_real = insiders_raw.reset_index()
                if 'index' in df_real.columns: df_real.rename(columns={'index': 'Fecha'}, inplace=True)
                df_real['Fecha'] = pd.to_datetime(df_real['Fecha']).dt.date
                
                cols = ['Fecha', 'Insider', 'Position', 'Text', 'Shares', 'Value']
                df_final = df_real[[c for c in cols if c in df_real.columns]].sort_values(by='Fecha', ascending=False)
                
                # Botón de extracción de datos para Excel
                st.download_button(label="📥 Exportar Matriz a CSV", data=df_final.to_csv(index=False).encode('utf-8'), file_name=f'{ticker}_sec_insiders.csv', mime='text/csv')
                st.dataframe(df_final, use_container_width=True)
            else:
                st.warning("Sin registros de transacciones internas archivados recientemente.")

        # ==========================================
        # MODULO 5: FLUJO INFORMATIVO (NOTICIAS)
        # ==========================================
        elif seccion == "📰 Flujo Informativo":
            st.subheader("📰 Titulares Financieros de Impacto Directo")
            if noticias_raw:
                for n in noticias_raw[:10]:
                    ts = n.get('providerPublishTime', None)
                    fecha_p = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M') if ts else "Ahora"
                    st.markdown(f"""
                    <div class="news-card">
                        <h4 style="margin:0;"><a href="{n.get('link', '#')}" target="_blank" style="text-decoration:none; color:#06b6d4;">{n.get('title')}</a></h4>
                        <div style="margin-top:10px; display:flex; justify-content:space-between; font-size:0.8em; color:#94a3b8;">
                            <span>Emisor: <b>{n.get('publisher')}</b></span>
                            <span>⏱️ {fecha_p}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error en el procesamiento del mercado financiero: {e}")