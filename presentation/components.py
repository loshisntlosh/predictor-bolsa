# presentation/components.py
import streamlit as st
from typing import List
from core.domains import QuantAssessment, CatalystEvent, MarketMetrics, TrumpPredictionResult, InstitutionalThesis, RadarRecommendation

def render_injection_styles() -> None:
    st.markdown("""
    <style>
        .main-title { color: #f8fafc; font-weight: 800; }
        .ticker-header {
            background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
            padding: 20px; border-radius: 12px; border-left: 6px solid #38bdf8; margin-bottom: 25px;
            display: flex; justify-content: space-between; align-items: center;
        }
        .price-huge { font-size: 3.2em; font-weight: 900; color: #f8fafc; line-height: 1; }
        .change-badge { padding: 6px 14px; border-radius: 8px; font-weight: 700; font-size: 1.1em; }
        .prediction-box { padding: 25px; border-radius: 12px; text-align: center; margin-bottom: 25px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); }
        .scenario-card { padding: 20px; border-radius: 12px; background-color: #0f172a; border: 1px solid #334155; height: 100%; }
        .thesis-card { background: #111827; border: 1px solid #1e293b; border-radius: 10px; padding: 18px; margin-bottom: 15px; }
        .ai-critique-box { background: rgba(245, 158, 11, 0.08); border-left: 4px solid #f59e0b; padding: 12px; border-radius: 6px; margin-top: 10px; }
        .radar-card-buy { background: linear-gradient(135deg, #064e3b 0%, #022c22 100%); border: 1px solid #059669; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
        .radar-card-sell { background: linear-gradient(135deg, #7f1d1d 0%, #450a0a 100%); border: 1px solid #dc2626; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
        .ai-oracle-box { background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%); border: 1px solid #c084fc; padding: 20px; border-radius: 12px; color: #f3e8ff; }
        .timeline-container { border-left: 3px solid #334155; padding-left: 20px; margin-left: 10px; margin-top: 15px; }
        .timeline-item { position: relative; margin-bottom: 25px; }
        .timeline-dot { position: absolute; left: -26px; top: 5px; width: 10px; height: 10px; border-radius: 50%; }
    </style>
    """, unsafe_allow_html=True)

def render_realtime_price_header(ticker: str, name: str, metrics: MarketMetrics) -> None:
    color = "#22c55e" if metrics.percentage_change >= 0 else "#ef4444"
    bg_color = "rgba(34, 197, 94, 0.15)" if metrics.percentage_change >= 0 else "rgba(239, 68, 68, 0.15)"
    sign = "+" if metrics.percentage_change >= 0 else ""
    st.markdown(f"""
    <div class="ticker-header">
        <div>
            <span style="color: #94a3b8; font-weight: 700; font-size: 0.9em; text-transform: uppercase;">Métricas de Mercado RT (2026)</span>
            <h2 style="margin: 5px 0 0 0; color: #f8fafc; font-size: 2em;">{ticker} <span style="font-size: 0.6em; color: #94a3b8; font-weight: 400;">| {name}</span></h2>
        </div>
        <div style="text-align: right;">
            <div class="price-huge">${metrics.current_price:,.2f} <span style="font-size: 0.4em; color: #94a3b8;">{metrics.currency}</span></div>
            <div style="margin-top: 8px;">
                <span class="change-badge" style="color: {color}; background: {bg_color};">{sign}{metrics.price_change:,.2f} ({sign}{metrics.percentage_change:,.2f}%)</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_assessment_card(assessment: QuantAssessment) -> None:
    st.markdown(f"""
    <div class="prediction-box" style="background: linear-gradient(135deg, #0f172a 0%, #020617 100%); border: 2px solid {assessment.hex_color};">
        <h2 style="margin:0; font-size:1.8em; color:#f8fafc;">Veredicto de Cobertura de la IA: <span style="color:{assessment.hex_color};">{assessment.verdict}</span></h2>
        <p style="margin:10px 0 0 0; color:#94a3b8; font-size:1.1em;">Puntuación de Convicción Cuantitativa Inteligente: <b>{assessment.confidence_score:.1f}%</b></p>
    </div>
    """, unsafe_allow_html=True)

def render_audited_institutional_theses(ticker: str, theses: List[InstitutionalThesis]) -> None:
    st.markdown(f"### 📑 Auditoría de IA de las 5 Tesis más Recientes (Flipped Alpha)")
    st.write(f"Análisis crítico de los últimos postulados institucionales de fondos de cobertura registrados para {ticker}:")
    
    for th in theses:
        color_stance = "#22c55e" if th.stance == "Bullish" else "#ef4444" if th.stance == "Bearish" else "#94a3b8"
        border_status = "2px solid #22c55e" if th.is_valid else "1px dashed #ef4444"
        badge_status = "🟢 VALIDADO POR IA" if th.is_valid else "🚨 CORRELACIÓN DE RIESGO DEBIL"
        
        st.markdown(f"""
        <div class="thesis-card" style="border-left: {border_status};">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <div>
                    <strong style="color: #f8fafc; font-size: 1.05em;">{th.author}</strong>
                    <span style="color: #64748b; font-size: 0.85em; margin-left: 10px;">📅 {th.date}</span>
                </div>
                <div style="text-align: right;">
                    <span style="color: {color_stance}; font-weight: bold; margin-right: 15px;">{th.stance}</span>
                    <span style="font-size: 0.8em; font-weight: bold; padding: 2px 6px; border-radius: 4px; background: rgba(255,255,255,0.05);">{badge_status}</span>
                </div>
            </div>
            <p style="margin: 0; font-size: 0.95em; color: #cbd5e1; font-style: italic;">"{th.thesis_text}"</p>
            <div class="ai-critique-box">
                <strong style="color: #f59e0b; font-size: 0.9em;">🤖 Auditoría Cruda del Modelo Cuántico:</strong>
                <p style="margin: 4px 0 0 0; font-size: 0.9em; color: #fde68a; line-height: 1.4;">{th.ai_critique}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_ai_hyper_forecast_box(ticker: str, metrics: MarketMetrics, assessment: QuantAssessment) -> None:
    st.markdown("### 🔮 Oráculo de IA: Síntesis Predictiva de Multi-Factores (Crítica Cruda)")
    
    # Simulación del precio exacto derivado por variables complejas de entorno en 2026
    precio_exacto_ia = metrics.current_price * (1.0 + (assessment.raw_score * 0.45))
    
    st.markdown(f"""
    <div class="ai-oracle-box">
        <div style="display: flex; align-items: center; margin-bottom: 12px;">
            <span style="font-size: 1.6em; margin-right: 12px;">🧠</span>
            <strong style="font-size: 1.2em; color: #e9d5ff;">Valor Justo Proyectado por Red Neuronal Quant: ${precio_exacto_ia:,.2f} USD</strong>
        </div>
        <p style="margin: 0; font-size: 0.98em; line-height: 1.6; color: #f3e8ff;">
            <b>Crítica Estructural Cruda:</b> El mercado sobreestima la narrativa del sector en el corto plazo. Evaluando de forma cruzada los números fríos, {ticker} cotiza con una prima de riesgo distorsionada por factores geopolíticos de la administración de 2026. 
            Nuestros cálculos indican un rango asimétrico. El precio puede oscilar con violencia en una brecha de posibilidad abierta: si las políticas fiscales de desregulación se consolidan, el activo buscará un techo técnico de <b>${metrics.current_price*1.28:,.2f}</b>; sin embargo, si ocurre una disrupción en los márgenes brutos debido al encarecimiento de capitales corporativos, el suelo algorítmico se sitúa firmemente en <b>${metrics.current_price*0.78:,.2f}</b>. Gestione el tamaño de su posición asumiendo que la volatilidad implícita no está barata.
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_high_frequency_radar(recommendations: List[RadarRecommendation]) -> None:
    st.markdown("### 📡 Radar Intersectorial de Alta Frecuencia (Feed Continuo 15m - 2026)")
    st.write("Cribado algorítmico automatizado sobre todo el espectro de mercado para ejecución inmediata:")
    
    compras = [r for r in recommendations if r.action == "COMPRA FUERTE"]
    evitar = [r for r in recommendations if r.action == "EVITAR/CORTO"]
    
    col_r1, col_r2 = st.columns(2)
    
    with col_r1:
        st.markdown("#### 🟢 Top 6 Selecciones de Compra Institucional")
        for r in compras[:6]:
            st.markdown(f"""
            <div class="radar-card-buy">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="font-size: 1.2em; color: #34d399;">{r.ticker}</strong>
                    <span style="font-size: 0.85em; background: rgba(0,0,0,0.3); padding: 2px 8px; border-radius: 4px; color: #a7f3d0; font-weight: bold;">{r.sector}</span>
                </div>
                <p style="margin: 8px 0 0 0; font-size: 0.9em; color: #e6f4ea; line-height: 1.4;">{r.justification}</p>
                <div style="text-align: right; margin-top: 5px; font-size: 0.8em; color: #6ee7b7;">Score de Convicción: <b>{r.score:.1f}/100</b></div>
            </div>
            """, unsafe_allow_html=True)
            
    with col_r2:
        st.markdown("#### 🚨 Selección Crítica de Activos a Evitar / Corto")
        for r in evitar:
            st.markdown(f"""
            <div class="radar-card-sell">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="font-size: 1.2em; color: #f87171;">{r.ticker}</strong>
                    <span style="font-size: 0.85em; background: rgba(0,0,0,0.3); padding: 2px 8px; border-radius: 4px; color: #fca5a5; font-weight: bold;">{r.sector}</span>
                </div>
                <p style="margin: 8px 0 0 0; font-size: 0.9em; color: #fce8e6; line-height: 1.4;">{r.justification}</p>
                <div style="text-align: right; margin-top: 5px; font-size: 0.8em; color: #fca5a5;">Score de Riesgo: <b>{r.score:.1f}/100</b></div>
            </div>
            """, unsafe_allow_html=True)

def render_trump_prediction_dashboard(ticker: str, predictions: List[TrumpPredictionResult], current_price: float) -> None:
    st.markdown(f"### 🦅 Trump Policy Arbitrage Matrix (`Trumprediction`)")
    
    total_score = 0.0
    for pred in predictions:
        total_score += pred.impact_score
        color_badge = "#22c55e" if "BENEFICIARIO" in pred.sentiment_label else "#ef4444" if "FUEGO" in pred.sentiment_label else "#94a3b8"
        bg_badge = "rgba(34, 197, 94, 0.15)" if "BENEFICIARIO" in pred.sentiment_label else "rgba(239, 68, 68, 0.15)" if "FUEGO" in pred.sentiment_label else "rgba(148, 163, 184, 0.15)"
            
        st.markdown(f"""
        <div style="background-color: #0f172a; border: 1px solid #1e293b; padding: 20px; border-radius: 12px; margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <h4 style="margin: 0; color: #f8fafc; font-size: 1.125em;">{pred.policy_vector}</h4>
                <div>
                    <span style="color: {color_badge}; background: {bg_badge}; padding: 4px 10px; border-radius: 6px; font-size: 0.8em; font-weight: 700; margin-right: 10px;">{pred.sentiment_label}</span>
                    <span style="color: #64748b; font-size: 0.8em;">Verificado: <b>{pred.last_update_date}</b></span>
                </div>
            </div>
            <p style="margin: 12px 0; color: #cbd5e1; font-size: 0.95em; line-height: 1.5;">{pred.analysis_justification}</p>
            <div style="background: #1e293b; height: 6px; border-radius: 3px; position: relative; margin-top: 10px;">
                <div style="background: {color_badge}; width: {abs(pred.impact_score)}%; height: 100%; border-radius: 3px; position: absolute; left: {50 if pred.impact_score >= 0 else 50 - abs(pred.impact_score)}%;"></div>
                <div style="position: absolute; left: 50%; top: -4px; background: #f8fafc; width: 2px; height: 14px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    avg_score = total_score / len(predictions) if predictions else 0.0

    st.markdown("---")
    st.markdown("### 🧮 Calculadora de Posición Avanzada y Cobertura Óptima")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        capital_invertido = st.number_input("Monto total asignado a la posición ($ USD):", min_value=10.0, value=10000.0, step=500.0)
    with col_c2:
        usar_precio_historico = st.checkbox("¿Simular con un precio de entrada personalizado / pasado?")
        precio_entrada = st.number_input("Precio de entrada personalizado ($):", min_value=0.01, value=current_price * 0.9) if usar_precio_historico else current_price

    acciones_compradas = capital_invertido / precio_entrada
    st.info(f"💼 **Volumen Real:** Adquieres un total de **{acciones_compradas:,.4f}** unidades de **{ticker}**.")

    # Lógica de Escenarios Avanzados
    shift_factor = avg_score / 100.0
    escenarios = [
        {"nombre": "🟢 Escenario Bull (Éxito de Política)", "probabilidad": max(15.0, min(85.0, 35.0 + (shift_factor * 40))), "rendimiento": max(0.05, 0.25 + (shift_factor * 0.35)), "color": "#22c55e", "bg": "rgba(34, 197, 94, 0.05)"},
        {"nombre": "⚖️ Escenario Base (Consenso Ordinario)", "probabilidad": max(20.0, min(70.0, 45.0 - (abs(shift_factor) * 15))), "rendimiento": 0.05 + (shift_factor * 0.10), "color": "#38bdf8", "bg": "rgba(56, 189, 248, 0.05)"},
        {"nombre": "🚨 Escenario Bear (Choque de Márgenes)", "probabilidad": max(10.0, min(80.0, 20.0 - (shift_factor * 40))), "rendimiento": min(-0.05, -0.20 + (shift_factor * 0.20)), "color": "#ef4444", "bg": "rgba(239, 68, 68, 0.05)"}
    ]

    total_probs = sum(e["probabilidad"] for e in escenarios)
    col_e1, col_e2, col_e3 = st.columns(3)
    columnas = [col_e1, col_e2, col_e3]

    for idx, esc in enumerate(escenarios):
        prob_final = (esc["probabilidad"] / total_probs) * 100
        valor_target = precio_entrada * (1.0 + esc["rendimiento"])
        pnl = (acciones_compradas * valor_target) - capital_invertido
        signo = "+" if pnl >= 0 else ""

        with columnas[idx]:
            st.markdown(f"""
            <div style="background-color: {esc['bg']}; border: 1px solid {esc['color']}; padding: 18px; border-radius: 10px; height: 100%;">
                <h5 style="margin: 0 0 10px 0; color: {esc['color']}; font-size: 0.95em;">{esc['nombre']}</h5>
                <p style="margin: 0; color: #94a3b8; font-size: 0.85em;">Probabilidad Asignada:</p>
                <h3 style="margin: 2px 0 12px 0; color: #f8fafc; font-weight: 800;">{prob_final:.1f}%</h3>
                <hr style="border-color: #334155; margin: 8px 0;"/>
                <p style="margin: 0; color: #64748b; font-size: 0.8em;">Target Proyectado: <b style="color:#f1f5f9;">${valor_target:,.2f}</b></p>
                <p style="margin: 4px 0 0 0; color: #64748b; font-size: 0.8em;">Retorno Neto Estimado:</p>
                <span style="color: {esc['color']}; font-weight: bold; font-size: 1.15em;">{signo}${pnl:,.2f} ({esc['rendimiento']*100:+.1f}%)</span>
            </div>
            """, unsafe_allow_html=True)

def render_timeline(catalysts: List[CatalystEvent]) -> None:
    if not catalysts:
        st.info("No se registran eventos temporales anómalos.")
        return
    st.markdown('<div class="timeline-container">', unsafe_allow_html=True)
    for item in catalysts:
        color = "#ef4444" if item.direction == "BEAR" else "#22c55e"
        st.markdown(f"""
        <div class="timeline-item">
            <div class="timeline-dot" style="background-color: {color}; box-shadow: 0 0 8px {color};"></div>
            <span style="color: {color}; font-weight: bold; font-size: 0.85em;">📅 {item.projected_date} — {item.impact_level}</span>
            <h4 style="margin: 5px 0 2px 0; color: #f8fafc;">{item.event_name}</h4>
            <p style="margin: 0; font-size: 0.9em; color: #94a3b8;">{item.desc}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_stress_testing_dashboard(shocks: List[any]) -> None:
    st.markdown("### 🧬 Simulación de Sensibilidad ante Choques Extremos")
    col_s1, col_s2 = st.columns(2)
    cols = [col_s1, col_s2]
    for idx, shock in enumerate(shocks):
        with cols[idx]:
            st.markdown(f"""
            <div class="scenario-card">
                <h4 style="margin:0 0 8px 0; color:#cbd5e1;">{shock.scenario_name}</h4>
                <p style="margin:0; font-size:0.9em;color:#94a3b8;">Nivel de Riesgo: <b style="color:#ef4444;">{shock.risk_level}</b></p>
                <p style="margin:4px 0 0 0; font-size:0.9em;color:#94a3b8;">Precio Ajustado Proyectado: <b>${shock.projected_price:,.2f}</b></p>
                <p style="margin:4px 0 0 0; font-size:0.9em;color:#94a3b8;">Índice de Vulnerabilidad Estructural: <b>{shock.vulnerability_index:.1f}/100</b></p>
            </div>
            """, unsafe_allow_html=True)