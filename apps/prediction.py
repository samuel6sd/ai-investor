# Importar librerí­as
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from keras.models import Model
from keras.layers import Dense, Dropout, LSTM, Input, Activation, concatenate
from keras import optimizers

# Función de la app PREDICTION
def app():
    # Colección de tickers
    tickers = pd.read_csv("tickers.csv", delimiter=';')
    tickers = tickers.set_index('Symbol')
    
    # Tí­tulo
    st.title('Pronóstico a corto plazo del precio de un activo')
    
    # Seleccionar activo
    ticker = st.selectbox('Ticker', tickers.index)
    if ticker == ' ':
     st.warning('Por favor, selecciona un ticker')
     st.stop()
    com = tickers.loc[ticker,'Name']
    
    # Obtener y visualizar datos históricos de la acción seleccionada
    data = yf.download(ticker, start="2016-01-01")
    # Gráfico
    st.subheader('Precio de cierre de ' + com)
    mes = data['Close'].tail(365)
    st.line_chart(mes, use_container_width=True)
    data['Date'] = data.index.strftime("%Y-%m-%d")
    df = data.set_index('Date')  
    # Datos
    st.subheader('Datos de los últimos 60 dí­as de ' + com)
    st.write(df.tail(60))
    df['Date'] = data.index
        
    # Preparar los datos
    df = df[['Close', 'Open', 'High', 'Low']]
    
    # Escalar los datos (sc para el conjunto de entrenamiento y price_sc para la predicción)
    close = np.array(df['Close']).reshape(-1, 1)
    train_sc = MinMaxScaler()
    price_sc = MinMaxScaler()
    price_sc.fit(close)
    df_train = train_sc.fit_transform(df)
    
    # X1 : Datos (Close, Open, High, Low) - 60 valores predicen el siguiente
    x1_train = np.array([df_train[i : i + 60].copy() for i in range(len(df_train) - 60)])
    
    # X2 : Media del precio de cierre para una ventana de 60 dí­as
    x2_train = []
    for h in x1_train:
      sma = np.mean(h[:,0])
      x2_train.append(np.array([sma]))
    x2_train = np.array(x2_train)
    
    # Y : Valores a predecir ; close
    y_train = np.array([df_train[:,0][i + 60].copy() for i in range(len(df_train) - 60)])
    
    # Comprobar que todos los conjuntos tienen el mismo nº de filas
    assert x1_train.shape[0] == x2_train.shape[0] == y_train.shape[0]
    
    # Definir el formato de las dos entradas de la red neuronal
    lstm_input = Input(shape=(x1_train.shape[1], x1_train.shape[2]))
    dense_input = Input(shape=(x2_train.shape[1],))
    
    # Primera rama
    x1 = LSTM(50)(lstm_input)
    x1 = Dropout(0.2)(x1)
    lstm_branch = Model(inputs=lstm_input, outputs=x1)
    
    # Segunda rama
    x2 = Dense(20)(dense_input)
    x2 = Activation("relu")(x2)
    x2 = Dropout(0.2)(x2)
    tech_ind_branch = Model(inputs=dense_input, outputs=x2)
    
    # Combinar ramas
    comb = concatenate([lstm_branch.output, tech_ind_branch.output])
    y = Dense(64, activation="sigmoid")(comb)
    y = Dense(1, activation="linear")(y)
    
    # Compilar y entrenar el modelo
    model = Model(inputs=[lstm_branch.input, tech_ind_branch.input], outputs=y)
    opt = optimizers.Adam(lr=0.0005)
    model.compile(optimizer=opt, loss='mse')
    model.fit(x=[x1_train, x2_train], y=y_train, batch_size=32, epochs=50, shuffle=True)
    st.success('Modelo entrenado')
    
    # Se realiza una predicción para el dí­a actual y el dí­a siguiente
    # Esto permitirá comparar las predicciones y clasificar el movimiento del precio
    df_pred = df_train[len(df_train)-61:, :]
    x1_pred = np.array([df_pred[i : i + 60].copy() for i in range(2)])
    x2_pred = []
    for h in x1_pred:
      sma = np.mean(h[:,0])
      x2_pred.append(np.array([sma]))
    x2_pred = np.array(x2_pred)
    
    fut = model.predict([x1_pred, x2_pred])
    fut = price_sc.inverse_transform(fut)
    
    # Previsión de si el precio va a subir o a bajar en función a los 60 últimos dí­as
    dif = ((fut[-1] - fut[-2]) / fut[-2]) * 100
    if fut[-1] > fut[-2]:
      st.markdown(f'_El modelo predice que el precio subirá mañana {dif.round(2)}%_')
    else:
      st.markdown(f'_El modelo predice que el precio bajará mañana {dif.round(2)}%_')

