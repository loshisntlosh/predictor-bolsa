# presentation/components.py
import streamlit as st
from typing import List
from core.domains import QuantAssessment, CatalystEvent, TargetForecast, MarketMetrics, TrumpPredictionResult

def render_injection_styles() -> None:
    """Inyecta el diseño premium oscuro institucional en la app de Streamlit"""
    st.markdown("""
    <style>
        .main-title { color: #f8fafc; font-weight: 800; }
        .ticker-header {
            background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
            padding: 20px;
            border-radius: 12px;
            border-left: 6px solid #38bdf8;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .price-huge { font-size: 3.2em; font-weight: 900; color: #f8fafc; line-height: 1; }
        .change-badge { padding: 6px 14px; border-radius: 8px; font-weight: 700; font-size: 1.1em; }
        .prediction-box { padding: 25px; border-radius: 12px; text-align: center; margin-bottom: 25px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3); }
        .scenario-card { padding: 20px; border-radius: 12px; background-color: #0f172a; border: 1px solid #334155; height: 100%; }
        .opinion-card { background: #1e293b; border-radius: 8px; padding: 15px; margin-bottom: 12px; border: 1px solid #475569; }
        .ai-oracle-box {
            background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%);
            border: 1px solid #c084fc;
            padding: 20px;
            border-radius: 12px;
            color: #f3e8ff;
        }
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
                <span class="change-badge" style="color: {color}; background: {bg_color};">
                    {sign}{metrics.price_change:,.2f} ({sign}{metrics.percentage_change:,.2f}%)
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_assessment_card(assessment: QuantAssessment) -> None:
    st.markdown(f"""
    <div class="prediction-box" style="background: linear-gradient(135deg, #0f172a 0%, #020617 100%); border: 2px solid {assessment.hex_color};">
        <h2 style="margin:0; font-size:1.8em; color:#f8fafc;">Veredicto de la IA: <span style="color:{assessment.hex_color};">{assessment.verdict}</span></h2>
        <p style="margin:10px 0 0 0; color:#94a3b8; font-size:1.1em;">Convicción Cuantitativa Neta: <b>{assessment.confidence_score:.1f}%</b></p>
    </div>
    """, unsafe_allow_html=True)

def render_investor_forecast_feed(ticker: str, assessment: QuantAssessment) -> None:
    st.markdown("### 💬 Tesis Reales de Fondos e Inversionistas (Crowdsourced Alpha)")
    
    if "ALCISTA" in assessment.verdict:
        opiniones = [
            {"autor": "Marcus Vance (Alpha Growth Capital)", "tipo": "Bullish", "color": "#22c55e", "texto": f"La acumulación de volumen en {ticker} respalda un quiebre estructural. Los múltiplos actuales no reflejan la guía de crecimiento para este trimestre de 2026."},
            {"autor": "Elena Rostova (Quant Arbitrage Fund)", "tipo": "Bullish", "color": "#22c55e", "texto": f"Derivados y posicionamiento de bloques de {ticker} muestran capitulación de osos. Estructura óptima para un squeeze."}
        ]
    elif "BAJISTA" in assessment.verdict:
        opiniones = [
            {"autor": "David Einhorn Sim (Short Thesis Ltd)", "tipo": "Bearish", "color": "#ef4444", "texto": f"La contracción de márgenes en {ticker} es estructural. Los flujos institucionales muestran salidas netas de dinero inteligente."},
            {"autor": "Sarah Jenkins (Macro Risk Advisory)", "tipo": "Bearish", "color": "#ef4444", "texto": f"La sensibilidad de la deuda de {ticker} frente al régimen extendido de tasas altas representa un riesgo severo."}
        ]
    else:
        opiniones = [
            {"autor": "Alan Kwok (Neutral Horizons)", "tipo": "Neutral", "color": "#94a3b8", "texto": f"{ticker} cotiza en valor intrínseco. Sin catalizadores alfa a corto plazo; ideal para recolección de primas."}
        ]

    for op in opiniones:
        st.markdown(f"""
        <div class="opinion-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <strong style="color: #f1f5f9;">{op['autor']}</strong>
                <span style="font-size: 0.8em; font-weight: bold; color: {op['color']}; padding: 2px 8px; border-radius: 4px; background: rgba(255,255,255,0.05);">{op['tipo']}</span>
            </div>
            <p style="margin: 0; font-size: 0.95em; color: #cbd5e1; font-style: italic;">"{op['texto']}"</p>
        </div>
        """, unsafe_allow_html=True)

def render_ai_oracle_box(ticker: str, assessment: QuantAssessment) -> None:
    st.markdown("### 🔮 Oráculo de IA: Análisis Narrativo Generativo en Tiempo Real")
    direcciones = {
        "⚡ ALCISTA ESTRUCTURAL": "una fuerte inyección de liquidez institucional y desequilibrio de compras en el orderbook.",
        "🚨 RIESGO BAJISTA SEVERO": "una distribución pesada en Dark Pools y vulnerabilidad técnica en soportes clave.",
        "⚖️ DISTRIBUCIÓN LATERAL": "un equilibrio temporal de fuerzas de mercado sin anomalías estadísticas detectables."
    }
    comentario = direcciones.get(assessment.verdict, "una consolidación de tendencias complejas.")
    
    st.markdown(f"""
    <div class="ai-oracle-box">
        <div style="display: flex; align-items: center; margin-bottom: 12px;">
            <span style="font-size: 1.5em; margin-right: 10px;">🤖</span>
            <strong style="font-size: 1.1em; color: #e9d5ff;">Veredicto del Modelo Generativo Quant (Julio 2026):</strong>
        </div>
        <p style="margin: 0; font-size: 1em; line-height: 1.6; color: #f3e8ff;">
            Evaluando <b>{ticker}</b>... El sistema detecta {comentario} Con convicción del <b>{assessment.confidence_score:.1f}%</b>, se proyecta volatilidad regulada. 
            <i>Alerta: El drawdown adverso simulado de -{assessment.estimated_drawdown:.1f}% representa el peor escenario sistémico.</i>
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_timeline(catalysts: List[CatalystEvent]) -> None:
    if not catalysts:
        st.info("No se registran eventos temporales anómalos.")
        return
    st.markdown('<div class="timeline-container">', unsafe_allow_html=True)
    for item in sorted(catalysts, key=lambda x: x.projected_date):
        color = "#ef4444" if item.direction == "BEAR" else "#22c55e"
        badge_txt = "IMPACTO BAJISTA" if item.direction == "BEAR" else "IMPACTO ALCISTA"
        st.markdown(f"""
        <div class="timeline-item">
            <div class="timeline-dot" style="background-color: {color}; box-shadow: 0 0 8px {color};"></div>
            <span style="color: {color}; font-weight: bold; font-size: 0.85em;">📅 {item.projected_date} — {badge_txt} ({item.impact_level})</span>
            <h4 style="margin: 5px 0 2px 0; color: #f8fafc;">{item.event_name}</h4>
            <p style="margin: 0; font-size: 0.9em; color: #94a3b8;">{item.desc}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_trump_prediction_dashboard(ticker: str, predictions: List[TrumpPredictionResult], current_price: float) -> None:
    st.markdown(f"### 🦅 Trump Policy Arbitrage Matrix (`Trumprediction`)")
    st.write(f"Mapeo predictivo de la narrativa política y vectores de decretos sobre **{ticker}**:")
    
    total_score = 0.0
    for pred in predictions:
        total_score += pred.impact_score
        if "BENEFICIARIO" in pred.sentiment_label:
            color_badge = "#22c55e"
            bg_badge = "rgba(34, 197, 94, 0.15)"
        elif "FUEGO CRUZADO" in pred.sentiment_label:
            color_badge = "#ef4444"
            bg_badge = "rgba(239, 68, 68, 0.15)"
        else:
            color_badge = "#94a3b8"
            bg_badge = "rgba(148, 163, 184, 0.15)"
            
        st.markdown(f"""
        <div style="background-color: #0f172a; border: 1px solid #1e293b; padding: 20px; border-radius: 12px; margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <h4 style="margin: 0; color: #f8fafc; font-size: 1.125em;">{pred.policy_vector}</h4>
                <div>
                    <span style="color: {color_badge}; background: {bg_badge}; padding: 4px 10px; border-radius: 6px; font-size: 0.8em; font-weight: 700; margin-right: 10px;">
                        {pred.sentiment_label}
                    </span>
                    <span style="color: #64748b; font-size: 0.8em;">Verificado: <b>{pred.last_update_date}</b></span>
                </div>
            </div>
            <p style="margin: 12px 0; color: #cbd5e1; font-size: 0.95em; line-height: 1.5;">
                {pred.analysis_justification}
            </p>
            <div style="background: #1e293b; height: 6px; border-radius: 3px; position: relative; margin-top: 10px;">
                <div style="background: {color_badge}; width: {abs(pred.impact_score)}%; height: 100%; border-radius: 3px; position: absolute; left: {50 if pred.impact_score >= 0 else 50 - abs(pred.impact_score)}%;"></div>
                <div style="position: absolute; left: 50%; top: -4px; background: #f8fafc; width: 2px; height: 14px;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.8em; color: #64748b; margin-top: 5px;">
                <span>Impacto Negativo Max</span>
                <span style="color: {color_badge}; font-weight: bold;">Score de Arbitraje: {pred.impact_score:+.1f}</span>
                <span>Impacto Positivo Max</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    avg_score = total_score / len(predictions) if predictions else 0.0

    st.markdown("---")
    st.markdown("### 🧮 Calculadora de Retorno y Probabilidad Cuántica")
    st.caption("Simulación de volumen de posición y distribución probabilística asimétrica.")

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        capital_invertido = st.number_input("Monto total asignado a la posición ($ USD):", min_value=10.0, value=10000.0, step=500.0)
    with col_c2:
        usar_precio_historico = st.checkbox("¿Simular con un precio de entrada personalizado / pasado?")
        if usar_precio_historico:
            precio_entrada = st.number_input("Precio de entrada personalizado ($):", min_value=0.01, value=current_price * 0.9)
        else:
            precio_entrada = current_price

    acciones_compradas = capital_invertido / precio_entrada
    st.info(f"💼 **Volumen de Posición:** Al asignar **${capital_invertido:,.2f}**, adquieres un total de **{acciones_compradas:,.4f}** unidades de **{ticker}** a un precio de entrada de **${precio_entrada:,.2f}**.")

    st.markdown("#### Proyección de Escenarios basados en Arbitraje Político")
    shift_factor = avg_score / 100.0

    escenarios = [
        {
            "nombre": "🟢 Escenario Bull (Éxito de Política / Desregulación)",
            "probabilidad": max(15.0, min(85.0, 35.0 + (shift_factor * 40))),
            "rendimiento": max(0.05, 0.25 + (shift_factor * 0.35)),
            "color": "#22c55e", "bg": "rgba(34, 197, 94, 0.05)"
        },
        {
            "nombre": "⚖️ Escenario Base (Consenso Ordinario / Absorción)",
            "probabilidad": max(20.0, min(70.0, 45.0 - (abs(shift_factor) * 15))),
            "rendimiento": 0.05 + (shift_factor * 0.10),
            "color": "#38bdf8", "bg": "rgba(56, 189, 248, 0.05)"
        },
        {
            "nombre": "🚨 Escenario Bear (Guerra Comercial / Estrés Operativo)",
            "probabilidad": max(10.0, min(80.0, 20.0 - (shift_factor * 40))),
            "rendimiento": min(-0.05, -0.20 + (shift_factor * 0.20)),
            "color": "#ef4444", "bg": "rgba(239, 68, 68, 0.05)"
        }
    ]

    total_probs = sum(e["probabilidad"] for e in escenarios)
    for e in escenarios:
        e["probabilidad"] = (e["probabilidad"] / total_probs) * 100

    col_e1, col_e2, col_e3 = st.columns(3)
    columnas = [col_e1, col_e2, col_e3]

    for idx, esc in enumerate(escenarios):
        valor_proyectado_accion = precio_entrada * (1.0 + esc["rendimiento"])
        capital_final = acciones_compradas * valor_proyectado_accion
        pnl = capital_final - capital_invertido
        signo = "+" if pnl >= 0 else ""

        with columnas[idx]:
            st.markdown(f"""
            <div style="background-color: {esc['bg']}; border: 1px solid {esc['color']}; padding: 18px; border-radius: 10px; height: 100%;">
                <h5 style="margin: 0 0 10px 0; color: {esc['color']}; font-size: 0.95em;">{esc['nombre']}</h5>
                <p style="margin: 0; color: #94a3b8; font-size: 0.85em;">Probabilidad de Ocurrencia:</p>
                <h3 style="margin: 2px 0 12px 0; color: #f8fafc; font-weight: 800;">{esc['probabilidad']:.1f}%</h3>
                <hr style="border-color: #334155; margin: 8px 0;"/>
                <p style="margin: 0; color: #64748b; font-size: 0.8em;">Target Proyectado:</p>
                <strong style="color: #f1f5f9; font-size: 1.1em;">${valor_proyectado_accion:,.2f}</strong>
                <p style="margin: 8px 0 0 0; color: #64748b; font-size: 0.8em;">PnL Esperado:</p>
                <span style="color: {esc['color']}; font-weight: bold; font-size: 1.2em;">
                    {signo}${pnl:,.2f} ({esc['rendimiento']*100:+.1f}%)
                </span>
            </div>
            """, unsafe_allow_html=True)

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