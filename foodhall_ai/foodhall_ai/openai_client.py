from openai import OpenAI

from settings import OPENAI_API_KEY, MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

def ask_gpt(prompt: str) -> str:
    response = client.responses.create(
        model=MODEL,
        input=prompt
    )

    return response.output_text
