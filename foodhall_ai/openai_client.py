from openai import OpenAI

client = OpenAI()

def ask_gpt(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-5.5",
        input=prompt,
    )

    return response.output_text
