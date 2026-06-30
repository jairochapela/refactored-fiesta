from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from tools import get_fecha_actual, agregar_evento_calendario, listar_eventos_calendario, eliminar_evento_calendario

class CustomAgent:

    def __init__(self, model, checkpointer, system_prompt: str, thread_id: str):
        self.agent = create_agent(
            model=model,
            system_prompt=system_prompt,
            checkpointer=checkpointer,
            tools=[
                get_fecha_actual,
                agregar_evento_calendario,
                listar_eventos_calendario,
                eliminar_evento_calendario
            ],
            middleware=[
                HumanInTheLoopMiddleware(
                    interrupt_on={"eliminar_evento_calendario": {"allowed_decisions": ["approve", "reject"]}}
                )
            ],
        )
        self.thread_id = thread_id

    def ask(self, question: str) -> tuple[str, list[dict]]:
        response = self.agent.invoke(
            input={
                "messages": [HumanMessage(content=question)]
            },
            config={
                "configurable": {
                    "thread_id": self.thread_id
                }
            }
        )
        action_requests = []
        interrupciones = response.get('__interrupt__', [])
        for interrupcion in interrupciones:
            print(interrupcion)
            action_requests += interrupcion.value.get('action_requests', [])
        return response['messages'][-1].content, action_requests
    
    def confirm_action(self, confirmation: list[bool]) -> str:
        decision = ["approve" if c else "reject" for c in confirmation]
        response = self.agent.invoke(
            Command(resume={"decisions": [{"type": d} for d in decision]}),
            config={
                "configurable": {
                    "thread_id": self.thread_id
                }
            }
        )
        return response['messages'][-1].content
