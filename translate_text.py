import os
import openai

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

english_prompt_text = "translate the following American English text into Mandarin Chinese: "
spanish_prompt_text = "translate the following Spanish text into American English: "
chinese_prompt_text = "translate the following Mandarin Chinese text into English: "

def translate(text, language_var):
    if language_var == 'en':
        prompt_text = english_prompt_text
    elif language_var == 'es':
        prompt_text = spanish_prompt_text
    elif language_var == 'zh':
        prompt_text = chinese_prompt_text

    response = openai.Completion.create(
        model="text-davinci-003", prompt=prompt_text + text, temperature=0, max_tokens=200
    )
    return response["choices"][0]["text"]
