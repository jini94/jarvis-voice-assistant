import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
	print ("Adjusting for background noise...")
	recognizer.adjust_for_ambient_noise(source,duration = 1)
	print("Listening... say something!")
	audio = recognizer.listen(source)

print("Recognizing...")
try:
	text = recognizer.recognize_google(audio)
	print(f"You said: {text}")
except sr.UnknownValueError:
	print("Sorry. I didn't catch that.")
except sr.RequestError as e:
	print(f"Could not request results; {e}")