import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Configuración de pantalla completa y diseño oscuro por defecto
st.set_page_config(layout="wide", page_title="El Intersector - Finanzas", page_icon="👁️")

# Estilos CSS personalizados para que se vea premium y elegante
st.markdown("""
<style>
    .metric-box {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #334155;
    }
    .news-card {
        padding: 15px; 
        border-radius: 8px; 
        background-color: #0f172a; 
        margin-bottom: 12px;
        border-left: 5px solid #38bdf8;
    }
</style>
""", unsafe_allow_html=True)

# 2. NAVBAR (Menú de Navegación Lateral)
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/radar.png", width=60)
    st.title("Radar Intersector")
    st.markdown("---")
    # Secciones del Navbar
    seccion = st.radio(
        "Navegación:",
        ["📈 Panel Financiero", "💼 Altos Mandos (SEC)", "📰 Noticias del Sector"]
    )
    st.markdown("---")
    st.caption("Proyecto Predictor de Bolsa | Datos en Tiempo Real")

# 3. BUSCADOR PRINCIPAL (Siempre visible arriba)
ticker = st.text_input("🔍 Escribe el Ticker de la empresa (Ej: NVDA, AAPL, SRFM, LLY):", "NVDA").upper()

if ticker:
    try:
        # Cargamos los datos de la empresa una sola vez para ahorrar tiempo
        empresa = yf.Ticker(ticker)
        info = empresa.info
        
        # --- BLOQUE INTERACTIVO EN TIEMPO REAL ---
        # Extraemos precio actual y datos clave
        precio_actual = info.get('currentPrice', info.get('regularMarketPrice', 0.0))
        precio_previo = info.get('previousClose', 1.0)
        cambio_precio = precio_actual - precio_previo
        porcentaje_cambio = (cambio_precio / precio_previo) * 100
        nombre_empresa = info.get('longName', ticker)
        moneda = info.get('currency', 'USD')

        # Encabezado elegante
        st.subheader(f"{nombre_empresa} ({ticker})")
        
        # Métricas visuales en pantalla
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric(label="Precio en Tiempo Real", value=f"{precio_actual:.2f} {moneda}", delta=f"{cambio_precio:.2f}")
        with col_m2:
            st.metric(label="Cambio del Día", value=f"{porcentaje_cambio:.2f}%", delta=f"{porcentaje_cambio:.2f}%")
        with col_m3:
            st.metric(label="Volumen de Mercado", value=f"{info.get('regularMarketVolume', 0):,}")
            
        st.markdown("---")

        # --- LÓGICA DE LAS SECCIONES DEL NAVBAR ---
        
        # SECCIÓN 1: PANEL FINANCIERO
        if seccion == "📈 Panel Financiero":
            st.subheader("📊 Historial de Precio Reciente")
            # Gráfico interactivo nativo de Streamlit con los precios de cierre del último mes
            historial = empresa.history(period="1mo")
            if not historial.empty:
                st.line_chart(historial['Close'], use_container_width=True)
            else:
                st.info("No hay gráfico histórico disponible para este activo.")

        # SECCIÓN 2: ALTOS MANDOS (CON FECHAS VERIFICABLES)
        elif seccion == "💼 Altos Mandos (SEC)":
            st.subheader("📅 Transacciones de Insiders con Fecha")
            df = empresa.insider_transactions
            
            if df is not None and not df.empty:
                # Yahoo Finance guarda la fecha como el índice de la tabla. 
                # La convertimos en una columna visible llamada 'Fecha'
                df_con_fecha = df.reset_index()
                df_con_fecha.rename(columns={'index': 'Fecha / Hora'}, inplace=True)
                
                # Convertimos la fecha a un formato limpio y legible (Año-Mes-Día)
                df_con_fecha['Fecha / Hora'] = pd.to_datetime(df_con_fecha['Fecha / Hora']).dt.strftime('%Y-%m-%d')
                
                columnas_importantes = ['Fecha / Hora', 'Insider', 'Position', 'Text', 'Shares', 'Value']
                columnas_validas = [c for c in columnas_importantes if c in df_con_fecha.columns]
                
                df_mostrar = df_con_fecha[columnas_validas]
                
                # Mostramos la tabla organizada por fecha reciente
                st.dataframe(df_mostrar, use_container_width=True, height=500)
                
                # Alerta de compras
                compras = df_mostrar[df_mostrar['Text'].str.contains('Buy|Purchase', case=False, na=False)]
                if not compras.empty:
                    st.success(f"🔥 ¡Señal Detectada! Hay {len(compras)} compras de acciones por parte de directivos registradas en estas fechas.")
            else:
                st.warning("No se encontraron transacciones de directivos para esta empresa.")

        # SECCIÓN 3: NOTICIAS DEL SECTOR (CORREGIDO EL ERROR)
        elif seccion == "📰 Noticias del Sector":
            st.subheader("📰 Actualidad Informativa Seleccionada")
            noticias = empresa.news
            
            if noticias:
                for noticia in noticias[:8]: # Mostramos hasta 8 noticias
                    titulo = noticia.get('title', 'Sin título')
                    fuente = noticia.get('publisher', 'Fuente')
                    enlace = noticia.get('link', '#')
                    
                    # El diseño HTML en tarjetas limpias libre de errores
                    st.markdown(f"""
                    <div class="news-card">
                        <h4 style="margin:0;"><a href="{enlace}" target="_blank" style="text-decoration:none; color:#38bdf8;">{titulo}</a></h4>
                        <p style="margin:5px 0 0 0; font-size:0.85em; color:#94a3b8;">Publicado por: <b>{fuente}</b></p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No hay noticias de última hora registradas para este ticker.")

    except Exception as e:
        st.error(f"Error general en la plataforma con el ticker {ticker}: {e}")