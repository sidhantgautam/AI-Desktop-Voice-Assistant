import pyttsx3
import datetime
import requests
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import psutil
import pyjokes
import time
from googletrans import Translator
from newsapi import NewsApiClient

# Setting up the text-to-speech engine
recognizre = sr.Recognizer()


speaker = pyttsx3.init('sapi5')
speaker.setProperty('rate', 150)
voices = speaker.getProperty('voices')
print(voices[1].id)
speaker.setProperty('voice', voices[0].id)

# Function to convert text to speech
def speak(audio):
    speaker.say(audio)
    speaker.runAndWait()

# Function to wish the user based on the current time
def wish_me():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning!")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am Jarvis. How may I assist you?")



# Function to take voice input and return text
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen for audio input
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio).lower()  # Use Google Web Speech API for recognition
        print(f"User: {query}")
        return query

    except Exception as e:
        print("I'm sorry, I didn't understand that. Please say that again.")
        query = None

    return query

def calculate_math_expression(query):
    try:
        # Modify the query to include the necessary mathematical operation
        query = query.replace("calculate", "")
        
        # Check if the query includes the word 'square root' and handle it accordingly
        if 'square root' in query:
            # Extract the number from the query and calculate the square root
            number = float(query.replace("square root of", ""))
            result = number ** 0.5
            result_text = f"The result is {result}"
            print(result_text)
            speak(result_text)
        else:
            # Evaluate the general math expression
            result = eval(query)
            result_text = f"The result is {result}"
            print(result_text)
            speak(result_text)

    except Exception as e:
        print(f"Error performing math calculation: {e}")
        speak("I'm sorry, there was an error while performing the math calculation.")

reminders_file_path = "reminders.txt"
reminders = {}

# Function to add a reminder
def add_reminder(query):
    speak("Sure, what should I remind you about?")
    reminder_task = listen()
    if reminder_task:
        speak("When should I remind you about?")
        reminder_time = listen()
        if reminder_time:
            reminders[reminder_task] = reminder_time
            save_reminders()  # Save reminders to the file
            speak(f"I will remind you to {reminder_task} at {reminder_time}.")

# Function to check and notify about reminders
def check_reminders():
    load_reminders()  # Load reminders from the file
    current_time = datetime.datetime.now().strftime("%H:%M").lower()
    for task, time in reminders.items():
        if time in current_time:
            speak(f"Reminder: Don't forget to {task}.")

# Function to save reminders to a file
def save_reminders():
    with open(reminders_file_path, 'w') as file:
        for task, time in reminders.items():
            file.write(f"{task}:{time}\n")

# Function to load reminders from a file
def load_reminders():
    try:
        with open(reminders_file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                task, time = line.strip().split(':')
                reminders[task] = time
    except FileNotFoundError:
        # If the file is not found, create an empty file
        with open(reminders_file_path, 'w'):
            pass
    except Exception as e:
        print(f"Error loading reminders: {e}")

translator = Translator()

# Function for language translation
def translate_text(query):
    speak("Sure, what text would you like to translate?")
    text_to_translate = listen()
    if text_to_translate:
        speak("Into which language would you like to translate?")
        target_language = listen()
        if target_language:
            try:
                translated_text = translator.translate(text_to_translate, dest=target_language).text
                speak(f"The translation is: {translated_text}")
            except Exception as e:
                print(f"Translation error: {e}")
                speak("I'm sorry, there was an error during translation.")

translator = Translator()
news_api_key = 'YOUR_NEWS_API_KEY'  # Replace with your News API key
newsapi = NewsApiClient(api_key=news_api_key)

# Function for fetching and reading news updates
def get_news_updates():
    speak("Sure, I'll fetch the latest news for you.")
    try:
        # You can customize the news source, category, and language based on your preferences
        news = newsapi.get_top_headlines(language='en', country='us', page_size=5)
        
        if news['totalResults'] > 0:
            speak("Here are the top news headlines:")
            for idx, article in enumerate(news['articles']):
                speak(f"News {idx + 1}: {article['title']}")
                time.sleep(1)  # Pause for a moment between news articles
        else:
            speak("I couldn't find any news updates at the moment.")

    except Exception as e:
        print(f"Error fetching news: {e}")
        speak("I'm sorry, there was an error fetching news updates.")




# Function to get Jarvis's response to a user query
def get_response(query):
    if 'wikipedia' in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia:")
        print(("According to Wikipedia:"))
        print(results)
        speak(results)
        

    elif 'open youtube' in query:
        print("Opening YouTube...")
        speak("Opening YouTube...")
        youtube_path = "C:\\Users\\gauta\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"
        try:
            os.startfile(youtube_path)
        except Exception as e:
            print(f"Error opening YouTube: {e}")
            speak("I'm sorry, there was an error opening YouTube.")
        
    elif 'open virtualbox' in query:
        print("Opening Virtual Box...")
        speak("Opening Virtual Box...")
        virtualbox_path = "C:\\Program Files\\Oracle\\VirtualBox\\VirtualBox.exe"
        try:
            os.startfile(virtualbox_path)
        except Exception as e:
            print(f"Error opening VirtualBox: {e}")
            speak("I'm sorry, there was an error opening VirtualBox.")

    elif 'open Brave' in query:
        speak("Opening Brave...")
        brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave"
        try:
            os.startfile(brave_path)
        except Exception as e:
            print(f"Error opening Brave: {e}")
            speak("I'm sorry, there was an error opening Brave.")
    

    elif 'open google' in query:
        speak("Opening Google...")
        webbrowser.open("https://www.google.com/")
    

    elif 'open yahoo' in query:
        speak("Opening Yahoo...")
        webbrowser.open("https://www.yahoo.com/")
    
    elif 'open duckduckgo.' in query:
        speak("Opening DuckDuckGo....")
        webbrowser.open("https://duckduckgo.com/")

    elif 'open bing' in query:
        speak("Opening Bing....")
        webbrowser.open("https://www.bing.com/")

    elif 'play music' in query:
        speak("Playing music...")
        music_dir = 'D:\\Music'
        songs = os.listdir(music_dir)
        random_song = random.choice(songs)
        # os.startfile(os.path.join(music_dir, random_song))
        os.startfile(os.path.join(music_dir, songs[0]))
    elif 'the time' in query:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"The current time is {current_time}")
        speak(f"The current time is {current_time}")

    elif 'open code' in query:
        speak("Opening Visual Studio Code...")
        code_path = "C:\\Users\\User\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(code_path)

    elif 'search_on_youtube' in search_on_youtube(query):
        query = '+'.join(query.split()) 
        # Construct the search URL for YouTube
        url = f'https://www.youtube.com/results?search_query={query}' 
        # Open the URL in the default web browser 
        webbrowser.open(url)


    elif 'joke' in query:
        joke = pyjokes.get_joke()
        speak(joke)

    elif 'cpu uses' in query:
        usage = str(psutil.cpu_percent())
        speak("CPU usage is at " + usage + " percent")

    elif 'stop' in query:
            speak("Goodbye!")
            exit()

def search_on_youtube(query):
    # Encode the query string to replace spaces with '+'
    query = '+'.join(query.split())

    # Construct the search URL for YouTube
    url = f'https://www.youtube.com/results?search_query={query}'

    # Open the URL in the default web browser
    webbrowser.open(url)

    
# Function to get the weather forecast for a given location
def get_weather(location):
    api_key = 'your_api_key'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    if data['cod'] == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        speak(f"The weather in {location} is {weather_description} with a temperature of {temperature} degrees Celsius. It feels like {feels_like} degrees Celsius.")
    else:
        speak("I'm sorry, I could not retrieve the weather information for that location.")

# Function to get the current location using IP geolocation
def get_location():
    url = 'https://ipinfo.io/json'
    response = requests.get(url)
    data = response.json()
    city = data['city']
    state = data['region']
    country = data['country']
    print(city, state, country)
    speak(f"You are currently in {city}, {state}, {country}.")

# Main loop to listen for user input and respond accordingly
if __name__ == "__main__":
    wish_me()
    while True:
        query = listen()
        if query is not None:
            query = query.lower()
            if 'goodbye' in query or 'bye' in query:
                speak("Goodbye!")
                break
            elif 'wikipedia' in query:
                get_response(query)
            elif 'youtube' in query:
                get_response(query)
            elif 'google' in query:
                get_response(query)
            elif 'yahoo' in query:
                get_response(query)
            elif 'Duck Duck Go' in query:
                get_response(query)
            elif 'bing' in query:
                get_response(query)
            elif 'music' in query:
                get_response(query)
            elif 'time' in query:
                get_response(query)
            elif 'code' in query:
                get_response(query)
            elif 'email' in query:
                get_response(query)
            elif 'joke' in query:
                get_response(query)
            elif 'cpu' in query:
                get_response(query)
            elif 'search_on_youtube' in query:
                get_response(query)
            elif 'weather' in query:
                get_weather(query.split()[-1])
            elif 'location' in query:
                get_location()
            elif 'fetch reminders' in query:
                check_reminders()
                continue  
            elif 'reminder' in query:
                add_reminder(query)
                continue
            elif 'translate' in query:
                translate_text(query)
            elif 'news' in query or 'headlines' in query:
                get_news_updates()
            elif 'calculate' in query or 'Jarvis' in query:
                calculate_math_expression(query)
            else:
                speak("I'm sorry, I don't know the answer to that. Would you like me to search the web?")
