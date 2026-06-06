import os
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()

client = OpenAI(
    api_key=os.getenv("CEREBRAS_API_KEY"),
    base_url="https://api.cerebras.ai/v1"
)

@app.get("/")
async def home():
    return {"status": "alive"}

@app.get("/chat")
async def chat(q: str):
    response = client.chat.completions.create(
        model="gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are Aayein AI."},
            {"role": "user", "content": q}
        ],
        max_tokens=200
    )

    return {"response": response.choices[0].message.content}
