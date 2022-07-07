import speech_recognition as sr
import utils
import os
import subprocess

recognizer = sr.Recognizer() #Init the audio recognizer
record_file = sr.AudioFile('record.wav') #Select the file

while True:

    utils.echo_call(recognizer,record_file)
    utils.tex2voice("Hello! What do you need?")
    utils.order_call(recognizer,record_file)

