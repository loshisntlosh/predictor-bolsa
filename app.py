import streamlit as st
import yfinance as yf
import pandas as pd

# Configuración de la página de Streamlit
st.set_page_config(layout="wide") # Esto hace que la web aproveche toda la pantalla

st.title("👁️ El Intersector: Radar de Altos Mandos y Noticias")
st.write("Cruzando transacciones de insiders con la actualidad informativa del sector.")

# Buscador en pantalla
ticker = st.text_input("Escribe el Ticker de la empresa a investigar (Ejemplo: NVDA, AAPL, MSFT, LLY):", "NVDA").upper()

if ticker:
    # Creamos dos columnas en la web para comparar cara a cara
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💼 Movimientos de los Altos Mandos (SEC)")
        try:
            empresa = yf.Ticker(ticker)
            df = empresa.insider_transactions
            
            if df is not None and not df.empty:
                columnas_importantes = ['Shares', 'Value', 'Text', 'Insider', 'Position']
                columnas_validas = [c for c in columnas_importantes if c in df.columns]
                df_mostrar = df[columnas_validas]
                
                # Mostramos la tabla de directivos
                st.dataframe(df_mostrar, use_container_width=True, height=400)
                
                # Alerta inteligente
                compras = df_mostrar[df_mostrar['Text'].str.contains('Buy|Purchase', case=False, na=False)]
                if not compras.empty:
                    st.success(f"🔥 ¡Atención! Se detectaron compras de acciones recientes por directivos.")
                else:
                    st.info("Los movimientos recientes parecen ser ventas o compensaciones rutinarias.")
            else:
                st.warning("No se encontraron transacciones recientes de directivos.")
        except Exception as e:
            st.error(f"Error al cargar transacciones: {e}")

    with col2:
        st.subheader("📰 Últimas Noticias del Sector")
        try:
            empresa = yf.Ticker(ticker)
            # Extraemos las noticias financieras más recientes que Yahoo recopila gratis
            noticias = empresa.news
            
            if noticias:
                # Recorremos las últimas 5 noticias y las mostramos de forma bonita
                for noticia in noticias[:5]:
                    titulo = noticia.get('title', 'Sin título')
                    fuente = noticia.get('publisher', 'Fuente desconocida')
                    enlace = noticia.get('link', '#')
                    
                    # Dibujamos una tarjeta visual para cada noticia
                    st.markdown(f"""
                    <div style="padding:10px; border-radius:5px; background-color:#1e293b; margin-bottom:10px;">
                        <h4 style="margin:0;"><a href="{enlace}" target="_blank" style="text-decoration:none; color:#38bdf8;">{titulo}</a></h4>
                        <p style="margin:5px 0 0 0; font-size:0.8em; color:#94a3b8;">Fuente: {fuente}</p>
                    </div>
                    """, unsafe_allow_lines=True, unsafe_allow_html=True)
            else:
                st.warning("No se encontraron noticias recientes para esta empresa.")
        except Exception as e:
            st.error(f"Error al cargar noticias: {e}")