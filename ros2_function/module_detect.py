import os
import wave
from io import BytesIO
from pyaudio import PyAudio
from picotts import PicoTTS
from pocketsphinx import LiveSpeech, get_model_path

hotword_dic_path = "../dictionary/hey_ducker.dict"
hotword_gram_path = "../dictionary/hey_ducker.gram"
model_path = get_model_path()
picotts = PicoTTS()
        
def detect():
    print("[*] START HOTWORD RECOGNITION")
    setup_live_speech(False, hotword_dic_path, hotword_gram_path, 1e-20)
    global live_speech
    # if detect hotword, delete live_speech
    for phrase in live_speech:
        print(phrase)
        if "hey ducker" == str(phrase):
            speak("yes sir !")
            live_speech.stop = True
            del(live_speech)
            break
                    
def speak(content):
    print("[*] SPEAK : {0}".format(content))
    p = PyAudio()
    waves = picotts.synth_wav(content)
    wav = wave.open(BytesIO(waves))
    stream = p.open(format=p.get_format_from_width(wav.getsampwidth()),\
                              channels=wav.getnchannels(),\
                              rate=16000,\
                              output=True)

    data = wav.readframes(1024)
    while data != b'':
        stream.write(data)
        data = wav.readframes(1024)

    stream.stop_stream()
    stream.close()
    p.terminate()
            
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
