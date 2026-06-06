import time

from fastapi import FastAPI, HTTPException
from openai import OpenAI

from config import (
    API_SECRET,
    CEREBRAS_API_KEY,
    MODEL_NAME,
)
from database import conversations, stats
from schemas import ChatRequest, ClearRequest

app = FastAPI()

client = OpenAI(
    api_key=CEREBRAS_API_KEY,
    base_url="https://api.cerebras.ai/v1"
)

COOLDOWNS = {}


@app.get("/")
async def home():
    return {"status": "alive"}


@app.get("/stats")
async def get_stats():

    users = await conversations.count_documents({})

    total = await stats.find_one({"_id": "global"}) or {
        "messages": 0
    }

    return {
        "users": users,
        "messages": total.get("messages", 0)
    }


@app.post("/clear")
async def clear_memory(data: ClearRequest):

    if data.api_key != API_SECRET:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    memory_id = f"{data.chat_id}_{data.user_id}"

    await conversations.delete_one(
        {"memory_id": memory_id}
    )

    return {
        "status": "cleared"
    }


@app.post("/chat")
async def chat(data: ChatRequest):

    if data.api_key != API_SECRET:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    if len(data.message) > 2000:
        raise HTTPException(
            status_code=400,
            detail="Message too long"
        )

    memory_id = f"{data.chat_id}_{data.user_id}"

    now = time.time()

    last = COOLDOWNS.get(memory_id, 0)

    if now - last < 3:
        raise HTTPException(
            status_code=429,
            detail="Cooldown active"
        )

    COOLDOWNS[memory_id] = now

    user_data = await conversations.find_one(
        {"memory_id": memory_id}
    )

    if not user_data:
        history = []
    else:
        history = user_data.get("messages", [])

    history.append({
        "role": "user",
        "content": data.message
    })

    recent_history = history[-20:]

    messages = [
        {
            "role": "system",
            "content": (
                "You are Zaid AI. "
                "Be intelligent, helpful, friendly "
                "and remember previous messages."
            )
        }
    ]

    messages.extend(recent_history)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=500
    )

    reply = response.choices[0].message.content

    history.append({
        "role": "assistant",
        "content": reply
    })

    history = history[-100:]

    await conversations.update_one(
        {"memory_id": memory_id},
        {
            "$set": {
                "memory_id": memory_id,
                "messages": history,
                "last_used": int(time.time())
            }
        },
        upsert=True
    )

    await stats.update_one(
        {"_id": "global"},
        {"$inc": {"messages": 1}},
        upsert=True
    )

    return {
        "response": reply
    }
