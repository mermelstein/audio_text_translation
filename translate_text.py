import os
import openai

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

prompt_text = "translate the following text into Mandarin Chinese: "

def translate(text):
    response = openai.Completion.create(
        model="text-davinci-003", prompt=prompt_text + text, temperature=0, max_tokens=200
    )
    return response["choices"][0]["text"]
