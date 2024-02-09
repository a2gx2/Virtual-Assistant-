import speech_recognition as sr
import pyttsx3
import pyaudio
import pywhatkit
import datetime
import wikipedia
import smtplib
import requests
import random

# name of the virtual assistant
name = 'cortana'

# your api key
key = 'YOUR_API_KEY_HERE'

# OpenWeatherMap API key
weather_api_key = 'YOUR_OPENWEATHERMAP_API_KEY'

# the flag helps us to turn off the program
flag = 1

listener = sr.Recognizer()
engine = pyttsx3.init()

# get voices and set the first of them
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# editing default configuration
engine.setProperty('rate', 178)
engine.setProperty('volume', 0.7)

def play_audio(filename):
    playsound(filename)

def talk(text):
    '''
    here, virtual assistant can talk
    '''
    engine.say(text)
    engine.runAndWait()

def listen():
    '''
    The program recovers our voice and sends it to another function
    '''
    global flag
    flag = 1
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            voice = listener.listen(source)
            rec = listener.recognize_google(voice, language='es-ES')
            rec = rec.lower()

            if name in rec:
                rec = rec.replace(name, '')
                flag = run(rec)
            else:
                talk("Vuelve a intentarlo, no reconozco: " + rec)
    except:
        pass
    return flag

def send_email(subject, message, to_email):
    from_email = "tucorreo@gmail.com"
    password = "tucontraseña"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, password)
        msg = f"Subject: {subject}\n\n{message}"
        server.sendmail(from_email, to_email, msg)
        server.quit()
        talk("Correo enviado exitosamente.")
    except Exception as e:
        talk("Error al enviar el correo.")

def get_weather(city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": weather_api_key,
        "units": "metric",  # Use metric units for temperature
        "lang": "es"  # Use Spanish language for weather description
    }

    response = requests.get(base_url, params=params)
    weather_data = response.json()

    if response.status_code == 200:
        temperature = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        return f"La temperatura en {city_name} es de {temperature}°C y está {description}."
    else:
        return "No se pudo obtener la información del clima."

def run(rec):
    '''
    All the actions that virtual assistant can do
    '''
    global flag
    if 'reproduce' in rec:
        music = rec.replace('reproduce', '')
        talk('Reproduciendo ' + music)
        pywhatkit.playonyt(music)
    elif 'dime la hora' in rec:
        hora = datetime.datetime.now().strftime('%I:%M %p')
        talk("Son las " + hora)
    elif 'busca' in rec:
        order = rec.replace('busca', '')
        wikipedia.set_lang("es")
        info = wikipedia.summary(order, 1)
        talk(info)
    elif 'envía un correo' in rec:
        talk("Por favor, dime el asunto del correo.")
        subject = listen()
        talk("Ahora, dime el mensaje del correo.")
        message = listen()
        talk("Finalmente, ¿a qué dirección de correo deseas enviar el correo?")
        to_email = listen()
        send_email(subject, message, to_email)
    elif 'dime el clima' in rec:
        talk("Por favor, dime la ciudad para la que quieres saber el clima.")
        city_name = listen()
        weather_info = get_weather(city_name)
        talk(weather_info)
    elif 'chao' in rec:
        talk("Hasta luego. ¡Que tengas un buen día!")
        flag = 0
    return flag

# Llamada al bucle principal
while flag:
    flag = listen()
