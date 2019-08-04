import os
import wave
from io import BytesIO
from pyaudio import PyAudio
from picotts import PicoTTS

picotts = PicoTTS()

#speak content
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
    
if __name__ == '__main__':
    speak("hello world")
