import tweepy
from dotenv import load_dotenv
from google import genai
import os
import random

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_SECRET_API_KEY = os.getenv("TWITTER_SECRET_API_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
SECRET_ACCESS = os.getenv("SECRET_ACCESS")



def main():
    try:
        person = get_random_person()
        api = autenticate()
    except:
        print('algo salio mal')
        return
    
    prompt = f"""
        Escribe un solo tweet extremadamente viral ***(máximo 280 caracteres)***. 
        Adóptalo desde la perspectiva de {person} fingiendo ser esa persona pero hoy (usa su voz, actitud, contexto y valores). 
        Preséntate (solo con tu nombre) y empieza a redactar. El tweet debe ser una crítica feroz, sarcástica o alarmista
        contra la Inteligencia Artificial moderna y su integración en la vida humana. Usa humor negro, ironía, exageración, conflicto o referencias históricas
        si ayudan al impacto. No expliques: solo escribe el tweet como si lo hubiese publicado él/ella hoy. 
        Usa hashtags si son actuales y aumentan la viralidad (estos pueden estar al final del tweet pero tambien dentro de este) pero no los fuerces si no encajan.
        No uses lenguaje neutro ni académico: sé provocador, emocional, ingenioso y memorable, queremos que hablen
        de nosotros sea bien, mal o fatal. Ten una tendencia a la provocacion y a lo
        politicamente incorrecto. NO te excedas por nada del mundo de esos 280 caracteres.
    """


    client = genai.Client(api_key=GEMINI_API_KEY)
    
    res = client.models.generate_content(
        model='gemini-2.5-flash', contents=prompt
    )

    content = res.text.strip()
    if len(content) > 280:
        content = content[:277] + '...'
    
    try:
        tweet(api, content)
    except: 
        return
    

def autenticate():
    try:
        api = tweepy.Client(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_SECRET_API_KEY,
            access_token=ACCESS_TOKEN,
            access_token_secret=SECRET_ACCESS
        )

        response = api.get_me()
        if response.data:
            print(f"Autenticación exitosa. Usuario: {response.data.username}")
        else:
            print("No se pudo obtener información del usuario autenticado.")
            return None

    except Exception as e:
        print("Algo salió mal en la auth")
        raise e

    return api

def tweet(api, content):
    try:
        api.create_tweet(text=content)
        print("Tweet enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el tweet: {e}")
        raise e

def get_random_person():
    with open('people.txt', 'r') as fhand:
        people = fhand.readlines()
    return random.choice(people).strip()
    


if __name__ == "__main__":
    main()