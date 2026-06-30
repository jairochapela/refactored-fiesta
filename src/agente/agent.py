from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

class CustomAgent:

    def __init__(self, model, checkpointer, system_prompt: str, thread_id: str):
        self.agent = create_agent(
            model=model,
            system_prompt=system_prompt,
            checkpointer=checkpointer
        )
        self.thread_id = thread_id

    def ask(self, question: str):
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
        return response['messages'][-1].content