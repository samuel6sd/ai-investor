# Importar librerí­as
import streamlit as st
import tweepy, re
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# Función de la app SENTIMENT
def app():
    # Tí­tulo
    st.title('Análisis de sentimiento')
    
    ticker = st.text_input('Término')
    if ticker == '':
     st.warning('Por favor, selecciona un término')
     st.stop()
    
    # Claves de acceso para la API de twitter
    consumerKey = 'f0y99pKjB4x2SNBHtK5fiD4IB'
    consumerSecret = 'jJXTcEuriPbjEzDvrBsXQ3eBeAOl2oqKaiwoUlhpRKPzHbcyAu'
    accessToken = '1350780188142039041-3NZlpno82LwUqlxL1SFTrHwzLs9luY'
    accessTokenSecret = 'B3KCfjNhCUR5glKMdqkK9Sjp5CEIOxGEBxQ4yJfkPMD4h'
    
    # Autenticar el acceso a la API
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    # Seleccionar fechas
    start = st.date_input("Selecciona la fecha de inicio")
    st.write("Se recopilarán los tweets con más repercusión desde la fecha de inicio hasta hoy.")
    
    # Obtener n tweets relacionados con term y filtrar por nº de RT
    term = '#'+ ticker + ' -filter:retweets'
    get_tweets = tweepy.Cursor(api.search, q=term, lang = "en", since=start, tweet_mode='extended').items(100)
    tweets = [tweet.full_text for tweet in get_tweets]
    df = pd.DataFrame(tweets, columns=['Tweets'])
    
    # Función para formatear los tweets
    def cleanTwt(twt):
      twt = re.sub('#'+ticker, ticker, twt) # Eliminar '#' del ticker
      twt = re.sub('#[A-Za-z0-9]+', '', twt) # Eliminar cualquier otro '#'
      twt = re.sub('\\n', '', twt) # Eliminar los '\n'
      twt = re.sub('https?:\/\/.*[\r\n]*', '', twt, flags=re.MULTILINE) # Eliminar hyperlinks
      return twt
    
    # Se crea una lista con los tweets formateados
    df['Cleaned_Tweets'] = df['Tweets'].apply(cleanTwt)
    
    # Función para obtener la subjetividad
    def getSub(twt):
      return TextBlob(twt).sentiment.subjectivity
    # Función para obtener la polaridad
    def getPol(twt):
      return TextBlob(twt).sentiment.polarity
    
    # Crear las columnas Subjetividad y Polaridad
    df['Subjectivity'] = df['Cleaned_Tweets'].apply(getSub)
    df['Polarity']  = df['Cleaned_Tweets'].apply(getPol)
    
    # Función para clasificar tweets en base a su sentimiento
    def getSen(pol):
      if pol == 0:
        return 'Neutral'
      elif (pol < -0.5):
        return 'Muy Negativo'   
      elif (pol < 0 and pol > -0.5):
        return 'Negativo'  
      elif (pol > 0 and pol < 0.5):
        return 'Positivo' 
      elif (pol > 0.5):
        return 'Muy Positivo'     
    
    # Crear la columna de sentimiento
    df['Sentiment'] = df['Polarity'].apply(getSen)   
    
    # Gráfico de puntos para mostrar subjetividad y polaridad
    fig1 = plt.figure()
    ax1 = fig1.add_subplot()
    for i in range(0, df.shape[0]):
      ax1.scatter(df['Polarity'][i], df['Subjectivity'][i], color='blue')
    ax1.set_title('Análisis de subjetividad / polaridad')
    ax1.set_xlabel('Polaridad')
    ax1.set_ylabel('Subjetividad')
    st.pyplot(fig1)
    
    # Gráfico de barras
    count = df['Sentiment'].value_counts()
    st.bar_chart(count)
    st.write(count)