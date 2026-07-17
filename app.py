import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Estilos CSS mejorados
st.markdown("""
<style>
    .prediction-box { padding: 20px; border-radius: 10px; background-color: #0f172a; border: 2px solid #38bdf8; text-align: center; }
</style>
""", unsafe_allow_html=True)

# Lógica del Motor Predictivo (IA Básica de Sentimiento)
def calcular_prediccion(ticker, noticias, insider_data):
    score = 0
    # Análisis de sentimiento muy básico basado en palabras clave en noticias
    palabras_pos = ['growth', 'profit', 'buy', 'upgrade', 'innovation', 'approval', 'record']
    palabras_neg = ['lawsuit', 'loss', 'downgrade', 'risk', 'regulatory', 'investigation', 'declining']
    
    for n in noticias:
        titulo = n.get('title', '').lower()
        if any(word in titulo for word in palabras_pos): score += 0.2
        if any(word in titulo for word in palabras_neg): score -= 0.2
    
    # Peso extra por compras de directivos (Insider Trading)
    if insider_data is not None and not insider_data.empty:
        score += 0.4
    
    # Normalizar score entre -1 y 1
    score = max(min(score, 1), -1)
    
    if score > 0.3: return "Alcista (Posible Subida)", "green", score * 100
    elif score < -0.3: return "Bajista (Posible Bajada)", "red", score * 100
    else: return "Neutro (Consolidación)", "gray", score * 100

# Interfaz en Streamlit
st.title("🔮 Motor Predictivo Intersector")
ticker = st.text_input("Ingresa el Ticker:", "NVDA").upper()

if ticker:
    empresa = yf.Ticker(ticker)
    noticias = empresa.news
    insiders = empresa.insider_transactions
    
    # Llamada al motor
    prediccion, color, porcentaje = calcular_prediccion(ticker, noticias, insiders)
    
    st.markdown(f"""
    <div class="prediction-box">
        <h3>Resultado del Motor: <span style="color:{color};">{prediccion}</span></h3>
        <p>Confianza estadística basada en narrativa: {abs(porcentaje):.1f}%</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("📰 Narrativa Política y Financiera")
    # Filtro: Solo mostrar noticias que mencionen la empresa o política sectorial
    for n in noticias[:5]:
        st.markdown(f"- **{n.get('title')}** | Fuente: *{n.get('publisher')}*")