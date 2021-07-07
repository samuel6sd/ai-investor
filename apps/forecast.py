# Importar librer�as
import streamlit as st
import pandas as pd
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly

# Funci�n de la app FORECAST
def app():
    # Colecci�n de tickers
    tickers = pd.read_csv("tickers.csv", delimiter=';')
    tickers = tickers.set_index('Symbol')
    
    # T�tulo
    st.title('Pron�stico a largo plazo del precio de un activo')
    
    # Seleccionar activo
    ticker = st.selectbox('Ticker', tickers.index)
    if ticker == ' ':
     st.warning('Por favor, selecciona un ticker')
     st.stop()
    com = tickers.loc[ticker,'Name']
    
    # Obtener y visualizar datos hist�ricos de la acci�n seleccionada
    data = yf.download(ticker, start="2015-01-01")
    # Gr�fico
    st.subheader('Precio de cierre de ' + com)
    st.line_chart(data['Close'], use_container_width=True)
    data['Date'] = data.index.strftime("%Y-%m-%d")
    df = data.set_index('Date')  
    # Datos
    st.subheader('Datos hist�ricos de ' + com)
    st.write(df)
    df['Date'] = data.index

    # PRONӓSTICO LARGO PLAZO
    st.subheader('Pron�stico a largo plazo del precio de ' + com)
    
    # Seleccionar los a�os para el pron�stico
    years = st.slider('Años a predecir:', 1, 5)
    period = years*365
    
    # Modificar dataset para que coincida con el m�dulo Prophet
    df = data[["Date","Close"]]
    df = df.rename(columns={"Date": "ds", "Close": "y"})
    
    # Crear el modelo y ajustarlo a los datos
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)
    st.success(f'Pron�stico ajustado para los pr�ximos {years} a�o/s:')
    
    # Mostrar pron�stico
    fig2 = plot_plotly(m, forecast, xlabel='Fecha', ylabel='Precio')
    st.plotly_chart(fig2, True)
    # Mostrar componentes del pron�stico
    st.subheader("Componentes del pron�stico")
    fig3 = m.plot_components(forecast)
    st.write(fig3)
    
    
    
