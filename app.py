from openai import OpenAI
from config import CEREBRAS_API_KEY, MODEL_NAME

client = OpenAI(
    api_key=CEREBRAS_API_KEY,
    base_url="https://api.cerebras.ai/v1"
)

@app.get("/test")
async def test():

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": "Say hello"
            }
        ],
        max_tokens=20
    )

    return {
        "response": response.choices[0].message.content
    }
