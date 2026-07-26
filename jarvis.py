import asyncio
import edge_tts
from playsound import playsound

VOICE = "en-GB-RyanNeural"
TEXT = "Hello, I am Jarvis. I am online and ready to assist."
AUDIO_FILE = "response.mp3"

async def speak(text):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(AUDIO_FILE)
    playsound(AUDIO_FILE)

asyncio.run(speak(TEXT))