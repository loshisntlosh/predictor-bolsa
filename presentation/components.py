import streamlit as st
from typing import List
from core.domains import QuantAssessment, CatalystEvent

def render_injection_styles() -> None:
    st.markdown("""
    <style>
        .main-title { color: #f8fafc; font-weight: 800; }
        .prediction-box { padding: 25px; border-radius: 12px; text-align: center; margin-bottom: 25px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3); }
        .scenario-card { padding: 20px; border-radius: 12px; background-color: #0f172a; border: 1px solid #334155; height: 100%; }
        .catalyst-badge { padding: 6px 12px; border-radius: 6px; font-size: 0.85em; font-weight: bold; display: inline-block; margin-bottom: 8px; }
        .timeline-container { border-left: 3px solid #334155; padding-left: 20px; margin-left: 10px; margin-top: 15px; }
        .timeline-item { position: relative; margin-bottom: 25px; }
        .timeline-dot { position: absolute; left: -26px; top: 5px; width: 10px; height: 10px; border-radius: 50%; }
    </style>
    """, unsafe_allow_html=True)

def render_assessment_card(assessment: QuantAssessment) -> None:
    st.markdown(f"""
    <div class="prediction-box" style="background: linear-gradient(135deg, #0f172a 0%, #020617 100%); border: 2px solid {assessment.hex_color};">
        <h2 style="margin:0; font-size:1.8em; color:#f8fafc;">Veredicto de la IA: <span style="color:{assessment.hex_color};">{assessment.verdict}</span></h2>
        <p style="margin:10px 0 0 0; color:#94a3b8; font-size:1.1em;">Convicción Cuantitativa Neta: <b>{assessment.confidence_score:.1f}%</b></p>
    </div>
    """, unsafe_allow_html=True)

def render_timeline(catalysts: List[CatalystEvent]) -> None:
    if not catalysts:
        st.info("No se registran eventos temporales anómalos para el ciclo operativo en curso.")
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

from core.domains import MacroShockResult

def render_stress_testing_dashboard(shocks: List[MacroShockResult]) -> None:
    st.write("Simulación algorítmica de shocks sistémicos basados en la estructura de capital actual del activo:")
    
    col1, col2 = st.columns(2)
    for idx, shock in enumerate(shocks):
        target_col = col1 if idx % 2 == 0 else col2
        
        color_alert = "#ef4444" if shock.risk_level == "EXTREME" else ("#f59e0b" if shock.risk_level == "ELEVATED" else "#22c55e")
        
        with target_col:
            st.markdown(f"""
            <div class="scenario-card" style="border-left: 5px solid {color_alert}; margin-bottom: 15px;">
                <h4 style="margin:0; color:#f8fafc;">{shock.scenario_name}</h4>
                <p style="margin:5px 0; font-size:0.85em; color:#94a3b8;">Nivel de Riesgo Corporativo: <b style="color:{color_alert};">{shock.risk_level}</b></p>
                <hr style="border-color:#334155; margin:10px 0;">
                <div style="display:flex; justify-content:space-between;">
                    <span>Precio Proyectado bajo Stress:</span>
                    <b style="color:#f8fafc;">${shock.projected_price:,.2f}</b>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:0.9em; margin-top:5px;">
                    <span>Índice de Vulnerabilidad:</span>
                    <span style="color:#cbd5e1;">{shock.vulnerability_index:.1f} / 100</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
