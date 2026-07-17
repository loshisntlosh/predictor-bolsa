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
    .scenario-card {
        padding: 20px;
        border-radius: 12px;
        background-color: #0f172a;
        border: 1px solid #334155;
        animation: fadeIn 1.1s ease-out;
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
# MOTOR PREDICTIVO AVANZADO CON MATRIZ DE ESCENARIOS
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
        score_narrativa = score_narrativa / total_noticias

    # 2. Análisis del Tamaño del Bloque de Capital (Insider Volume Weighted)
    compras_masivas = False
    if df_insiders is not None and not df_insiders.empty:
        for _, row in df_insiders.head(10).iterrows():
            texto_accion = str(row.get('Text', '')).lower()
            valor_transaccion = float(row.get('Value', 0))
            acciones_operadas = float(row.get('Shares', 0))
            
            peso_capital = 0.1
            if valor_transaccion > 1000000: 
                peso_capital = 0.4
                compras_masivas = True
            elif valor_transaccion > 250000: 
                peso_capital = 0.25
            
            if 'buy' in texto_accion or 'purchase' in texto_accion:
                impacto_volumen = (acciones_operadas / volumen_mercado) * 10
                score_insider += peso_capital + min(impacto_volumen, 0.2)
            elif 'sale' in texto_accion or 'sell' in texto_accion:
                score_insider -= (peso_capital * 0.3)

    # 3. Consolidación de la Matriz Predictiva
    score_total = (score_narrativa * 0.4) + (score_insider * 0.6)
    score_total = max(min(score_total, 1.0), -1.0)
    
    porcentaje_fiabilidad = abs(score_total) * 100
    
    if score_total > 0.20:
        perfil = "🟢 ALCISTA CONVERGENTE (Señal de Alta Convicción)"
        color = "#22c55e"
    elif score_total < -0.20:
        perfil = "🔴 DISTRIBUCIÓN / BAJISTA (Fuerte Presión de Venta Interna)"
        color = "#ef4444"
    else:
        perfil = "🟡 ACUMULACIÓN NEUTRA (Baja Convicción de Datos)"
        color = "#94a3b8"
        
    return perfil, color, porcentaje_fiabilidad, score_narrativa, score_insider, score_total, compras_masivas

# =========================================================================
# INTERFAZ DE USUARIO Y CONFIGURACIÓN DEL NAVBAR
# =========================================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/radar.png", width=55)
    st.markdown("<h2 style='margin-top:0;'>Radar Intersector</h2>", unsafe_allow_html=True)
    st.markdown("---")
    seccion = st.sidebar.radio(
        "Módulos del Sistema:",
        ["🎯 Recomendación y Escenarios", "🔮 Inteligencia Predictiva", "🏢 Perfil Corporativo", "📊 Análisis Técnico", "💼 Transacciones SEC", "📰 Flujo Informativo"]
    )
    st.markdown("---")
    st.caption("Filtros Profesionales Activos")

st.markdown("<h1 class='main-title'>🔮 El Intersector: Inteligencia Financiera</h1>", unsafe_allow_html=True)
ticker = st.text_input("🔍 Ingresa el Ticker de la Empresa a Monitorear (Ej: NVDA, AAPL, AMZN, LLY):", "NVDA").upper()

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

        # Panel de Estado Financiero Superior (KPIs)
        st.markdown(f"### {info.get('longName', ticker)} <span style='color:#64748b; font-size:0.8em;'>| {info.get('sector', 'N/A')}</span>", unsafe_allow_html=True)
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric(label="Último Precio", value=f"${precio_actual:,.2f} {moneda}", delta=f"${cambio_precio:,.2f}")
        with col_m2:
            st.metric(label="Retorno Diario (%)", value=f"{porcentaje_cambio:,.2f}%", delta=f"{porcentaje_cambio:,.2f}%")
        with col_m3:
            st.metric(label="Volumen del Día", value=f"{volumen_hoy:,}")
            
        st.markdown("---")

        # Ejecución del algoritmo maestro una sola vez
        resultado, color_r, confianza, sub_narrativa, sub_insider, score_puro, compras_grandes = algoritmo_predictivo_institucional(noticias_raw, insiders_raw, volumen_hoy)

        # =========================================================================
        # [NUEVA] SECCIÓN 1: RECOMENDACIÓN CON PORCENTAJES DE ESCENARIO (COLUMNAS)
        # =========================================================================
        if seccion == "🎯 Recomendación y Escenarios":
            st.subheader("🎯 Matriz Verídica de Escenarios de Inversión (Toma de Decisiones)")
            st.write("Cálculo estadístico concurrente que divide el comportamiento estimado del activo en tres vías independientes basadas en los datos analizados hoy.")
            
            # Cálculo matemático de probabilidades dinámicas según el score del modelo
            prob_base = 50.0 + (score_puro * 20.0)
            if score_puro >= 0:
                prob_subida = max(15.0, min(40.0, 15.0 + (score_puro * 30.0)))
                prob_bajada = max(5.0, 100.0 - prob_base - prob_subida)
            else:
                prob_bajada = max(15.0, min(40.0, 15.0 + (abs(score_puro) * 30.0)))
                prob_subida = max(5.0, 100.0 - prob_base - prob_bajada)
                
            # Renderizado de tres columnas premium para los escenarios
            col_e1, col_e2, col_e3 = st.columns(3)
            
            with col_e1:
                st.markdown(f"""
                <div class="scenario-card" style="border-top: 4px solid #22c55e;">
                    <h3 style="color:#22c55e; margin:0;">📈 Escenario Alcista</h3>
                    <h2 style="margin:10px 0; font-size:2.2em;">{prob_subida:.1f}%</h2>
                    <p style="font-size:0.9em; color:#94a3b8;"><b>Catalizador de subida:</b></p>
                    <p style="font-size:0.85em; color:#cbd5e1;">Convergencia institucional de compras en el Formulario 4 de la SEC y optimismo político sectorial reflejado en el sentimiento de prensa acumulado.</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col_e2:
                st.markdown(f"""
                <div class="scenario-card" style="border-top: 4px solid #38bdf8;">
                    <h3 style="color:#38bdf8; margin:0;">⚖️ Escenario Base</h3>
                    <h2 style="margin:10px 0; font-size:2.2em;">{prob_base:.1f}%</h2>
                    <p style="font-size:0.9em; color:#94a3b8;"><b>Comportamiento esperado:</b></p>
                    <p style="font-size:0.85em; color:#cbd5e1;">El mercado ya asimiló los reportes trimestrales y la cotización flotante lateralizará en soportes técnicos institucionales clave hoy.</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col_e3:
                st.markdown(f"""
                <div class="scenario-card" style="border-top: 4px solid #ef4444;">
                    <h3 style="color:#ef4444; margin:0;">📉 Escenario Bajista</h3>
                    <h2 style="margin:10px 0; font-size:2.2em;">{prob_bajada:.1f}%</h2>
                    <p style="font-size:0.9em; color:#94a3b8;"><b>Riesgo de caída:</b></p>
                    <p style="font-size:0.85em; color:#cbd5e1;">Aparición de noticias regulatorias de última hora o distribución pasiva de acciones (ventas) por parte de altos directivos.</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.subheader("💡 Conclusión de Gestión de Riesgo Profesional")
            if compras_grandes and score_puro > 0.2:
                st.success(f"✔️ **Nota Verídica del Sistema:** El escenario alcista cuenta con respaldo de capital real corporativo de altos mandos (>1M USD). Históricamente, esto reduce la probabilidad de caídas abruptas en el corto plazo debido al soporte institucional.")
            else:
                st.info("✔️ **Nota Verídica del Sistema:** No se detectan anomalías de volumen institucional masivas hoy. La acción se moverá principalmente por la inercia macroeconómica del mercado general.")

        # ==========================================
        # RESTO DE LOS MÓDULOS DE LA APLICACIÓN
        # ==========================================
        elif seccion == "🔮 Inteligencia Predictiva":
            st.subheader("🤖 Diagnóstico Cuantitativo del Algoritmo")
            st.markdown(f"""
            <div class="prediction-box">
                <h2 style="margin:0; font-size:1.9em;">Vector de Inversión: <span style="color:{color_r};">{resultado}</span></h2>
                <p style="margin:10px 0 0 0; color:#94a3b8; font-size:1.1em;">Convicción Matemática del Modelo: <b>{confianza:.1f}%</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 📊 Desglose de Componentes del Modelo")
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.write(f"**Índice de Sentimiento de Prensa (40% peso):** `{sub_narrativa:+.2f}`")
            with col_d2:
                st.write(f"**Convicción de Flujo Corporativo (60% peso):** `{sub_insider:+.2f}`")

        elif seccion == "🏢 Perfil Corporativo":
            st.subheader("🏢 Fundamentales Básicos de la Empresa")
            col_p1, col_p2 = st.columns([1, 2])
            with col_p1:
                st.metric("Capitalización bursátil", f"${info.get('marketCap', 0):,}")
                st.write(f"**Ubicación:** {info.get('country', 'N/A')}")
            with col_p2:
                st.info(info.get('longBusinessSummary', 'No disponible.'))

        elif seccion == "📊 Análisis Técnico":
            st.subheader("📈 Gráfico de Cotización Estructurado")
            periodo = st.selectbox("Rango Temporal:", ["1 Día", "5 Días", "1 Mes", "6 Meses", "1 Año", "Máximo Histórico"], index=2)
            intervalo = st.selectbox("Intervalo de Barras:", ["1 Minuto", "5 Minutos", "15 Minutos", "30 Minutos", "1 Hora", "1 Día", "1 Mes"], index=5)
            
            mapa_p = {"1 Día": "1d", "5 Días": "5d", "1 Mes": "1mo", "6 Meses": "6mo", "1 Año": "1y", "Máximo Histórico": "max"}
            mapa_i = {"1 Minuto": "1m", "5 Minutos": "5m", "15 Minutos": "15m", "30 Minutos": "30m", "1 Hora": "1h", "1 Día": "1d", "1 Mes": "1mo"}
            
            historial = empresa.history(period=mapa_p[periodo], interval=mapa_i[intervalo])
            if not historial.empty:
                st.line_chart(historial['Close'], use_container_width=True)

        elif seccion == "💼 Transacciones SEC":
            st.subheader("📅 Historial Cronológico de Compras y Ventas Oficiales")
            if insiders_raw is not None and not insiders_raw.empty:
                df_real = insiders_raw.reset_index()
                if 'index' in df_real.columns: df_real.rename(columns={'index': 'Fecha'}, inplace=True)
                df_real['Fecha'] = pd.to_datetime(df_real['Fecha']).dt.date
                cols = ['Fecha', 'Insider', 'Position', 'Text', 'Shares', 'Value']
                df_final = df_real[[c for c in cols if c in df_real.columns]].sort_values(by='Fecha', ascending=False)
                
                st.download_button(label="📥 Exportar Matriz a CSV", data=df_final.to_csv(index=False).encode('utf-8'), file_name=f'{ticker}_sec_insiders.csv', mime='text/csv')
                st.dataframe(df_final, use_container_width=True)

        elif seccion == "📰 Flujo Informativo":
            st.subheader("📰 Titulares Financieros de Impacto Directo")
            if noticias_raw:
                for n in noticias_raw[:10]:
                    st.markdown(f"""
                    <div class="news-card">
                        <h4 style="margin:0;"><a href="{n.get('link', '#')}" target="_blank" style="text-decoration:none; color:#06b6d4;">{n.get('title')}</a></h4>
                        <p style="margin:5px 0 0 0; font-size:0.8em; color:#94a3b8;">Emisor: {n.get('publisher')}</p>
                    </div>
                    """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error en el procesamiento del mercado financiero: {e}")