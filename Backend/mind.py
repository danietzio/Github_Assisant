from ollama import chat

async def generate_answer(prompt: str) -> str: 
  response = chat(model='qwen2.5-coder:3b',
       messages=[{
         'role': 'user',
         'content': prompt
       }],
  )

  return response.message.content
