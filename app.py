import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Título de la página web
st.title("👁️ Rastreador de Movimientos de CEOs")
st.write("Mira lo que los altos mandos están comprando o vendiendo en tiempo real.")

# 2. Buscador en pantalla
ticker = st.text_input("Escribe las siglas de la empresa (Ejemplo: NVDA, AAPL, MSFT):", "NVDA").upper()

# 3. Lógica para buscar los datos
if ticker:
    st.subheader(f"Movimientos recientes para: {ticker}")
    
    try:
        empresa = yf.Ticker(ticker)
        df = empresa.insider_transactions
        
        if df is not None and not df.empty:
            # Seleccionamos solo las columnas más importantes para limpiar la vista
            columnas_importantes = ['Shares', 'Value', 'Text', 'Insider', 'Position']
            columnas_validas = [c for c in columnas_importantes if c in df.columns]
            
            df_mostrar = df[columnas_validas]
            
            # Dibujamos la tabla en la página web
            st.dataframe(df_mostrar, use_container_width=True)
            
            # Alerta si detectamos compras de acciones
            compras = df_mostrar[df_mostrar['Text'].str.contains('Buy|Purchase', case=False, na=False)]
            if not compras.empty:
                st.success(f"🔥 ¡Atención! Se detectaron compras de acciones por parte de los directivos.")
            else:
                st.info("Los movimientos recientes parecen ser ventas rutinarias u opciones de acciones.")
                
        else:
            st.warning("No se encontraron transacciones recientes de directivos para esta empresa.")
            
    except Exception as e:
        st.error(f"Hubo un error al buscar el ticker {ticker}. Asegúrate de que exista en la bolsa. Error: {e}")