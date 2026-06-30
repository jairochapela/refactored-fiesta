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
            respuesta = response.json().get("response", "")
            action_requests = response.json().get("action_requests", [])
            st.session_state['thread_id'] = response.json().get("thread_id", st.session_state.get('thread_id', ''))
            st.markdown(respuesta)

            if action_requests:
                for action in action_requests:
                    st.markdown(f"**Action Request:** {action['description']}")
                st.button("Aprobar Acción", on_click=confirm_action, args=(len(action_requests) * [True],))
                st.button("Rechazar Acción", on_click=confirm_action, args=(len(action_requests) * [False],))

            st.session_state['mensajes'].append({"role": "assistant", "content": respuesta})


def confirm_action(approval: list[bool]):
    response = requests.post(
        "http://localhost:8000/confirm_action",
        json={"question": '', "confirmation": approval, "thread_id": st.session_state.get('thread_id', '')}
    )
    respuesta = response.json().get("response", "")

def sidebar():
    st.header("Sidebar")

if __name__ == "__main__":
    main()