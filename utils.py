from cgitb import text
from time import sleep
from gtts import gTTS
import pyaudio
import speech_recognition as sr
import wave
  
import subprocess
import os

#CONSTANTS
user = os.getenv("USER")
music_directory="/home/%s/Music" % user

def recording(SECONDS): # Record method args(RECORD_TIME)
        
    OUTPUT_FILENAME = "record.wav" # Name of output         
    audio = pyaudio.PyAudio() #PyAudio Init

    stream = audio.open(format=pyaudio.paInt16, channels=2,
            rate=44100, input=True,
            frames_per_buffer=1024) #Record Init
        
    frames = []

    for i in range(0, int(44100/1024*SECONDS )):
        data = stream.read(1024)
        frames.append(data)
        
    #Finish Recording

    stream.stop_stream()
    stream.close()
    audio.terminate()

    #Creating the WAV file

    file = wave.open(OUTPUT_FILENAME, 'wb')
    file.setnchannels(2)
    file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    file.setframerate(44100)
    file.writeframes(b''.join(frames))
    file.close()

def tex2voice(text):
    language = 'en'
    myobj = gTTS(text=text, lang=language, slow=False)
    myobj.save("echo.mp3")
    os.system("mpg321 echo.mp3")

def play_music(path):
    music_process = subprocess.Popen(["cvlc",path])
    music_on = True
    recognizer = sr.Recognizer() #Init the audio recognizer
    record_file = sr.AudioFile('record.wav') #Select the file
    while music_on:

        recording(3)

        recognizer = sr.Recognizer() #Init the audio recognizer
        record_file = sr.AudioFile('record.wav') #Select the file

        with record_file as source:
            audio = recognizer.record(source)

        try:
            textFromAudio = recognizer.recognize_google(audio).lower() #Using the google API we translate the audio 
        except:
            continue

        if "stop" in textFromAudio:
            music_process.kill()
            music_on=False

def echo_call(recognizer,record_file):
    echo=False
    while not echo:
        recording(3)
        with record_file as source:
            audio = recognizer.record(source)

        try:
            textFromAudio = recognizer.recognize_google(audio).lower() #Using the google API we translate the audio 
        except:
            continue

        if "echo" in textFromAudio:
            echo=True


def order_call(recognizer,record_file):

    recording(3)
    with record_file as source:
        audio = recognizer.record(source)

    try:
        textFromAudio = recognizer.recognize_google(audio).lower() #Using the google API we translate the audio
        if "play music" in textFromAudio:
            play_music(music_directory)
        elif "open" in textFromAudio:
            textFromAudio=textFromAudio.replace("open","")
            os.system("%s" % textFromAudio)
        else:
            tex2voice("Sorry, I can't understand you")
    except:
        tex2voice("Sorry, I can't hear you") #I can't hear you



