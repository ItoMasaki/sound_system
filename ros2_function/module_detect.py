import os
import wave
from io import BytesIO
from pyaudio import PyAudio
from picotts import PicoTTS
from pocketsphinx import LiveSpeech, get_model_path

import module_speak

hotword_dic_path = "../dictionary/hey_ducker.dict"
hotword_gram_path = "../dictionary/hey_ducker.gram"
model_path = get_model_path()
picotts = PicoTTS()
  
#detect hotword      
def detect():
    print("[*] START HOTWORD RECOGNITION")
    setup_live_speech(False, hotword_dic_path, hotword_gram_path, 1e-20)
    global live_speech
    # if detect hotword, delete live_speech
    for phrase in live_speech:
        print(phrase)
        if "hey ducker" == str(phrase):
            module_speak.speak("yes sir !")
            live_speech.stop = True
            del(live_speech)
            break
            
# setup livespeech
def setup_live_speech(lm, dict_path, jsgf_path, kws_threshold):
    global live_speech
    live_speech = LiveSpeech(lm=lm,
                             hmm=os.path.join(model_path, 'en-us'),
                             dic=dict_path,
                             jsgf=jsgf_path,
                             kws_threshold=kws_threshold)

if __name__ == '__main__':                       
    detect()
