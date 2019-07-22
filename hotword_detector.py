import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from pocketsphinx import LiveSpeech,get_model_path


class HotwordDetector(Node):
    def __init__(self):
        super().__init__("HotwordDetector")

        self.publisher=self.create_publisher(String,"sound_system/command")

        self.msg=String()
        self.msg.data="Command:detect , Content: "
        self.model_path=get_model_path()
        self.dic_path = dic_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"dictionary")
        self.live_speech=None
        self.pause()

        self.init_detector()

    def pause(self):
        print("== STOP RECOGNITION ==")
        self.live_speech = LiveSpeech(no_search=True)

    def resume(self):
        print("== START RECOGNITION ==")
        self.live_speech = LiveSpeech(
            lm=False,
            hmm=os.path.join(self.model_path, 'en-us'),
            dic='/home/matsudayamato/python_ws/src/sound_system/dictionary/hey_ducker.dict',
	        jsgf='/home/matsudayamato/python_ws/src/sound_system/dictionary/hey_ducker.gram',
	        kws_threshold=1e-0,
	        no_search=False,
            )

    def init_detector(self):
        print('__file__:    ', __file__)
        print("Hotword detection start")
        self.resume()
        for phrase in self.live_speech:
            if str(phrase)!="" :
                print("--"+str(phrase)+"--")
                self.publisher.publish(self.msg)
                self.pause()
                break
def main():
    rclpy.init()
    node = HotwordDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

