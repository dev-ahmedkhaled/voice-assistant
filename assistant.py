import wikipedia
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

# using golbal user name for the user and for easier access

global username
# creating temp pause variable to let jarvis pause when i call for him
global temp_pause
temp_pause=False
# making .env 
load_dotenv()

# creating engine for txt to speech
engine=pyttsx3.init('sapi5')

# getting voices properties of engine

voices=engine.getProperty('voices')

#setting the voice for male to change to female 1 insted of 0

engine.setProperty('voice',voices[0].id)

#  making music player using pygame

pygame.mixer.init()

music_dir = os.getenv('music_dir')  
songs = os.listdir(music_dir) 
# initializing song index 
global current_song_index 
current_song_index = 0
# initializing is paused
global is_paused
is_paused = True
# initializing query to save the user input in it 
global query

# loading music
pygame.mixer.music.load(os.path.join(music_dir, songs[current_song_index]))

# initializing is stopped to check if music stopped or not
global is_stopped
is_stopped = True 

# function for text to speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#next song function also checks if there are corrupt music files in the directory and skips them
def play_next_song():
    global current_song_index
    current_song_index = (current_song_index + 1) % len(songs)
    try:
        pygame.mixer.music.load(os.path.join(music_dir, songs[current_song_index]))
        pygame.mixer.music.play()
    except pygame.error as e:
            print(f"Error playing song: {e}")
            print("Switching to next song...")
            play_next_song()


            
# same as next song but to switch song to previous
def play_previous_song():
    global current_song_index
    current_song_index = (current_song_index - 1) % len(songs)
    try:
        pygame.mixer.music.load(os.path.join(music_dir, songs[current_song_index]))
        pygame.mixer.music.play()
    except pygame.error as e:
            print(f"Error playing song: {e}")
            print("Switching to previous song...")
            play_previous_song()


# function to stop music entirely
def stop_music():
    pygame.mixer.music.stop()
    global is_stopped
    is_stopped = True
    print("Music stopped.")

# function to resume music when paused
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



# function that checks real life time and respond based on time when starting jarvis

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning, sir.")
    elif 12 <= hour < 18:
        speak("Good afternoon, sir.")
    else:
        speak("Good evening, sir.")
    speak("I am Jarvis, your assistant.")

# function to take command from user by creating speech recognizer obj and recongize it using google speech service
# if successful return the query
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


# function to checks song end

def check_song_end():
    while True:
        if not pygame.mixer.music.get_busy() and not is_paused and not is_stopped:
            play_next_song()
            time.sleep(1)  

#function to play song and starts a new thread to check when song ends
def play_song(index):
    pygame.mixer.music.load(os.path.join(music_dir, songs[index]))  
    pygame.mixer.music.play()
    threading.Thread(target=check_song_end, daemon=True).start()


# function to wake jarvis up when 'jarvis' is heard using pvporcupine and when music plays and jarvis wake word is heard it stops music 
# and after command is done re enables it

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

# function to send emails from jarvis directly using gmail smtp
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

    
# takes user name and save it
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


# search wiki function 
def search_wikipedia(query):
    try:
        wikipedia.set_lang("en")
        summary = wikipedia.summary(query, sentences=2)  # Get a summary of the first two sentences
        speak('According to Wikipedia:')
        print(summary)
        speak(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("The query is ambiguous. Here are some suggestions:")
        print(e.options)
    except wikipedia.exceptions.PageError:
        speak("Sorry, I couldn't find any results on Wikipedia.")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("An error occurred while searching Wikipedia.")


if __name__=='__main__':
    clear = lambda:os.system('cls')

    clear()
    wishMe()
    user_name()
    while True:
        wake_up()
        query=takeCommand().lower()
        

        if 'search' in query and 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace('wikipedia', '')
            search_wikipedia(query)
        
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
# adding media controls for easier controling of media while songs playing
        elif 'open media controls' in query:
            resume_music()

            while True:
                temp_command=takeCommand()
                if 'next' in temp_command:
                     play_next_song()

                elif 'back' in temp_command and 'pervious' in temp_command:
                    play_previous_song()

                elif 'stop' in temp_command:
                    stop_music()

                elif 'pause' in temp_command:
                    temp_pause = True 
                    is_paused = True
                    if temp_pause is True and  is_paused is True: 
                        temp_pause = False 
                        pygame.mixer.music.pause()
                        is_paused = True
                        speak("Music paused.")

                elif 'continue' in temp_command or 'resume' in temp_command:
                    if is_paused:  
                        pygame.mixer.music.unpause()
                        is_paused = False
                        speak("Music resumed.")
                    else:
                        speak("Music is already playing.")

                elif 'exit' in temp_command:
                    break


        elif 'stop' in query:
            stop_music()

                

        elif 'play music' in query or 'play song' in query:
            play_song(current_song_index)
        

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
    # jokes for jarvis why not 
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

# change background to specifed bakground path "may change it later" for more user friendly option
        elif 'change background' in query:
            background_location=str(input())
            ctypes.windll.user32.SystemParametersInfoW(20, 
                                                       0, 
                                                       background_location,
                                                       0)
            speak("Background changed successfully")

# gets news headlines from tech catagory using news api
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

# couple of windows commands from shutdown, lock, etc
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

# asking about location opens google maps
        elif "where is" in query:
            query = query.replace("where is", "")
            location = query.strip()
            speak("User asked to Locate")
            speak(location)
            encoded_location = urllib.parse.quote(location)
            url=f"https://www.google.com/maps/search/?api=1&query={location.replace(' ', '+')}"
            webbrowser.open(url)
            print("Opening URL:", url)
# camera for taking pics 
        elif "camera" in query or "take a photo" in query:
            ec.capture(0, "Jarvis Camera ", "img.jpg")
        # note book to show write and clear it displayes note and its time later iam going to add date

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
            # using wolframalpha api to calculate any math problem
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

# displays weather info depend on city
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
            
        



        

        




    


