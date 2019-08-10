import os
import wave
import pyttsx3


# Speak content
def speak(content):
    print("[*] SPEAK : {0}".format(content),flush=True)
    engine=pyttsx3.init()
    rate=engine.getProperty('rate')
    engine.setProperty('rate', 150)
    engine.say(content)
    engine.runAndWait()
    engine.stop()
    
if __name__ == '__main__':
    speak("hello world")
