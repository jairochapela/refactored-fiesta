from fastapi import FastAPI
from pydantic import BaseModel
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.checkpoint.postgres import PostgresSaver
import logging
import random
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
    thread_id: str

@app.post("/ask")
def ask_question(question: Question):
    if not question.thread_id:
        question.thread_id = f"thread_{random.randint(1000000, 9999999)}"
    # Aquí puedes agregar la lógica para procesar la pregunta y generar una respuesta
    with PostgresSaver.from_conn_string(config.DB_URI) as checkpointer:
        agent = CustomAgent(
            model=LLM(),
            checkpointer=checkpointer,
            system_prompt=system_prompt,
            thread_id=question.thread_id
        )
        response = agent.ask(question.question)
        logging.info(f"Pregunta: {question.question}. Respuesta: {response}.")
        return {"response": response, "thread_id": question.thread_id}
