import wave
from io import BytesIO
from pyaudio import PyAudio
from picotts import PicoTTS

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

from rclpy.qos import qos_profile_sensor_data

class SoundSystem(Node):
    def __init__(self):
        super(SoundSystem, self).__init__("SoundSystem")

        self.create_subscription(String,\
                                 "sound_system/command",\
                                 self.command_callback,\
                                 qos_profile_sensor_data)

        self.command = None

        self.picotts = PicoTTS()

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

            if "speak" == command[0].strip("Command:"):
                self.speak(command[1].strip("Content:"))

    # speak content
    def speak(self, content):
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
        pass

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
