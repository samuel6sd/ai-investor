import streamlit as st
from multiapp import MultiApp
from apps import markets, forecast, prediction, sentiment, portfolio
import pandas as pd

main = MultiApp()

# Apps disponibles
main.add_app("Mercados financieros", markets.app)
main.add_app("Pronóstico largo plazo", forecast.app)
main.add_app("Predicción corto plazo", prediction.app)
main.add_app("Análisis de sentimiento", sentiment.app)
main.add_app("Optimizador de carteras", portfolio.app)

# Aplicación principal
st.sidebar.title('AINVESTOR')
main.run()

# Base de datos de los tickers disponibles para analizar
tickers = pd.read_csv("tickers.csv", delimiter=';')
tickers = tickers.set_index('Symbol')