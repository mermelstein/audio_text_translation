from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Dict, Callable
from deepgram import Deepgram
from dotenv import load_dotenv
import json
import os
from translate_text import translate
from debouncer import Debouncer

load_dotenv()

app = FastAPI()

dg_client = Deepgram(os.getenv("DEEPGRAM_API_KEY"))

templates = Jinja2Templates(directory="templates")

async def process_audio(fast_socket: WebSocket, language_var):
    debouncer = Debouncer(delay=0.5)
    confidence_threshold = 0.8

    async def get_transcript(data: Dict) -> None:
        if 'channel' in data and data['channel']['alternatives'][0]['confidence'] >= confidence_threshold:
            transcript = data['channel']['alternatives'][0]['transcript']

            if transcript:
                await debouncer.debounce(send_translated_text, fast_socket, transcript)

    async def send_translated_text(websocket: WebSocket, transcript: str):
        translated_text = translate(transcript, language_var[0])
        message = json.dumps({"original": transcript, "translated": translated_text})
        await websocket.send_text(message)

    deepgram_socket = await connect_to_deepgram(get_transcript, language_var)

    return deepgram_socket

async def connect_to_deepgram(transcript_received_handler: Callable[[Dict], None], language_var):
    try:
        socket = await dg_client.transcription.live({'punctuate': True, 'interim_results': False, 'language': language_var[1]})
        socket.registerHandler(socket.event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))
        socket.registerHandler(socket.event.TRANSCRIPT_RECEIVED, transcript_received_handler)

        return socket
    except Exception as e:
        raise Exception(f'Could not open socket: {e}')

@app.get("/", response_class=HTMLResponse)
def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/listen")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        language_var = ['en','en-US']
        # language_var = ['es','es-419']
        # language_var = ['zh','zh-CN']

        deepgram_socket = await process_audio(websocket, language_var)

        while True:
            data = await websocket.receive_bytes()
            deepgram_socket.send(data)
    except Exception as e:
        raise Exception(f'Could not process audio: {e}')
    finally:
        await websocket.close()
