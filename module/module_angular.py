from threading import Thread

import usb
import usb.core
import usb.util
import time
import os
import sys
import struct

from pocketsphinx import LiveSpeech, get_model_path

live_speech=None
dev = usb.core.find(idVendor=0x2886,idProduct=0x0018)
file_path = os.path.abspath(__file__)
model_path = get_model_path()

# Define path
spr_dic_path = file_path.replace(
    'module/module_angular.py', '/dictionary/spr_question.dict')
spr_gram_path = file_path.replace(
    'module/module_angular.py', '/dictionary/spr_question.gram')

# PARAMETERS for sound localization
PARAMETERS = {
    'DOAANGLE': (21, 0, 'int', 359, 0, 'ro', 'DOA angle. Current value. Orientation depends on build configuration.'),
    'SPEECHDETECTED': (19, 22, 'int', 1, 0, 'ro', 'Speech detection status.', '0 = false (no speech detected)',
                       '1 = true (speech detected)')
}

TIMEOUT = 100000

# Find angular
def angular():
    global live_speech
    
    setup_live_speech(
        False,
        spr_dic_path,
        spr_gram_path,
        1e-10)
    
    while True:
        counter = 0
        if read('SPEECHDETECTED') == 1:
            for question in live_speech:
                angular = direction()
                #print(question)
                if str(question) not in noise_words:
                    if str(question) in question_dictionary.keys():
                        counter += 1
                        print(str(counter) + ':' + str(angular), flush=True)
                        return angular

                # noise
                else:
                    #print(".*._noise_.*.")
                    #print("\n[*] LISTENING ...")
                    pass


def read(param_name):

    try:
        data = PARAMETERS[param_name]
    except KeyError:
        return

    cmd = 0x80 | data[1]
    
    if data[2] == 'int':
        cmd |= 0x40
    
    id = data[0]
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


def direction():
    return read('DOAANGLE')

# Setup livespeech
def setup_live_speech(lm, dict_path, jsgf_path, kws_threshold):
    global live_speech
    live_speech = LiveSpeech(lm=lm,
                             hmm=os.path.join(model_path, 'en-us'),
                             dic=dict_path,
                             jsgf=jsgf_path,
                             kws_threshold=kws_threshold)


if __name__ == '__main__':
    angular()
