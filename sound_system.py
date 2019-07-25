import os
import wave
from io import BytesIO
from pyaudio import PyAudio
from picotts import PicoTTS
from pocketsphinx import LiveSpeech, get_model_path

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from std_msgs.msg import String,Float64


from threading import Thread

import usb
import usb.core
import usb.util
import time
import os
import sys
import struct

dev = usb.core.find(idVendor=0x2886,idProduct=0x0018)

PARAMETERS = {
    'DOAANGLE': (21, 0, 'int', 359, 0, 'ro', 'DOA angle. Current value. Orientation depends on build configuration.'),
    'SPEECHDETECTED': (19, 22, 'int', 1, 0, 'ro', 'Speech detection status.', '0 = false (no speech detected)',
                       '1 = true (speech detected)')
}

TIMEOUT = 100000

class SoundSystem(Node):
    def __init__(self):
        super(SoundSystem, self).__init__("SoundSystem")

        # ROS2
        self.create_subscription(String, "sound_system/command", self.command_callback, qos_profile_sensor_data)
        self.command = None

        self.pub = self.create_publisher(Float64,"sound_system/direction",qos_profile_sensor_data)
        # Speak
        self.picotts = PicoTTS()
        # Pocketsphinx
        self.hotword_dic_path = "sound_system/dictionary/hey_ducker.dict"
        self.hotword_gram_path = "sound_system/dictionary/hey_ducker.gram"
        self.model_path = get_model_path()
        # respeaker
        self.dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
        self.counter = 0
        ###debug###
        self.listen('hey_ducker')



    # recieve a command {Command, Content}
    def command_callback(self, msg):

        # if msg.data is defferent from self.command, one time execute command recieved.
        if self.one_time_execute(msg.data, self.command):

            self.command = msg.data

            # split " , "
            command = msg.data.split(" , ")

            if "setup" == command[0].replace("Command:", ""):
                self.setup_topic(command[1].replace("Content:", ""))

            if "detect" == command[0].replace("Command:", ""):
                self.detect()

            if "speak" == command[0].replace("Command:", ""):
                self.speak(command[1].replace("Content:", ""))

            if "listen" == command[0].replace("Command:", ""):
                self.listen(command[1].replace("Content:", ""))


    # detect hotword
    def detect(self):
        print("[*] START HOTWORD RECOGNITION")
        self.setup_live_speech(False, self.hotword_dic_path, self.hotword_gram_path, 1e-20)

        # if detect hotword, delete live_speech
        for phrase in self.live_speech:
            print(phrase)
            if "hey ducker" == str(phrase):
                self.speak("yes sir !")
                self.live_speech.stop = True
                del(self.live_speech)
                break


    # speak content
    def speak(self, content):
        print("[*] SPEAK : {0}".format(content))
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


    # listen any drammers
    def listen(self, file_name):

        # make dict and gram files path
        dict_path = self.hotword_dic_path
        gram_path = self.hotword_gram_path
        # setup live_speech
        self.setup_live_speech(False, dict_path, gram_path, 1e-10)

        print("[*] LISTENING ...")

        self.get_array()


    # get array from respeaker
    def get_array(self):
        while True:
            if self.read('SPEECHDETECTED') == 1:
                for kw in self.live_speech:
                    angular = self.direction()
                    if kw != " ":
                        self.counter += 1
                        print(str(self.counter) + ":" + str(angular), flush=True)
                        #self.pub.publish(float(angular))


    # read buffer data from respeaker
    @staticmethod
    def read(param_name):

        try:
            data = PARAMETERS[param_name]
        except KeyError:
            return

        id = data[0]

        cmd = 0x80 | data[1]
        if data[2] == 'int':
            cmd |= 0x40

        length = 8


        response = dev.ctrl_transfer(
            usb.util.CTRL_IN | usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE,
            0, cmd, id, length, TIMEOUT)

        response = struct.unpack(b'ii', response.tostring())

        if data[2] == 'int':
            result = response[0]
        else:
            result = response[0] * (2. ** response[1])


        return result


    # get direction
    def direction(self):
        return self.read('DOAANGLE')


    # setup livespeech
    def setup_live_speech(self, lm, dict_path, jsgf_path, kws_threshold):
        self.live_speech = LiveSpeech(lm=lm,
                                      hmm=os.path.join(self.model_path, 'en-us'),
                                      dic=dict_path,
                                      jsgf=jsgf_path,
                                      kws_threshold=kws_threshold)


    # setup publisher for return to root topic
    def setup_topic(self, topic_name):
        print("[*] CREATE PUBLISHER : TOPIC NAME IS [{0}]".format(topic_name))
        self.publisher = self.create_publisher(String, topic_name, qos_profile_sensor_data)


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
