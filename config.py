import os

CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
API_SECRET = os.getenv("API_SECRET")
MONGO_URL = os.getenv("MONGO_URL")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-oss-120b")
