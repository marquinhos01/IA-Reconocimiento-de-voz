from email import message
from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys
import nltk
import json
import random
import requests
from deep_translator import GoogleTranslator
nltk.download('omw-1.4')


recognizer = speech_recognition.Recognizer();

speaker = tts.init();
speaker.setProperty("rate", 140);

todo_list = [];

def agregar_a_lista():
    global recognizer
    speaker.say(respuesta("agregar_a_lista"))
    speaker.runAndWait()
    done = False
    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                item = recognizer.recognize_google(audio, language="es-AR")
                item = item.lower()
                speaker.say("Agregue los objetos a la lista")
                speaker.runAndWait()
                for e in todo_list:
                    print(e)
                todo_list.append(item)
                done = True

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
    

def mostrar_lista():
    for item in todo_list:
        speaker.say(item)
        speaker.runAndWait()


def respuesta(comando):
    with open('intents.json') as file:
        data = json.load(file)
        respuestas = []
        for intento in data['intents']:
            if intento["tag"] == comando:
                respuestas = intento["responses"]
                return respuestas[random.randint(0,len(respuestas)-1)]

def saludo():
    speaker.say(respuesta("saludo"))
    speaker.runAndWait()

def chiste():
    speaker.say(getChiste())
    speaker.runAndWait()

def adios():
    speaker.say(respuesta("adios"))
    speaker.runAndWait()
    sys.exit(0)

def getChiste():
    url = "https://api.chucknorris.io/jokes/random";
    data = requests.get(url)
    if data.status_code == 200:
        data = data.json()
        #Se traduce el chiste ya que viene en inglés
        traductor = GoogleTranslator(source='en', target='es')
        chiste = traductor.translate(data["value"]);
        print(chiste)
        return chiste

mappings = {
    "saludo": saludo,
    "agregar_a_lista": agregar_a_lista,
    "mostrar_lista":mostrar_lista,
    "chiste":chiste,
    "adios": adios
}

assistant = GenericAssistant("intents.json", intent_methods=mappings);
assistant.train_model()


while True:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio, language="es-AR")
            message = message.lower()
            print(message)
        assistant.request(message)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()





