import groq
import streamlit as st

Modelos = ['llama3-8b-8192', 'llama3-70b-8192','mixtral-8x7b-32768']

#Configurar pagina
def configurar_pagina():
   st.set_page_config(page_title="Chatbot con py", page_icon='😎')
   st.title('Bienvenido a mi chatbot')

#Mostrar el side bar con los modelos
def mostrar_sidebar():
    st.sidebar.title('Elegi tu modelo favorito')
    modelo = st.sidebar.selectbox('¿Cual Elejis?', Modelos)
    st.sidebar.write(f'**Elegiste el modelo** : {modelo}')
    return modelo

#Un Cliente groq
def Crear_cliente_groq():
    groq_api_key = st.secrets['GROQ_API_KEY']
    return groq.Groq(api_key=groq_api_key)

#Inicializa el estado del mensaje
def inicializacion_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

# Historial del chat
def mostrar_historial_chat():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

#Mostrar mensajes previos
def obtener_mensajes_previos():
    for mensaje in st.session_state.mensajes: 
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

#Obtener el mensaje del usuario
def obtener_mensaje_usuario():
    return st.chat_input("Envia un mensaje")

#Guardar msg
def agregar_mensajes_previos(role, content):
    st.session_state.mensajes.append({"role": role , "content": content})

#Mostrar los msg en pantalla
def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)

#Llamar al modelo de groq
def obtener_respuesta_modelo(cliente, modelo, mensajes):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        stream = False
    )
    return respuesta.choices[0].message.content

def ejecutar_chat():
    configurar_pagina()
    cliente = Crear_cliente_groq()
    modelo = mostrar_sidebar()
    inicializacion_estado_chat()
    mensaje_usuario = obtener_mensaje_usuario()
    obtener_mensajes_previos()

    
    if mensaje_usuario:
        agregar_mensajes_previos('user', mensaje_usuario)
        mostrar_mensaje('user', mensaje_usuario)

        mensaje_modelo = obtener_respuesta_modelo(cliente,modelo,st.session_state.mensajes)

        agregar_mensajes_previos('assistant', mensaje_modelo)
        mostrar_mensaje('assistant', mensaje_modelo)
        
if __name__ == '__main__':
    ejecutar_chat()
