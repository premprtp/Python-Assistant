import subprocess
import wolframalpha
import pyttsx3
import json
import random
import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import pyjokes
import smtplib
import ctypes
import time
import requests
import shutil
from ecapture import ecapture as ec
from bs4 import BeautifulSoup
from urllib.request import urlopen

# Initialize pyttsx3
engine = pyttsx3.init('dummy')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Function to convert text to speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def clear(): 
    os.system('cls')

# Function to greet the user based on the time of day
def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning Sir!")
    elif 12 <= hour < 18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")

    assname = "Jarvis 2.0"
    speak("I am your Assistant")
    speak(assname)

# Function to get the user's name
def getUsername():
    speak("What should I call you, sir?")
    uname = takeCommand()
    speak("Welcome, Mister " + uname)
    print("Welcome, Mr.", uname)

# Function to capture voice command
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        speak("Some Technical Error.")
        return "None"
    return query

# Function to send email
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your-email', 'your-password')
    server.sendmail('your-email', to, content)
    server.close()

# Main program logic
if __name__ == '__main__':

    clear()
    wishMe()
    getUsername()

    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("google.com")
        elif 'open stackoverflow' in query:
            speak("Opening Stack Overflow")
            webbrowser.open("stackoverflow.com")
        elif 'play music' in query or 'play song' in query:
            speak('Playing music..')
            music_dir = "/path/to/music/folder"
            songs = os.listdir(music_dir)
            random.shuffle(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        elif 'email to' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "receiver-email"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry sir. I am not able to send this email at the moment.")
        elif 'search' in query:
            query = query.replace("search", "")
            webbrowser.open(query)
        elif 'search maps' in query:
            query = query.replace("search maps", "")
            webbrowser.open("https://www.google.com/maps/search/" + query)
        elif 'capture screenshot' in query:
            speak("Please tell me the name for the screenshot file")
            name = takeCommand().lower()
            speak("Please hold the screen for a few seconds")
            time.sleep(3)
            img = ec.capture_screen()
            img.save(f"{name}.png")
            speak("Screenshot saved as " + name)
        elif 'news' in query:
            try:
                news_url = "https://news.google.com/news/rss"
                Client = urlopen(news_url)
                xml_page = Client.read()
                Client.close()
                soup_page = BeautifulSoup(xml_page, "xml")
                news_list = soup_page.findAll("item")
                for news in news_list[:15]:
                    print(news.title.text)
                    speak(news.title.text)
            except Exception as e:
                print(e)
                speak("Sorry sir, I am unable to fetch the news at the moment.")
        elif 'system information' in query:
            uname = platform.uname()
            speak(f"System: {uname.system}")
            speak(f"Node Name: {uname.node}")
            speak(f"Release: {uname.release}")
            speak(f"Version: {uname.version}")
            speak(f"Machine: {uname.machine}")
            speak(f"Processor: {uname.processor}")
        elif 'tell me a joke' in query:
            speak(pyjokes.get_joke())
        elif 'shutdown' in query:
            speak("Shutting down the system. Goodbye, Sir!")
            subprocess.call('shutdown / p /f')
        elif 'restart' in query:
            speak("Restarting the system. Be right back, Sir!")
            subprocess.call('shutdown / r /f')
        elif 'logout' in query:
            speak("Logging out. Goodbye, Sir!")
            subprocess.call('shutdown / l')
        elif 'remember that' in query:
            speak("What should I remember?")
            data = takeCommand()
            speak("You asked me to remember " + data)
            remember = open('data.txt', 'w')
            remember.write(data)
            remember.close()
        elif 'do you remember anything' in query:
            remember = open('data.txt', 'r')
            speak("You asked me to remember that " + remember.read())
        elif 'remove memory' in query:
            speak("Memory removed, sir.")
            remember = open('data.txt', 'w')
            remember.write("")
            remember.close()
        elif 'calculate' in query:
            app_id = "your-wolframalpha-app-id"
            client = wolframalpha.Client(app_id)
            indx = query.lower().split().index('calculate')
            query = query.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            print("The answer is: " + answer)
            speak("The answer is " + answer)
        elif 'go offline' or 'offline' or 'bye' in query:
            speak("Going offline, sir!")
            quit()
