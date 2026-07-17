# REEMPLAZA ESTA FUNCIÓN EN: presentation/components.py
from core.domains import TrumpPredictionResult
import streamlit as st
from typing import List

def render_trump_prediction_dashboard(ticker: str, predictions: List[TrumpPredictionResult], current_price: float) -> None:
    st.markdown(f"### 🦅 Trump Policy Arbitrage Matrix (`Trumprediction`)")
    st.write(f"Análisis cuantitativo crudo del impacto de la narrativa política y decretos sobre **{ticker}**:")
    
    # Sumatoria neta del score para alimentar la calculadora probabilística
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

    # Promedio del Score de Impacto de la Empresa
    avg_score = total_score / len(predictions) if predictions else 0.0

    st.markdown("---")
    st.markdown("### 🧮 Calculadora de Retorno y Probabilidad Cuántica")
    st.caption("Determina el tamaño de tu posición y simula retornos ponderados por riesgo geopolítico en tiempo real (2026).")

    # Controles de la Calculadora de Inversión
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        capital_invertido = st.number_input("Monto a Invertir / Invertido ($ USD):", min_value=10.0, value=10000.0, step=500.0)
    with col_c2:
        usar_precio_historico = st.checkbox("¿Simular con precio personalizado/pasado?")
        if usar_precio_historico:
            precio_entrada = st.number_input(f"Precio de Entrada Personalizado ($):", min_value=0.01, value=current_price * 0.9)
        else:
            precio_entrada = current_price

    # Cálculo de Acciones Adquiridas
    acciones_compradas = capital_invertido / precio_entrada
    
    st.info(f"**Volumen de Posición:** Con una inversión de **${capital_invertido:,.2f}**, adquieres un total de **{acciones_compradas:,.4f}** acciones de **{ticker}** (a un precio de entrada de **${precio_entrada:,.2f}**).")

    st.markdown("#### Proyección de Escenarios y Modelado de Probabilidad")
    
    # Lógica Algorítmica Ponderando el Score Político de Trump
    shift_factor = avg_score / 100.0

    escenarios = [
        {
            "nombre": "🟢 Escenario Bull (Desregulación / Éxito de Política)",
            "probabilidad": max(15.0, min(85.0, 35.0 + (shift_factor * 40))),
            "rendimiento": max(0.05, 0.25 + (shift_factor * 0.35)),
            "color": "#22c55e", "bg": "rgba(34, 197, 94, 0.05)"
        },
        {
            "nombre": "⚖️ Escenario Base (Consenso de Mercado / Absorción)",
            "probabilidad": max(20.0, min(70.0, 45.0 - (abs(shift_factor) * 15))),
            "rendimiento": 0.05 + (shift_factor * 0.10),
            "color": "#38bdf8", "bg": "rgba(56, 189, 248, 0.05)"
        },
        {
            "nombre": "🚨 Escenario Bear (Guerra Comercial / Stress de Márgenes)",
            "probabilidad": max(10.0, min(80.0, 20.0 - (shift_factor * 40))),
            "rendimiento": min(-0.05, -0.20 + (shift_factor * 0.20)),
            "color": "#ef4444", "bg": "rgba(239, 68, 68, 0.05)"
        }
    ]

    # Normalizar probabilidades para que sumen 100% exacto
    total_probs = sum(e["probabilidad"] for e in escenarios)
    for e in escenarios:
        e["probabilidad"] = (e["probabilidad"] / total_probs) * 100

    # Renderizado estético de las tarjetas de escenarios financieros
    col_e1, col_e2, col_e3 = st.columns(3)
    columnas = [col_e1, col_e2, col_e3]

    for idx, esc in enumerate(escenarios):
        valor_proyectado_accion = precio_entrada * (1.0 + esc["rendimiento"])
        capital_final_proyectado = acciones_compradas * valor_proyectado_accion
        pnl_neto = capital_final_proyectado - capital_invertido
        signo = "+" if pnl_neto >= 0 else ""

        with columnas[idx]:
            st.markdown(f"""
            <div style="background-color: {esc['bg']}; border: 1px solid {esc['color']}; padding: 18px; border-radius: 10px; height: 100%;">
                <h5 style="margin: 0 0 10px 0; color: {esc['color']}; font-size: 0.95em;">{esc['nombre']}</h5>
                <p style="margin: 0; color: #94a3b8; font-size: 0.85em;">Probabilidad Asignada:</p>
                <h3 style="margin: 2px 0 12px 0; color: #f8fafc; font-weight: 800;">{esc['probabilidad']:.1f}%</h3>
                <hr style="border-color: #334155; margin: 8px 0;"/>
                <p style="margin: 0; color: #64748b; font-size: 0.8em;">Precio Objetivo:</p>
                <strong style="color: #f1f5f9; font-size: 1.1em;">${valor_proyectado_accion:,.2f}</strong>
                <p style="margin: 8px 0 0 0; color: #64748b; font-size: 0.8em;">Retorno Estimado:</p>
                <span style="color: {esc['color']}; font-weight: bold; font-size: 1.2em;">
                    {signo}${pnl_neto:,.2f} ({esc['rendimiento']*100:+.1f}%)
                </span>
            </div>
            """, unsafe_allow_html=True)