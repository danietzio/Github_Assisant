from ollama import AsyncClient


async def generate_answer(prompt: str) -> str:

    client = AsyncClient(
        host="http://host.docker.internal:11434"
    )

    response = await client.chat(
        model="qwen2.5-coder:3b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.message.content