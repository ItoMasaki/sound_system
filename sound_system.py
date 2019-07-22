import os
import wave
from io import BytesIO
from pyaudio import PyAudio
from picotts import PicoTTS
from pocketsphinx import LiveSpeech,get_model_path
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from std_msgs.msg import String
import snowboy.snowboydecoder
import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from pocketsphinx import LiveSpeech,get_model_path

class HotwordDetector(Node):
    def __init__(self):
        super().__init__("HotwordDetector")

        self.publisher=self.create_publisher(String,"sound_sytem/command")

        self.msg=String()
        self.msg.data="Command:speak , Content:hello!"
        self.model_path=get_model_path()
        self.dic_path = dic_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"dictionary")
        self.livespeech=LiveSpeech(
            lm=False,
            hmm=os.path.join(self.model_path, 'en-us'),
            dic='/home/matsudayamato/python_ws/src/sound_system/dictionary/ros2_sound_system_sphinx.dict',
	        jsgf='/home/matsudayamato/python_ws/src/sound_system/dictionary/ros2_sound_system_sphinx.gram',
            kws_threshold=1e-30
            )

        self.init_detector()

    def init_detector(self):

        print("Hotword detection start")
        for phrase in self.livespeech:
            if str(phrase)!="" :
                print("--"+str(phrase)+"--")
                self.publisher.publish(self.msg)


class SoundSystem(Node):
    def __init__(self):
        super(SoundSystem, self).__init__("SoundSystem")

        self.create_subscription(String,\
                                 "sound_system/command",\
                                 self.command_callback)
        self.command = None

        self.picotts = PicoTTS()

        self.model_path = get_model_path()
        self.dic_path = dic_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"dictionary/ros2_sound_system_sphinx.dict"),
        self.gram_path=  dic_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"dictionary/ros2_sound_system_sphinx.gram"),
        self.live_speech = LiveSpeech(
            lm=False,
            hmm=os.path.join(self.model_path, 'en-us'),
            dic=self.dic_path,
	        jsgf=self.gram_path)


    # recieve a command {Command, Content}
    def command_callback(self, msg):
        #+++++++++++++++++++++++++++++++#
        #
        #   Data :
        #       Type    : speak
        #       Content : ~~~~
        #
        #
        #+++++++++++++++++++++++++++++++#


        if self.one_time_execute(msg.data, self.command):

            self.command = msg.data

            # Command:speak , Content:hello!
            command = msg.data.split(" , ")

            if "speak" == command[0].replace("Command:", ""):
                self.Speak(command[1].replace("Content:", ""))

            if "listen" == command[0].replace("Command:", ""):
                self.Listen()

    # speak content
    def Speak(self, content):
        print("[*] Speak : {0}".format(content))
        p = PyAudio()
        waves = self.picotts.synth_wav(content)
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

    # [TODO] please build this function!
    def Listen(self):
        print("[*] Listening")
        for phrase in self.live_speech:
            print(phrase)

    # only one time execute
    def one_time_execute(self, now, previous):
        flag = False

        if now != previous:
            flag = True

        return flag


def main():
    rclpy.init()
    node = SoundSystem()
    rclpy.spin(node)
