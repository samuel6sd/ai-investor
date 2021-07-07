# Importar librerí­as
import streamlit as st
import yfinance as yf

# Función de la app MARKETS
def app():
    
    # Tí­tulo y descripción
    st.title('Mercados financieros')
    st.write('Desde la página de mercados financieros puedes echar un vistazo a los diferentes activos que están disponibles.')
    
    # Selección de mercado
    market = st.selectbox('Mercados', ('Índices', 'Materias primas', 'Divisas', 'Criptomonedas'))
    
    # Función para mostrar toda la información de un activo
    def show(sym, act):
        data = yf.download(sym, '2000-01-01')
        d = data.set_index(data.index.strftime("%Y-%m-%d"))
        d = d.drop('Adj Close', 1)
        st.header(act)
        st.line_chart(data['Close'])
        st.subheader('Datos históricos')
        st.write(d)
    
    if (market == 'Índices'):
        ind = st.radio('Selecciona el activo a mostrar', ('S&P 500', 'Nasdaq', 'Dow Jones', 'Euro Stoxx 50', 'Ibex 35', 'DAX', 'Nikkei 225'))
        if (ind == 'S&P 500'):
            show('^GSPC', ind)
        elif (ind == 'Nasdaq'):   
            show('^IXIC', ind)

    elif (market == 'Materias primas'):
        mat = st.radio('Selecciona el activo a mostrar', ('Oro', 'Plata', 'Cobre', 'Petróleo'))
        if (mat == 'Oro'):
            show('GC=F', mat)
        elif (mat == 'Plata'):   
            show('SI=F', mat)
            
    elif (market == 'Divisas'):
        div = st.radio('Selecciona el activo a mostrar', ('EUR-USD', 'USD-JPY', 'USD-CHF', 'USD-CAD', 'GBP-USD', 'AUD-USD'))
        if (div == 'EUR-USD'):   
            show('EURUSD=X', div)
        elif (div == 'USD-JPY'):   
            show('USDJPY=X', div)
    
    elif (market == 'Criptomonedas'):
        cripto = st.radio('Selecciona el activo a mostrar', ('BTC', 'ETH', 'USDT', 'BNB', 'ADA', 'XRP', 'DOGE', 'DOT'))
        if (cripto == 'BTC'):   
            show('BTC-USD', cripto)
        elif (cripto == 'ETH'):   
            show('ETH-USD', cripto)