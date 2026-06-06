from fastapi import FastAPI
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(
    api_key=os.getenv("CEREBRAS_API_KEY"),
    base_url="https://api.cerebras.ai/v1"
)

@app.get("/")
async def home():
    return {"status": "alive"}

@app.get("/test")
async def test():

    response = client.chat.completions.create(
        model=os.getenv("MODEL_NAME", "gpt-oss-120b"),
        messages=[
            {
                "role": "user",
                "content": "Say hello"
            }
        ]
    )

    return {
        "response": response.choices[0].message.content
    }
    
