# Importar librerí­as
import streamlit as st
import pandas as pd
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly

# Función de la app FORECAST
def app():
    # Colección de tickers
    tickers = pd.read_csv("tickers.csv", delimiter=';')
    tickers = tickers.set_index('Symbol')
    
    # Tí­tulo
    st.title('Pronóstico a largo plazo del precio de un activo')
    
    # Seleccionar activo
    ticker = st.selectbox('Ticker', tickers.index)
    if ticker == ' ':
     st.warning('Por favor, selecciona un ticker')
     st.stop()
    com = tickers.loc[ticker,'Name']
    
    # Obtener y visualizar datos históricos de la acción seleccionada
    data = yf.download(ticker, start="2015-01-01")
    # Gráfico
    st.subheader('Precio de cierre de ' + com)
    st.line_chart(data['Close'], use_container_width=True)
    data['Date'] = data.index.strftime("%Y-%m-%d")
    df = data.set_index('Date')  
    # Datos
    st.subheader('Datos históricos de ' + com)
    st.write(df)
    df['Date'] = data.index

    # PRONÓ“STICO LARGO PLAZO
    st.subheader('Pronóstico a largo plazo del precio de ' + com)
    
    # Seleccionar los años para el pronóstico
    years = st.slider('AÃ±os a predecir:', 1, 5)
    period = years*365
    
    # Modificar dataset para que coincida con el módulo Prophet
    df = data[["Date","Close"]]
    df = df.rename(columns={"Date": "ds", "Close": "y"})
    
    # Crear el modelo y ajustarlo a los datos
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)
    st.success(f'Pronóstico ajustado para los próximos {years} año/s:')
    
    # Mostrar pronóstico
    fig2 = plot_plotly(m, forecast, xlabel='Fecha', ylabel='Precio')
    st.plotly_chart(fig2, True)
    # Mostrar componentes del pronóstico
    st.subheader("Componentes del pronóstico")
    fig3 = m.plot_components(forecast)
    st.write(fig3)
    
    
    
