import streamlit as st
from multiapp import MultiApp
from apps import markets, forecast, prediction, sentiment, portfolio
import pandas as pd
import sqlite3

# Objeto de la clase MultiApp()
main = MultiApp()

# Apps disponibles
main.add_app("Mercados financieros", markets.app)
main.add_app("Pronóstico largo plazo", forecast.app)
main.add_app("Predicción corto plazo", prediction.app)
main.add_app("Análisis de sentimiento", sentiment.app)
main.add_app("Optimizador de carteras", portfolio.app)

# Aplicación principal
st.image('logo.png')
st.sidebar.title('AI-INVESTOR')
main.run()

# Login
con = sqlite3.connect('users.sqlite3')
cur = cur = con.cursor()
user = st.sidebar.text_input('Usuario')
psw = st.sidebar.text_input('Contraseña', type= 'password')

if st.sidebar.button('Iniciar sesión'):
    statement = f"SELECT username from users WHERE username='{user}' AND Password = '{psw}';"
    cur.execute(statement)
    if not cur.fetchone():
        st.sidebar.write("Inicio de sesión fallido")
    else:
        st.sidebar.write("Sesión iniciada")
        
if st.sidebar.button('Registrarse'):
    cur.execute("INSERT INTO users VALUES (?, ?)", (user, psw))
    con.commit()
    
# Base de datos de los tickers disponibles para analizar
tickers = pd.read_csv("tickers.csv", delimiter=';')
tickers = tickers.set_index('Symbol')