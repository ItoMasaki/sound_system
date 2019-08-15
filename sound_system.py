import os
import struct
import sys
import time

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from ros2_function import module_angular
from ros2_function import module_QandA
from ros2_function import module_detect
from ros2_function import module_speak

from std_msgs.msg import String


class SoundSystem(Node):
    def __init__(self):
        super(SoundSystem, self).__init__('SoundSystem')
        
        self.command = None
        
        self.create_subscription(
            String, 'sound_system/command',
            self.command_callback)

    # recieve a command {Command, Content}
    def command_callback(self, msg):

        self.command = msg.data
        command = msg.data.split(',')
        
        # Detect hotword, "hey ducker"
        if 'detect' == command[0].replace('Command:', ''):
            if module_detect.detect() == 1:
                self.cerebrum_publisher('Return:1,Content:None')
            else:
                self.cerebrum_publisher('Return:0,Content:None')
        
        # Speak a content
        if 'speak' == command[0].replace('Command:', ''):
            if module_speak.speak(command[1].replace('Content:', '')) == 1:
                self.cerebrum_publisher('Return:1,Content:None')
            else:
                self.cerebrum_publisher('Return:0,Content:None')
        
        # Sound localization
        if 'angular' == command[0].replace('Command:', ''):
            self.temp_angular = module_angular.angular()
            if self.temp_angular > 0:
                self.cerebrum_publisher(
                    'Return:1,Content:'+str(self.temp_angular))
            else:
                self.cerebrum_publisher('Return:0,Content:None')

        # Start QandA, an act of repeating 5 times
        times = 0 
        if 'QandA' == command[0].replace('Command:', ''):
            times = int(command[1].replace('Content:', ''))
            if module_QandA.QandA(times) == 1:
                    self.cerebrum_publisher('Retern:0,Content:None')   
            else:
                self.cerebrum_publisher('Return:0.Content:None')

    # Publish a result of an action
    def cerebrum_publisher(self, message):
        self.senses_publisher = self.create_publisher(
            String, 'cerebrum/command')

        _trans_message = String()
        _trans_message.data = message

        self.senses_publisher.publish(_trans_message)
        # self.destroy_publisher(self.senses_publisher)


def main():
    rclpy.init()
    node = SoundSystem()
    rclpy.spin(node)


if __name__ == '__main__':
    main()
