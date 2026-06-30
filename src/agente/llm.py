from langchain.chat_models import init_chat_model
import config

__model = None

def LLM():
    global __model
    if not __model:
        __model = init_chat_model(
            model=config.MODEL_NAME,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS,
            api_key=config.API_KEY,
            streaming=False
        )
    return __model