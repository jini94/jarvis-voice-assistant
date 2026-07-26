import asyncio
import os
from flask import Flask, render_template, jsonify
import speech_recognition as sr
import edge_tts
import ollama
import uuid
import time
import pygame
from playsound import playsound

app = Flask(__name__)

VOICE = "en-GB-RyanNeural"
AUDIO_FILE = "response.mp3"

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=12)
    try:
        return recognizer.recognize_google(audio)
    except (sr.UnknownValueError,sr.RequestError):
        return None
    except sr.WaitTimeoutError:
        return None

def ask_ollama(prompt):
	response = ollama.chat(
		model = "llama3.2",
		messages = [{"role": "user","content": prompt}]
	)
	return response["message"]["content"]


def speak_sync(text):
    filename = f"response_{uuid.uuid4().hex}.mp3"
    communicate = edge_tts.Communicate(text, VOICE)
    asyncio.run(communicate.save(filename))

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    start_time = time.time()
    while pygame.mixer.music.get_busy():
        if time.time() - start_time > 60:
            pygame.mixer.music.stop()
            break
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove(filename)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/talk", methods= ["POST"])
def talk():
	user_text = listen()
	if not user_text:
		return jsonify(user_text="(didn't catch that)", jarvis_text="Sorry, try again.")
	reply = ask_ollama(user_text)
	speak_sync(reply)
	return jsonify(user_text=user_text, jarvis_text=reply)

if __name__ == "__main__":
	app.run(debug=True)
