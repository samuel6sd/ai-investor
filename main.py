# Importar librer�as
import streamlit as st
from multiapp import MultiApp
from apps import markets, forecast, prediction, sentiment, portfolio
import pandas as pd
import sqlite3

# Objeto de la clase MultiApp()
main = MultiApp()

# Apps disponibles
main.add_app("Mercados financieros", markets.app)
main.add_app("Pron�stico largo plazo", forecast.app)
main.add_app("Predicci�n corto plazo", prediction.app)
main.add_app("Análisis de sentimiento", sentiment.app)
main.add_app("Optimizador de carteras", portfolio.app)

# Logo título y llamada ejecuci�n de la aplicaci�n seleccionada
st.image('logo.png')
st.sidebar.title('AI-INVESTOR')
main.run()

# Conexi�n con la base de datos users
con = sqlite3.connect('users.sqlite3')
cur = cur = con.cursor()

# Formulario de login
user = st.sidebar.text_input('Usuario')
psw = st.sidebar.text_input('Contrase�a', type= 'password')
# Inicio de sesi�n
if st.sidebar.button('Iniciar sesi�n'):
    statement = f"SELECT username from users WHERE username='{user}' AND Password = '{psw}';"
    cur.execute(statement)
    if not cur.fetchone():
        st.sidebar.write("Inicio de sesi�n fallido")
    else:
        st.sidebar.write("Sesi�n iniciada")
# Registro        
if st.sidebar.button('Registrarse'):
    cur.execute("INSERT INTO users VALUES (?, ?)", (user, psw))
    con.commit()
    
# Base de datos de los tickers disponibles
tickers = pd.read_csv("tickers.csv", delimiter=';')
tickers = tickers.set_index('Symbol')