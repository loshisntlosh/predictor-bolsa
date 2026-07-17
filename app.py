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
# MOTOR DE DETECCIÓN DE CATALIZADORES CORPORATIVOS (ALCISTAS)
# =========================================================================
def escanear_catalizadores_alcistas(info_empresa, df_insiders):
    catalizadores = []
    puntos_alcistas = 0
    
    # Catalizador 1: Recompra de Acciones (Share Buyback) - Indica que la empresa cree que está barata
    # Verificamos si hay indicios históricos o políticas vigentes en la data general
    if info_empresa.get('impliedSharesOutstanding') and info_empresa.get('sharesOutstanding'):
        if info_empresa.get('impliedSharesOutstanding') < info_empresa.get('sharesOutstanding'):
            catalizadores.append({
                "evento": "🔄 Programa de Recompra Activo (Buyback)",
                "impacto": "ALTO",
                "descripcion": "La reducción de acciones en circulación incrementa artificialmente el Beneficio por Acción (EPS), atrayendo fondos de cobertura."
            })
            puntos_alcistas += 25

    # Catalizador 2: Descuento Histórico Crítico (Mínimos de 52 semanas)
    precio_actual = float(info_empresa.get('currentPrice', 1.0))
    min_52 = float(info_empresa.get('fiftyTwoWeekLow', 1.0))
    max_52 = float(info_empresa.get('fiftyTwoWeekHigh', 1.0))
    
    # Si está a menos del 15% de su mínimo de un año, suele haber rebote institucional
    if (precio_actual - min_52) / min_52 < 0.15:
        catalizadores.append({
            "evento": "🛡️ Zona de Soporte Anual Proxima (52-Week Low)",
            "impacto": "MEDIO",
            "descripcion": "El activo cotiza cerca de niveles de liquidación institucional, activando órdenes automáticas de compra por valor (Value Investing)."
        })
        puntos_alcistas += 20
        
    # Catalizador 3: Alta Convicción de Altos Mandos (Insider Buying Masivo)
    if df_insiders is not None and not df_insiders.empty:
        compras_grandes = df_insiders[(df_insiders['Text'].str.contains('Buy|Purchase', case=False, na=False)) & (df_insiders['Value'] > 500000)]
        if not compras_grandes.empty:
            catalizadores.append({
                "evento": "💼 Inyección de Capital Interno Masivo (>500K USD)",
                "impacto": "CRÍTICO",
                "descripcion": f"Se registraron {len(compras_grandes)} transacciones de compra de gran volumen por miembros de la junta directiva en la SEC."
            })
            puntos_alcistas += 35

    # Catalizador 4: Margen Operativo Saludable (Ventaja Competitiva / Moat)
    margen_operativo = info_empresa.get('operatingMargins', 0.0)
    if margen_operativo > 0.20: # Más del 20% es excelente
        catalizadores.append({
            "evento": "💰 Eficiencia Operativa Superior (Margen > 20%)",
            "impacto": "MEDIO",
            "descripcion": f"El margen operativo de {margen_operativo*100:.1f}% demuestra un sólido foso económico para resistir presiones inflacionarias."
        })
        puntos_alcistas += 20

    return catalizadores, puntos_alcistas

# =========================================================================
# ALGORITMO PREDICTIVO DE MATRIZ DE ESCENARIOS
# =========================================================================
def algoritmo_predictivo_institucional(noticias, df_insiders, volumen_mercado, puntos_cat):
    score_narrativa = 0.0
    score_insider = 0.0
    
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

    if df_insiders is not None and not df_insiders.empty:
        for _, row in df_insiders.head(10).iterrows():
            texto_accion = str(row.get('Text', '')).lower()
            valor_transaccion = float(row.get('Value', 0))
            
            peso_capital = 0.1
            if valor_transaccion > 1000000: peso_capital = 0.4
            elif valor_transaccion > 250000: peso_capital = 0.25
            
            if 'buy' in texto_accion or 'purchase' in texto_accion:
                score_insider += peso_capital
            elif 'sale' in texto_accion or 'sell' in texto_accion:
                score_insider -= (peso_capital * 0.3)

    # Inyección de los puntos de catalizadores reales en el score final
    peso_catalizadores = (puntos_cat / 100) * 0.5
    score_total = (score_narrativa * 0.2) + (score_insider * 0.3) + peso_catalizadores
    score_total = max(min(score_total, 1.0), -1.0)
    
    porcentaje_fiabilidad = abs(score_total) * 100
    
    if score_total > 0.15:
        perfil = "🟢 COMPRA ESTRUCTURAL (Fuerte Presencia de Catalizadores)"
        color = "#22c55e"
    elif score_total < -0.15:
        perfil = "🔴 RIESGO DE DISTRIBUCIÓN (Ausencia de Catalizadores de Valor)"
        color = "#ef4444"
    else:
        perfil = "🟡 RANGO NEUTRO / LATERAL"
        color = "#94a3b8"
        
    return perfil, color, porcentaje_fiabilidad, score_total

# =========================================================================
# INTERFAZ DE USUARIO Y CONFIGURACIÓN DEL NAVBAR
# =========================================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/radar.png", width=55)
    st.markdown("<h2 style='margin-top:0;'>Radar Intersector</h2>", unsafe_allow_html=True)
    st.markdown("---")
    seccion = st.sidebar.radio(
        "Módulos de Inversión:",
        ["🔥 Escáner de Catalizadores", "🎯 Recomendación y Escenarios", "🔮 Inteligencia Predictiva", "🏢 Perfil Corporativo", "📊 Análisis Técnico", "💼 Transacciones SEC"]
    )
    st.markdown("---")
    st.caption("Terminal Cuantitativa v2.4")

st.markdown("<h1 class='main-title'>🔮 El Intersector: Inteligencia Financiera</h1>", unsafe_allow_html=True)
ticker = st.text_input("🔍 Ticker de la Empresa (Ej: NVDA, AAPL, AMZN, LLY, TSLA):", "NVDA").upper()

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
        with col_m2: st.metric(label="Retorno Diario (%)", value=f"{porcentaje_cambio:,.2f}%", delta=f"{porcentaje_cambio:,.2f}%")
        with col_m3: st.metric(label="Volumen del Día", value=f"{volumen_hoy:,}")
        st.markdown("---")

        # Escaneo previo de catalizadores duros
        lista_catalizadores, puntos_totales_cat = escanear_catalizadores_alcistas(info, insiders_raw)
        resultado, color_r, confianza, score_puro = algoritmo_predictivo_institucional(noticias_raw, insiders_raw, volumen_hoy, puntos_totales_cat)

        # =========================================================================
        # [NUEVO] MÓDULO 1: ESCÁNER DE CATALIZADORES ALCISTAS
        # =========================================================================
        if seccion == "🔥 Escáner de Catalizadores":
            st.subheader("🔥 Escáner de Catalizadores Corporativos e Institucionales")
            st.write("Identificación algorítmica de eventos macro y microeconómicos verificables que sustentan presiones de compra inminentes.")
            
            if lista_catalizadores:
                # Mostrar los catalizadores en tarjetas organizadas
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
                st.warning("⚠️ Análisis Neutral: No se detectan anomalías de catalizadores específicos en este bloque. El activo depende estrictamente de su beta de mercado general.")

            # Indicador de Asimetría de Riesgo
            st.markdown("---")
            st.subheader("🛡️ Evaluación del Margen de Seguridad e Inversión Asimétrica")
            
            # Cálculo del Ratio de Asimetría basado en catalizadores vs volatilidad
            if puntos_totales_cat > 40:
                st.success("✔️ **Asimetría Altamente Positiva:** Las fuerzas corporativas internas ofrecen un colchón fundamental fuerte. La probabilidad de pérdida de capital permanente en estos niveles se reduce estadísticamente según la Teoría del Mosaico.")
            else:
                st.info("⚠️ **Asimetría Simétrica:** No hay ventajas estadísticas claras en este momento. El perfil riesgo/beneficio está equilibrado.")

        # =========================================================================
        # MÓDULO 2: RECOMENDACIÓN Y ESCENARIOS
        # =========================================================================
        elif seccion == "🎯 Recomendación y Escenarios":
            st.subheader("🎯 Matriz Verídica de Escenarios de Inversión")
            
            prob_base = max(10.0, min(80.0, 50.0 + (score_puro * 25.0)))
            if score_puro >= 0:
                prob_subida = max(15.0, min(45.0, 15.0 + (score_puro * 35.0)))
                prob_bajada = max(5.0, 100.0 - prob_base - prob_subida)
            else:
                prob_bajada = max(15.0, min(45.0, 15.0 + (abs(score_puro) * 35.0)))
                prob_subida = max(5.0, 100.0 - prob_base - prob_bajada)
                
            col_e1, col_e2, col_e3 = st.columns(3)
            with col_e1:
                st.markdown(f'<div class="scenario-card" style="border-top: 4px solid #22c55e;"><h3 style="color:#22c55e; margin:0;">📈 Escenario Alcista</h3><h2 style="margin:10px 0; font-size:2.2em;">{prob_subida:.1f}%</h2><p style="font-size:0.85em; color:#cbd5e1;">Presión por catalizadores de volumen de compra acumulados y resiliencia en márgenes operativos operativos.</p></div>', unsafe_allow_html=True)
            with col_e2:
                st.markdown(f'<div class="scenario-card" style="border-top: 4px solid #38bdf8;"><h3 style="color:#38bdf8; margin:0;">⚖️ Escenario Base</h3><h2 style="margin:10px 0; font-size:2.2em;">{prob_base:.1f}%</h2><p style="font-size:0.85em; color:#cbd5e1;">Consolidación de precio en rangos medios institucionales, asimilando noticias anteriores sin catalizadores disruptivos a corto plazo.</p></div>', unsafe_allow_html=True)
            with col_e3:
                st.markdown(f'<div class="scenario-card" style="border-top: 4px solid #ef4444;"><h3 style="color:#ef4444; margin:0;">📉 Escenario Bajista</h3><h2 style="margin:10px 0; font-size:2.2em;">{prob_bajada:.1f}%</h2><p style="font-size:0.85em; color:#cbd5e1;">Distribución/Venta sistemática si la inercia macroeconómica del sector se deteriora o se reduce la liquidez de mercado global.</p></div>', unsafe_allow_html=True)

        # =========================================================================
        # RECOPILED TRADITIONAL MODULES (Preservados e Integrados)
        # =========================================================================
        elif seccion == "🔮 Inteligencia Predictiva":
            st.subheader("🤖 Diagnóstico Cuantitativo del Algoritmo")
            st.markdown(f'<div class="prediction-box"><h2 style="margin:0; font-size:1.9em;">Vector de Inversión: <span style="color:{color_r};">{resultado}</span></h2><p style="margin:10px 0 0 0; color:#94a3b8; font-size:1.1em;">Convicción Matemática Combinada: <b>{confianza:.1f}%</b></p></div>', unsafe_allow_html=True)

        elif seccion == "🏢 Perfil Corporativo":
            st.subheader("🏢 Fundamentales Básicos de la Empresa")
            st.metric("Capitalización bursátil", f"${info.get('marketCap', 0):,}")
            st.info(info.get('longBusinessSummary', 'No disponible.'))

        elif seccion == "📊 Análisis Técnico":
            st.subheader("📈 Gráfico de Cotización Estructurado")
            historial = empresa.history(period="1mo", interval="1d")
            if not historial.empty: st.line_chart(historial['Close'], use_container_width=True)

        elif seccion == "💼 Transacciones SEC":
            st.subheader("📅 Historial Cronológico de Compras y Ventas Oficiales")
            if insiders_raw is not None and not insiders_raw.empty:
                st.dataframe(insiders_raw.head(20), use_container_width=True)

    except Exception as e:
        st.error(f"Error en el procesamiento del mercado financiero o Ticker incorrecto: {e}")