import configparser

config = configparser.ConfigParser()
config.read("config.ini")

MODEL_NAME = config.get("llm", "model_name")
TEMPERATURE = config.getfloat("llm", "temperature")
MAX_TOKENS = config.getint("llm", "max_tokens")
API_KEY = config.get("llm", "api_key")
DB_URI = config.get("database", "db_uri")
