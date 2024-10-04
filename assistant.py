import subprocess
import pvporcupine
import pyaudio
import wolframalpha
import pyttsx3
import tkinter
import json
import random
from dotenv import load_dotenv, dotenv_values
import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import threading
import os
import urllib.parse  
import winshell
import pyjokes
import pygame
import feedparser
import smtplib
import ctypes
import time
import requests
import struct
import shutil
from twilio.rest import Client
from clint.textui import progress
from ecapture import ecapture as ec
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen

global username

global temp_pause
temp_pause=False
load_dotenv()


engine=pyttsx3.init('sapi5')

voices=engine.getProperty('voices')

engine.setProperty('voice',voices[0].id)


pygame.mixer.init()

music_dir = os.getenv('music_dir')  
songs = os.listdir(music_dir)  
global current_song_index 
current_song_index = 0
global is_paused
is_paused = True

global query

pygame.mixer.music.load(os.path.join(music_dir, songs[current_song_index]))


global is_stopped
is_stopped = True 


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def play_next_song():
    global current_song_index
    current_song_index = (current_song_index + 1) % len(songs)
    pygame.mixer.music.load(os.path.join(music_dir, songs[current_song_index]))
    pygame.mixer.music.play()

def play_previous_song():
    global current_song_index
    current_song_index = (current_song_index - 1) % len(songs)
    pygame.mixer.music.load(os.path.join(music_dir, songs[current_song_index]))
    pygame.mixer.music.play()


def stop_music():
    pygame.mixer.music.stop()
    global is_stopped
    is_stopped = True
    print("Music stopped.")

def resume_music():
    global is_paused, is_stopped
    if is_paused and not is_stopped:
        pygame.mixer.music.unpause()
        is_paused = False
        print("Music resumed.")
    elif is_stopped:
        play_next_song()
        is_stopped = False
        print("Music restarted.")

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning, sir.")
    elif 12 <= hour < 18:
        speak("Good afternoon, sir.")
    else:
        speak("Good evening, sir.")
    speak("I am Jarvis, your assistant.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Sorry, I didn't catch that.")
        return "None"
    return query

def check_song_end():
    while True:
        if not pygame.mixer.music.get_busy() and not is_paused and not is_stopped:
            play_next_song()
            time.sleep(1)  

def play_song(index):
    pygame.mixer.music.load(os.path.join(music_dir, songs[index]))  
    pygame.mixer.music.play()
    threading.Thread(target=check_song_end, daemon=True).start()

def wake_up():
    global is_paused, is_stopped,temp_pause

    access_key = os.getenv('wake_up_key')
    porcupine = pvporcupine.create(keywords=["jarvis"], access_key=access_key)
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(rate=porcupine.sample_rate,
                           channels=1,
                           format=pyaudio.paInt16,
                           input=True,
                           frames_per_buffer=porcupine.frame_length)

    print("Listening for wake word 'Jarvis'...")

    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            if not is_paused:  
                pygame.mixer.music.pause()
                is_paused= True
                temp_pause=True
                print("Music paused due to wake word.")

            print("Wake word detected!")

            speak("Yes, how can I help you?")
            break



def check_song_end():
    while True:
        if not pygame.mixer.music.get_busy() and not is_paused and not is_stopped:
            print("Song ended. Playing the next song.")
            play_next_song()
        time.sleep(1) 


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    email = os.getenv('main_email')
    passs = os.getenv('main_email_pass')
    server.login(email, passs)
    server.sendmail(email, to, content)
    server.close()



def play_song(index):
    global is_stopped,is_paused
    pygame.mixer.music.load(os.path.join(music_dir, songs[index]))  
    pygame.mixer.music.play() 
    is_paused = False
    is_stopped = False

    threading.Thread(target=check_song_end, daemon=True).start()

    

def user_name():
    speak('what should i call you sir')
    global username
    username = takeCommand()
    speak('welcome sir')
    speak(username)
    columns=shutil.get_terminal_size().columns
    print('#####################'.center(columns))
    print('      welcome Mr.',username.center(columns))
    print('#####################'.center(columns))

    speak('how may i assist you today')

if __name__=='__main__':
    clear = lambda:os.system('cls')

    clear()
    wishMe()
    user_name()
    while True:
        wake_up()
        query=takeCommand()
        


        if 'search' in query and 'wikipedia' in query:
            speak('searching wikipedia.....')
            query=query.replace('wikipedia','')
            result= wikipedia.summary(query,sentences=3)
            speak('according to wikipedia')
            print(result)
            speak(result)
        
        elif 'open youtube' in query:
            speak('opening youtube\n')
            webbrowser.open('youtube.com')
        
        elif 'open google' in query:
            speak('opening google\n')
            webbrowser.open('google.com')
        
        elif 'open stack overflow' in query:
            speak('opening stack over flow')
            webbrowser.open('stackoverflow.com')
            
        elif 'the time' in query or 'what the time' in query:
            strtime=datetime.datetime.now().strftime('%I and %M minutes and %S seconds %p')
            speak(f'the time now is{strtime}')
            print(f'the time now is {strtime}')

        
        elif 'open opera' in query:
            code_path=os.getenv('opera_dir')
            os.startfile(code_path)

        elif 'play music' in query or 'play song' in query:
            play_song(current_song_index)
        
        elif 'next' in query:
            play_next_song()

        elif 'back' in query:
            play_previous_song()

        elif 'stop' in query:
            stop_music()
        elif 'pause' in query:
             if temp_pause is True and  is_paused is True: 
                temp_pause = False 
                pygame.mixer.music.pause()
                is_paused = True
                speak("Music paused.")

        elif 'continue' in query or 'resume' in query:
            if is_paused:  
                pygame.mixer.music.unpause()
                is_paused = False
                speak("Music resumed.")
            else:
                speak("Music is already playing.")

        elif 'send mail' in query:
            try:
                speak('wht shoud i say?')
                content=takeCommand()
                speak('who do i send it to?')
                to= input()
                sendEmail(to,content)
                speak('email has been sent')
            except Exception as e:
                print(e)
                speak('iam not able to send this email')
        
        elif 'how are you' in query:
            speak("I am fine, Thank you")
            speak("How are you, Sir")
            answering=takeCommand()

            if 'fine' in answering or 'good' in answering:
                speak('its good to know you are fine')  

        elif "change my name to" in query:
            query = query.replace("change my name to", "")
            username = query
 
        elif "change name" in query:
            speak("What would you like to call me, Sir ")
            assistant_name = takeCommand()
            speak("Thanks for naming me")
 
        elif "what's your name" in query or "What is your name" in query:
            speak("My friends call me")
            speak(assistant_name)
            print("My friends call me", assistant_name)
 
        elif 'exit' in query:
            speak("Thanks for giving me your time")
            exit()       

        elif "who made you" in query or "who created you" in query: 
            speak("I have been created by glitch")
             
        elif 'joke' in query:
            joker=pyjokes.get_joke()
            speak(joker)
            print(joker)

        elif "who i am" in query:
            speak("If you talk then definitely your human.")

        elif 'is love' in query:
            speak("It is 7th sense that destroy all other senses")
 
        elif "who are you" in query:
            speak("I am your virtual assistant created by Glitch")
 
        elif 'reason for you' in query:
            speak("I was created as a Minor project by Mister Glitch ")


        elif 'change background' in query:
            background_location=str(input())
            ctypes.windll.user32.SystemParametersInfoW(20, 
                                                       0, 
                                                       background_location,
                                                       0)
            speak("Background changed successfully")


        elif 'whats the news today'in query or 'news' in query:
            try:
                api_key=os.getenv('news_api_key')
                base_news_url=os.getenv('url_news_api')
                url = f'{base_news_url}&apiKey={api_key}'

                response= requests.get(url)
                data= response.json()
                

                if data['status']=='ok':
                    articles= data['articles']
                    speak('here some headlines:')
                    print('=============== TOP HEADLINES ============\n')

                    for i,article in enumerate(articles[:5], start=1):
                        print(f'{i}. {article["title"]}\n{article["description"]}\n')
                        speak(f'{i}. {article["title"]}')

                else:
                    speak('iam unable to fetch the news right now')

            except Exception as e:
                print(f'error: {e}')
                speak('i encountered an error while getting news')


        elif 'lock window' in query:
                speak("locking the device")
                ctypes.windll.user32.LockWorkStation()
 
        elif 'shutdown system' in query:
                speak("Hold On a Sec ! Your system is on its way to shut down")
                subprocess.call('shutdown / p /f')
                 
        elif 'empty recycle bin' in query:
            winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
            speak("Recycle Bin Recycled")



        elif "don't listen" in query or "stop listening" in query:
            speak("for how much time you want to stop jarvis from listening commands")
            a = int(takeCommand())
            time.sleep(a)
            print(a)


        elif "where is" in query:
            query = query.replace("where is", "")
            location = query.strip()
            speak("User asked to Locate")
            speak(location)
            encoded_location = urllib.parse.quote(location)
            url=f"https://www.google.com/maps/search/?api=1&query={location.replace(' ', '+')}"
            webbrowser.open(url)
            print("Opening URL:", url)

        elif "camera" in query or "take a photo" in query:
            ec.capture(0, "Jarvis Camera ", "img.jpg")
        
        elif "note this" in query or 'make a note' in query:
            speak('what should i write sir')
            note=takeCommand()
            file=open('jarvis.txt','w')
            speak('should i include date and time sir')
            snfm=takeCommand()
            if 'yes' in snfm or 'sure' in snfm or 'yeah' in snfm:
                strTime = datetime.datetime.now().strftime("%H:%M:%S  %p")
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
            else:
                file.write(note)

        elif "show note" in query:
            speak("Showing Notes")
            file = open("jarvis.txt", "r") 
            print(file.read())
            speak(file.read(6))

        elif "clear note" in query or "clear notes" in query:
            file = open("jarvis.txt", "w") 
            file.write("") 
            file.close()  
            speak("All notes have been cleared.")



 
        elif "restart" in query:
            subprocess.call(["shutdown", "/r"])
             
        elif "hibernate" in query or "sleep" in query:
            speak("Hibernating")
            subprocess.call("shutdown / h")
 
        elif "log off" in query or "sign out" in query:
            speak("Make sure all the application are closed before sign-out")
            time.sleep(5)
            subprocess.call(["shutdown", "/l"])
        elif "jarvis" in query:
             
            wishMe()
            speak("iam in your service Master")
            speak(username)


        elif "good" in query and 'morning' in query:
            speak("A warm" +query)
            speak("How are you Mister")
            speak(username)
 
        
        elif "will you be my gf" in query or "will you be my bf" in query:   
            speak("I'm not sure about, may be you should give me some time")
 
        elif "how are you" in query:
            speak("I'm fine, glad you me that")
 
        elif "i love you" in query:
            speak("It's hard to understand")   

        elif "what is" in query or "who is" in query:
            api_key_wolf=os.getenv('calculate_api')
            client = wolframalpha.Client(api_key_wolf)
            res = client.query(query)
             
            try:
                print (next(res.results).text)
                speak (next(res.results).text)
            except StopIteration:
                print ("No results")  
            
        elif "calculate" in query: 
            api_key_wolf=os.getenv('calculate_api')
            app_id = api_key_wolf
            client = wolframalpha.Client(app_id)
            indx = query.lower().split().index('calculate') 
            query = query.split()[indx + 1:] 
            res = client.query(' '.join(query)) 
            answer = next(res.results).text
            print("The answer is " + answer) 
            speak("The answer is " + answer) 


        elif "weather" in query or 'whats the weather' in query:
            api_key = os.getenv('weather_api_key')
            base_url = os.getenv('weather_base_url')
            speak(" City name ")
            print("City name : ")
            city_name = takeCommand()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url) 
            x = response.json() 
             
            if x["cod"] != "404": 
                y = x["main"] 
                current_temperature = y["temp"] 
                current_pressure = y["pressure"] 
                current_humidiy = y["humidity"] 
                z = x["weather"] 
                weather_description = z[0]["description"] 
                print(" Temperature (in kelvin unit) = " +str(current_temperature)+"\n atmospheric pressure (in hPa unit) ="+str(current_pressure) +"\n humidity (in percentage) = " +str(current_humidiy) +"\n description = " +str(weather_description)) 

                speak(f"The temperature is {current_temperature} kelvin, "
                f"the atmospheric pressure is {current_pressure} hPa, "
                f"the humidity is {current_humidiy} percent, "
                f"and the weather is described as {weather_description}.")
             
            else: 
                speak(" City Not Found ")

        elif 'code' in query or 'open vs code'in query or 'open vscode' in query:
            speak('opening vs code')
            vscode_path=os.getenv('vs_code_path')
            os.startfile(vscode_path)
        

        elif 'open' in query and 'wikipedia' in query:
            speak('opening Wikipedia')
            webbrowser.open("https://wikipedia.com")


        if is_paused is True and is_stopped is False and temp_pause is True:
            resume_music()
            temp_pause= False
            
        



        

        




    



