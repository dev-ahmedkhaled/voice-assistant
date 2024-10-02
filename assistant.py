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
import os
import winshell
import pyjokes
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
# we set up engine to pyttsx3 we use it to convert txt to speech
# and sapi5 is a microsoft speech applictaion platform

load_dotenv()

# this to start our engine 
engine=pyttsx3.init('sapi5')

voices=engine.getProperty('voices')
# we set our engine to talk male voice with this
engine.setProperty('voice',voices[0].id)
# we make a function so make the assistant talk whenever we want
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# here we get date and time and we use the above function to make the assistant say it out
def wishMe():
    global assistant_name
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak('Good morning sir')
    elif hour>=12 and hour<18:
        speak('good afternoon sir')
    else:
        speak('good evening sir')
    
    assistant_name=('jarvis')
    speak('iam your assistant')
    speak(assistant_name)


def wake_up():
    
    #Listen for the wake word 'Jarvis' using Porcupine voice recognition.
    #When detected, prompt the user for assistance.
    
    access_key = os.getenv('wake_up_key')
    porcupine = pvporcupine.create(keywords=["jarvis"],access_key=access_key)
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(rate=porcupine.sample_rate,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,
                        frames_per_buffer=porcupine.frame_length)

    print("Listening for the wake word 'Jarvis'...")
    while True:
        #this we use audio_stream to stream audio then porcupine.frame_length determines number of sample read at once 
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        #this checks if the word is jarvis or not if yes it returns a value bigger than or equal 0 if not returns -1

        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            print("Wake word detected!")
            speak("Yes, how can I help you?")
            audio_stream.close()
            porcupine.delete()
            break


def user_name():
    speak('what should i call you sir')
    global username
    username = takeCommand()
    speak('welcome sir')
    speak(username)
    #to get current width of the terminal
    columns=shutil.get_terminal_size().columns
    print('#####################'.center(columns))
    print('      welcome Mr.',username.center(columns))
    print('#####################'.center(columns))

    speak('how may i assist you today')


def takeCommand():
    # this makes a recognizer object aka someone listening
    r=sr.Recognizer()
# this opens the mic so the r can listen
    with sr.Microphone() as source:
        print('listening...')
    # this the time taken before user done talking
        r.pause_threshold=1
        # we saved the audio in a variable called audio
        audio=r.listen(source)
    try:
        print('recognizing...')
        #we sent the audio to google web speech api for speech recognition
        query=r.recognize_google(audio, language='en-US') #en in is english in us
        print(f'user said:{query}\n')
    except Exception as e:
        print(e)
        print('unable to recogize your voice')
        return 'None'
    return query



def sendEmail(to,content):
    #this creates a gmail simple mail transfer protocol server for sending emails through python script
    server =smtplib.SMTP('smtp.gmail.com',587)
    # we use this to identify the program also known as client to email server and to ask wht feature the server supports 
    server.ehlo()
    # it upgrades the silmple plain text smtp to a secure encrypted connection 
    server.starttls()
    email=os.getenv('main_email')
    passs=os.getenv('main_email_pass')


    server.login(email,passs)
    server.sendmail(email,to,content)
    server.close()


def play_song(index):
    os.startfile(os.path.join(music_dir, songs[index]))

music_dir = os.getenv('music_dir')
songs = os.listdir(music_dir)
current_song_index = 0


if __name__=='__main__':
    clear = lambda:os.system('cls')

    clear()
    wishMe()
    user_name()

    while True:
        wake_up()
        query= takeCommand().lower()


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
        
        elif 'open stackoverflow' in query:
            speak('opening stack over flow')
            webbrowser.open('stackoverflow.com')

        elif 'play music' in query or 'play song' in query:
            speak('opening media player')
            music_dir=os.getenv('music_dir')
            songs= os.listdir(music_dir)
            print(songs)
            random = os.startfile(os.path.join(music_dir,songs[1]))
        
        elif 'the time' in query or 'what the time' in query:
            strtime=datetime.datetime.now().strftime('%I and %M minutes and %S seconds %p')
            speak(f'the time now is{strtime}')
            print(f'the time now is {strtime}')

        
        elif 'open opera' in query:
            code_path=os.getenv('opera_dir')
            os.startfile(code_path)

        elif 'play next song' in query or 'next' in query:
            current_song_index=(current_song_index+1)%len(songs)
            play_song(current_song_index)
        
        elif 'play pervious song' in query or 'back' in query:
            current_song_index=(current_song_index-1)%len(songs)
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

        elif 'fine' in query or 'good' in query:
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
            location = query
            speak("User asked to Locate")
            speak(location)
            webbrowser.open("https://www.google.nl / maps / place/" + location + "")

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


        

        




    



