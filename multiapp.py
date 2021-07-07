# Importar librer�as
import streamlit as st

# Clase que ejecuta varias aplicaciones
class MultiApp:
    
    # Se crea un array donde se almacenar� el t�tulo y la funci�n de cada app
    def __init__(self):
        self.apps = []
    
    # Funci�n para a�adir apps al array     
    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })
        
    # Funci�n que ejecuta la app seleccionada mediante el selectbox    
    def run(self):
        app = st.sidebar.selectbox('Apps', self.apps, format_func=lambda app: app['title'], )
        app['function']()
