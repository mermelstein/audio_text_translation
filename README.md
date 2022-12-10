# Live Audio Transcription and Translation

This project uses the [Deepgram API](https://deepgram.com) to transcribe audio in real time and OpenAI's [GPT-3](https://openai.com/blog/gpt-3-apps/) to translate the transcript into another language.

To run this project you will need to create an account on [Deepgram](https://deepgram.com) and get an API key. You will also need to create an account on [OpenAI](https://openai.com) and get an API key. Also Docker Compose helps to run this project easily.

Once you have your API keys, run `docker compose up` to start the translator, then navigate to http://localhost:8000 in your browser. Allow access to your microphone and start speaking. A transcript of your audio will appear on the page.
