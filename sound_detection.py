import usb.core
import usb.util
import time
import os
import sys
from pocketsphinx import LiveSpeech,get_model_path
import struct
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from rclpy.qos import qos_profile_sensor_data

dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)

PARAMETERS = {
    'DOAANGLE': (21, 0, 'int', 359, 0, 'ro', 'DOA angle. Current value. Orientation depends on build configuration.'),
    'SPEECHDETECTED': (19, 22, 'int', 1, 0, 'ro', 'Speech detection status.', '0 = false (no speech detected)',
                       '1 = true (speech detected)')
}

TIMEOUT = 100000

class SoundDetection(Node):
    def __init__(self,dic_path,gram_path):
        super().__init__('SoundDetection')

        self.pub = self.create_publisher(Float64, 'sound_system/direction',qos_profile_sensor_data)
        self.cnt=0

        self.dic_path=dic_path
        self.gram_path=gram_path
        self.hmm=os.path.join(get_model_path,'en-us')
        self.get_array()

    def get_array(self):
        if dev:
            speech=self.setup_live_speech(False,self.hmm,self.dic_path,self,gram_path,1e-20)
            while True:
                try:
                    if read('SPEECHDETECTED')==1:
                        for kw in speech:
                            temp=direction()
                            if kw !=" ":
                                self.cnt+=1
                                print(cnt+":"+temp,flush=True)
                                self.pub.publish(temp)

    @staticmethod
    def setup_live_speech(self, lm,hmm, dict_path, jsgf_path, kws_threshold):
        self.live_speech = LiveSpeech(lm=lm,
                                      hmm=hmm,
                                      dic=dict_path,
                                      jsgf=jsgf_path,
                                      kws_threshold=kws_threshold)


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


    @staticmethod
    def direction():
        read('DOAANGLE')

def main():
    rclpy.init()
    node=SoundDetection("sound_system/dictionary/hey_ducker.dict","sound_system/dictionary/hey_ducker.gram")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()