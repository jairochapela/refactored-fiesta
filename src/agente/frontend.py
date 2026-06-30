import streamlit as st
import requests

def main():
    if 'mensajes' not in st.session_state:
        st.session_state['mensajes'] = []

    st.title("Agente IA")
    st.write("Bienvenido a la aplicación de Agente IA. Esta aplicación permite interactuar con un agente de inteligencia artificial para realizar diversas tareas.")

    with st.sidebar:
        sidebar()

    for mensaje in st.session_state['mensajes']:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

    if question := st.chat_input("Pregunta al agente IA..."):
        with st.chat_message("user"):
            st.markdown(question)
            st.session_state['mensajes'].append({"role": "user", "content": question})

        with st.chat_message("assistant"):
            response = requests.post(
                "http://localhost:8000/ask",
                json={"question": question, "thread_id": st.session_state.get('thread_id', '')}
            )
            respuesta = response.json()["response"]
            st.session_state['thread_id'] = response.json().get("thread_id", st.session_state.get('thread_id', ''))
            st.markdown(respuesta)
            st.session_state['mensajes'].append({"role": "assistant", "content": respuesta})

def sidebar():
    st.header("Sidebar")

if __name__ == "__main__":
    main()