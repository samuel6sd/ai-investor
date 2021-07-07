# Importar librerí­as
import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pypfopt import expected_returns
from pypfopt import risk_models
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

# Función de la app PORTFOLIO
def app():
    # Tí­tulo
    st.title('Optimizador de carteras')
    
    # Colección de tickers
    tickers = pd.read_csv("tickers.csv", delimiter=';')
    
    portfolio = st.multiselect('Selecciona los activos a incluir en la cartera', tickers['Symbol'])
    if not portfolio:
     st.warning('Por favor, selecciona al menos un ticker')
     st.stop()
    
    # Crear el dataframe con el precio de cierre ajustado de todas las acciones de la cartera
    df = pd.DataFrame()
    df = yf.download(portfolio, data_source='yahoo', start='2016-01-01')['Adj Close']
    
    # Visualizar comportamiento del precio de cada acción
    st.subheader('Comportamiento del precio de las acciones')
    st.line_chart(df, use_container_width=True)
    
    # Calcular retornos esperados anuales y matriz de covarianza
    mu = expected_returns.mean_historical_return(df, compounding=False) 
    S = risk_models.risk_matrix(df, method='sample_cov')
    
    # Visualizar matriz de correlación a partir de la matriz de covarianza
    st.subheader('Matriz de correlación')
    risk_models.cov_to_corr(S)
    fig1, ax1 = plt.subplots(figsize=(15,10)) 
    mat = np.triu(risk_models.cov_to_corr(S))
    sns.heatmap(risk_models.cov_to_corr(S), annot=True, linewidths=.5, ax=ax1, vmin=-1, vmax=1, center= 0, mask=mat)
    ax1.set_xticklabels(ax1.get_xticklabels(),rotation=45,horizontalalignment='right');
    st.pyplot(fig1)
    
    # Optimizar cartera
    ef = EfficientFrontier(mu, S)
    weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    cw = pd.DataFrame(cleaned_weights.values(), cleaned_weights.keys(), ['Pesos'])
    cw = cw.drop(cw[cw['Pesos'] <= 0].index)
    
    # Visualización de pesos optimizados
    st.subheader('Distribución óptima de los pesos')
    fig2 = plt.figure()
    ax2 = fig2.add_subplot()
    ax2.pie(cw['Pesos'], labels=cw.index, autopct='%1.1f%%', startangle=90)
    ax2.set_title('Participación de cada activo')
    st.pyplot(fig2)
    
    # Resultados del portafolio optimizado
    st.subheader('Performance de la cartera')
    performance = ef.portfolio_performance()
    ret = performance[0]*100
    volatility = performance[1]*100
    sharpe = performance[2]
    st.write(f'Retorno anual esperado: {ret.round(2)}%')
    st.write(f'Volatilidad anual: {volatility.round(2)}%')
    st.write(f'Sharpe ratio: {sharpe.round(2)}')
    
    
    # Seleccionar capital a invertir
    st.subheader('Configuración de cartera personal')
    capital = st.slider("Capital a invertir", 0, 1000000, step=1000)
    if capital == 0:
        st.stop()
        
    # Nº de acciones a comprar de cada compañí­a y dinero sobrante
    latest_prices = get_latest_prices(df)
    da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=capital)
    allocation, leftover = da.lp_portfolio()
    allocation = pd.DataFrame(data=allocation.values(), index=allocation.keys(), columns=['Nº de acciones'])
    
    # Resultados
    st.write('Composición de la cartera: ')
    st.write(allocation)
    st.write(f'Dinero restante: {leftover.round(2)}$')
    
