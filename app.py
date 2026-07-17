import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN DE PANTALLA Y ESTILOS VISUALES PREMIUM
st.set_page_config(layout="wide", page_title="El Intersector: Inteligencia de Mercados", page_icon="🔮")

# Inyección de CSS para diseño oscuro, animaciones Fade-In y efectos Hover interactivos
st.markdown("""
<style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .main-title {
        animation: fadeIn 0.8s ease-out;
        color: #f8fafc;
        font-weight: 800;
    }
    .prediction-box { 
        padding: 22px; 
        border-radius: 12px; 
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #06b6d4; 
        text-align: center;
        animation: fadeIn 1s ease-out;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        margin-bottom: 25px;
    }
    .news-card {
        padding: 18px; 
        border-radius: 10px; 
        background-color: #1e293b; 
        margin-bottom: 15px;
        border-left: 5px solid #06b6d4;
        animation: fadeIn 1.1s ease-out;
        transition: transform 0.2s, border-left 0.2s;
    }
    .news-card:hover {
        transform: scale(1.015);
        border-left: 5px solid #22c55e;
        background-color: #1e293bfa;
    }
</style>
""", unsafe_allow_html=True)

# 2. ALGORITMO: MOTOR PREDICTIVO DE NARRATIVA (IA BÁSICA)
def calcular_prediccion_narrativa(noticias, df_insiders):
    score = 0.0
    
    # Diccionarios de impacto semántico institucional y político
    palabras_alcistas = ['growth', 'profit', 'buy', 'upgrade', 'innovation', 'approval', 'record', 'bullish', 'expansion', 'partnership']
    palabras_bajistas = ['lawsuit', 'loss', 'downgrade', 'risk', 'regulatory', 'investigation', 'declining', 'bearish', 'fine', 'deficit']
    
    # Análisis de texto en los titulares de prensa actuales
    if noticias:
        for n in noticias:
            titulo = n.get('title', '').lower()
            if any(word in titulo for word in palabras_alcistas): 
                score += 0.15
            if any(word in titulo for word in palabras_bajistas): 
                score -= 0.15
    
    # Factor de Convicción: Compras reales de altos mandos (Insider Trading legal)
    if df_insiders is not None and not df_insiders.empty:
        transacciones_texto = " ".join(df_insiders['Text'].astype(str).tolist()).lower()
        if 'buy' in transacciones_texto or 'purchase' in transacciones_texto:
            score += 0.35  # Gran peso si los CEOs arriesgan su propio dinero
        if 'sale' in transacciones_texto or 'sell' in transacciones_texto:
            score -= 0.10  # Peso menor, las ventas a veces son para pagar impuestos
            
    # Acotar el puntaje matemático entre [-1.0, 1.0]
    score = max(min(score, 1.0), -1.0)
    porcentaje_confianza = abs(score) * 100
    
    # Clasificación de la señal libre de especulación directa
    if score > 0.25:
        return "⚡ ALCISTA (Posible Oportunidad de Compra)", "#22c55e", porcentaje_confianza
    elif score < -0.25:
        return "🚨 BAJISTA (Riesgo de Corrección Detectado)", "#ef4444", porcentaje_confianza
    else:
        return "⚖️ NEUTRO (Consolidación / Esperando Catalizadores)", "#94a3b8", porcentaje_confianza

# 3. NAVGACIÓN LATERAL (NAVBAR)
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/radar.png", width=55)
    st.markdown("<h2 style='margin-top:0;'>Radar Intersector</h2>", unsafe_allow_html=True)
    st.markdown("---")
    seccion = st.radio(
        "Módulos del Sistema:",
        ["🔮 Analizador Predictivo (IA)", "📊 Gráfico Avanzado", "💼 Altos Mandos (SEC)", "📰 Noticias del Sector"]
    )
    st.markdown("---")
    st.caption("Filtros en Tiempo Real Activos")
    st.info("⚠️ Aviso: Este prototipo procesa datos públicos agregados mediante la Teoría del Mosaico. No constituye asesoría financiera.")

# 4. ENCABEZADO Y BUSCADOR PRINCIPAL (Siempre en el Top)
st.markdown("<h1 class='main-title'>🔮 El Intersector: Inteligencia Financiera</h1>", unsafe_allow_html=True)
ticker = st.text_input("🔍 Escribe el Ticker de la empresa a investigar (Ej: NVDA, AAPL, AMZN, LLY):", "NVDA").upper()

if ticker:
    try:
        # Petición global a la API del mercado
        empresa = yf.Ticker(ticker)
        info = empresa.info
        noticias_raw = empresa.news
        insiders_raw = empresa.insider_transactions
        
        # Extracción y casteo estricto de floats numéricos en tiempo real
        precio_actual = float(info.get('currentPrice', info.get('regularMarketPrice', 0.0)))
        precio_previo = float(info.get('previousClose', 1.0))
        cambio_precio = precio_actual - precio_previo
        porcentaje_cambio = (cambio_precio / precio_previo) * 100
        nombre_empresa = info.get('longName', ticker)
        moneda = info.get('currency', 'USD')
        sector = info.get('sector', 'No especificado')

        # Panel de Estado Financiero Superior Elegante
        st.markdown(f"### {nombre_empresa} <span style='color:#64748b; font-size:0.8em;'>| Sector: {sector}</span>", unsafe_allow_html=True)
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric(label="Precio de Mercado (Float)", value=f"${precio_actual:,.2f} {moneda}", delta=f"${cambio_precio:,.2f}")
        with col_m2:
            st.metric(label="Variación Porcentual", value=f"{porcentaje_cambio:,.2f}%", delta=f"{porcentaje_cambio:,.2f}%")
        with col_m3:
            st.metric(label="Volumen Operado Hoy", value=f"{info.get('regularMarketVolume', 0):,}")
            
        st.markdown("---")

        # ==========================================
        # SECCIÓN A: MOTOR PREDICTIVO CON IA
        # ==========================================
        if seccion == "🔮 Analizador Predictivo (IA)":
            st.subheader("🤖 Diagnóstico de Probabilidad de Tendencia Diaria")
            st.write("Análisis cuantitativo instantáneo que cruza la tendencia narrativa política/financiera con el comportamiento de la junta directiva.")
            
            # Ejecución del algoritmo unificado
            resultado, color_resultado, confianza = calcular_prediccion_narrativa(noticias_raw, insiders_raw)
            
            st.markdown(f"""
            <div class="prediction-box">
                <h2 style="margin:0; font-size:1.8em;">Sentimiento Técnico: <span style="color:{color_resultado};">{resultado}</span></h2>
                <p style="margin:10px 0 0 0; color:#94a3b8; font-size:1.1em;">Convicción Algorítmica Basada en Datos: <b>{confianza:.1f}%</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Guía rápida interpretativa para el usuario
            st.markdown("#### 🤔 ¿Cómo interpretar este porcentaje?")
            st.info("• **Puntaje Alto (>60%):** Fuerte convergencia. Las noticias del sector y las compras de los directivos apuntan en una misma dirección directa.\n\n• **Puntaje Bajo (<30%):** Incertidumbre o fuerzas cruzadas (ej. noticias malas pero CEOs comprando, o viceversa). Se sugiere cautela para operaciones intradía.")

        # ==========================================
        # SECCIÓN B: GRÁFICO AVANZADO CON FILTROS
        # ==========================================
        elif seccion == "📊 Gráfico Avanzado":
            st.subheader("📈 Gráfico de Cotización con Temporalidad Variable")
            
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                periodo = st.selectbox(
                    "Rango Histórico de Datos:",
                    ["1 Día", "5 Días", "1 Mes", "6 Meses", "1 Año", "Máximo Histórico"], index=2
                )
            with col_t2:
                intervalo = st.selectbox(
                    "Intervalo de las Velas / Barras:",
                    ["1 Minuto", "5 Minutos", "15 Minutos", "30 Minutos", "1 Hora", "1 Día", "1 Mes"], index=5
                )

            # Mapeo técnico de variables para llamadas a yfinance
            mapa_p = {"1 Día": "1d", "5 Días": "5d", "1 Mes": "1mo", "6 Meses": "6mo", "1 Año": "1y", "Máximo Histórico": "max"}
            mapa_i = {"1 Minuto": "1m", "5 Minutos": "5m", "15 Minutos": "15m", "30 Minutos": "30m", "1 Hora": "1h", "1 Día": "1d", "1 Mes": "1mo"}
            
            p_api, i_api = mapa_p[periodo], mapa_i[intervalo]

            # Corrección automática de restricciones de la API para minutos
            if "Minuto" in intervalo or "Hora" in intervalo:
                if p_api in ["6mo", "1y", "max"]:
                    st.warning("⚠️ Nota: Las frecuencias de minutos solo están disponibles para rangos máximos de 5 días por regulaciones de almacenamiento de datos. Ajustando ventana temporal.")
                    p_api = "5d"

            historial = empresa.history(period=p_api, interval=i_api)
            if not historial.empty:
                st.line_chart(historial['Close'], use_container_width=True)
                st.caption(f"Visualización activa: Intervalo '{intervalo}' de forma continua sobre el rango '{periodo}'.")
            else:
                st.error("Error en la matriz de datos: No se consolidaron precios para este bloque específico de tiempo.")

        # ==========================================
        # SECCIÓN C: ALTOS MANDOS CON FECHA REAL
        # ==========================================
        elif seccion == "💼 Altos Mandos (SEC)":
            st.subheader("📅 Registro Cronológico de Transacciones Internas (Insiders)")
            st.write("Muestra la fecha de operación exacta y verificable reportada ante el regulador.")
            
            if insiders_raw is not None and not insiders_raw.empty:
                df_real = insiders_raw.reset_index()
                
                # Extracción y formateo limpio de la marca de tiempo de la SEC
                if 'index' in df_real.columns:
                    df_real.rename(columns={'index': 'Fecha Efectiva'}, inplace=True)
                
                df_real['Fecha Efectiva'] = pd.to_datetime(df_real['Fecha Efectiva']).dt.date
                
                cols_validas = ['Fecha Efectiva', 'Insider', 'Position', 'Text', 'Shares', 'Value']
                df_final = df_real[[c for c in cols_validas if c in df_real.columns]].sort_values(by='Fecha Efectiva', ascending=False)
                
                st.dataframe(df_final, use_container_width=True, height=450)
                
                # Alertas visuales dinámicas
                compras = df_final[df_final['Text'].str.contains('Buy|Purchase', case=False, na=False)]
                if not compras.empty:
                    st.success(f"🔥 Anomalía de Convicción: Detectadas {len(compras)} compras directas por miembros de la mesa de control corporativo.")
            else:
                st.warning("No hay transacciones registradas de insiders para este activo en los últimos meses.")

        # ==========================================
        # SECCIÓN D: NOTICIAS DEL SECTOR CON HOVER
        # ==========================================
        elif seccion == "📰 Noticias del Sector":
            st.subheader(f"📰 Flujo de Prensa Cruzada: {ticker} y Entorno Político")
            
            if noticias_raw:
                for n in noticias_raw[:10]:
                    titulo = n.get('title', 'Sin título')
                    fuente = n.get('publisher', 'Medio de Comunicación')
                    enlace = n.get('link', '#')
                    
                    # Convertir timestamp a formato legible
                    ts = n.get('providerPublishTime', None)
                    fecha_p = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M') if ts else "Reciente"
                    
                    st.markdown(f"""
                    <div class="news-card">
                        <h4 style="margin:0;"><a href="{enlace}" target="_blank" style="text-decoration:none; color:#06b6d4;">{titulo}</a></h4>
                        <div style="margin-top:10px; display:flex; justify-content:space-between; font-size:0.8em; color:#94a3b8;">
                            <span>Medio Emisor: <b>{fuente}</b></span>
                            <span>⏱️ Publicación: {fecha_p}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Sin registros de prensa localizados en los agregadores digitales para esta sesión.")

    except Exception as e:
        st.error(f"Error general en los servidores de consulta de datos. Revisa las siglas o reintenta. Detalles: {e}")