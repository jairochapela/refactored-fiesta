from fastapi import FastAPI
from pydantic import BaseModel
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.checkpoint.postgres import PostgresSaver

import logging
import random
from tools import get_fecha_actual
import config

from llm import LLM
from agent import CustomAgent

app = FastAPI()
logging.basicConfig(level=logging.INFO)

with open("system_prompt.md", "r") as f:
    system_prompt = f.read()

# Crear la tabla de checkpoints si no existe
with PostgresSaver.from_conn_string(config.DB_URI) as checkpointer:
    checkpointer.setup()


class Question(BaseModel):
    question: str
    confirmation: list[bool] = []
    thread_id: str

@app.post("/ask")
def ask_question(question: Question):
    if not question.thread_id:
        question.thread_id = f"thread_{random.randint(1000000, 9999999)}"
    # Aquí puedes agregar la lógica para procesar la pregunta y generar una respuesta
    try:
        with PostgresSaver.from_conn_string(config.DB_URI) as checkpointer:
            agent = CustomAgent(
                model=LLM(),
                checkpointer=checkpointer,
                system_prompt=system_prompt,
                thread_id=question.thread_id
            )
            response, action_requests = agent.ask(question.question)
            logging.info(f"Pregunta: {question.question}. Respuesta: {response}.")
            return {"response": response, "action_requests": action_requests, "thread_id": question.thread_id}
        
    except Exception as e:
        logging.error(f"Error al procesar la pregunta: {e}")
        return {"error": str(e), "thread_id": question.thread_id}


@app.post("/confirm_action")
def confirm_action(question: Question):
    if not question.thread_id:
        return {"error": "No se proporcionó un thread_id para la confirmación."}
    
    try:
        with PostgresSaver.from_conn_string(config.DB_URI) as checkpointer:
            agent = CustomAgent(
                model=LLM(),
                checkpointer=checkpointer,
                system_prompt=system_prompt,
                thread_id=question.thread_id
            )

            agent.confirm_action(question.confirmation)
            logging.info(f"Acción confirmada: {question.confirmation} para el thread_id: {question.thread_id}.")
            return {"message": f"Entendido. Acción {'aprobada' if question.confirmation else 'rechazada'}.", "thread_id": question.thread_id}
        
    except Exception as e:
        logging.error(f"Error al confirmar la acción: {e}")
        return {"error": str(e), "thread_id": question.thread_id}