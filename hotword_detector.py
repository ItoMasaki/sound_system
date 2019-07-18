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
def main():
    rclpy.init()
    node = HotwordDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
if __name__ == "__main__":
    main()