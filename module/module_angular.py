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
spr_gram_path = file_path.replace(
    'module/module_QandA.py', 'dictionary/spr_question.gram')

# PARAMETERS for sound localization
PARAMETERS = {
    'DOAANGLE': (21, 0, 'int', 359, 0, 'ro', 'DOA angle. Current value. Orientation depends on build configuration.'),
    'SPEECHDETECTED': (19, 22, 'int', 1, 0, 'ro', 'Speech detection status.', '0 = false (no speech detected)',
                       '1 = true (speech detected)')
}

TIMEOUT = 100000

# Find angular
def angular(dictionary):

    ###############
    #
    # use this module to find angular
    #
    # param >> dictionary: dict and gram file's name
    #
    # return >> angular
    #
    ###############
    
    global live_speech
    
    # Noise list
    noise_words = read_noise_word()
    
    setup_live_speech(
        False,
        file_path.replace('module/module_angular.py',
                          '/dictionary/{}.dict').format(str(dictionary)),
        file_path.replace('module/module_angular.py',
                          '/dictionary/{}.gram').format(str(dictionary)),
        1e-10)
    
    while True:
        counter = 0
        if read('SPEECHDETECTED') == 1:
            for phrase in live_speech:
                angular = direction()
                #print(phrase)
                if str(dintionary) == "spr_question":
                    if str(phrase) not in noise_words:
                        counter += 1
                        print(str(counter) + ':' + str(angular), flush=True)
                        return angular

                elif str(dintionary) == "hey_ducker":
                    if 'hey ducker' == str(phrase):
                        print("angular" + ':' + str(angular), flush=True)
                        return angular

def read_noise_word():
    
    ###############
    #
    # use this module to put noise to list
    #
    # param >> None
    #
    # return >> words: list in noises
    #
    ###############
    
    words = []
    with open(spr_gram_path) as f:
        for line in f.readlines():
            if "<noise>" not in line:
                continue
            if "<rule>" in line:
                continue
            line = line.replace("<noise>", "").replace(
                    " = ", "").replace("\n", "").replace(";", "")
            words = line.split(" | ")
    return words

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
    
    ###############
    #
    # use this module to set live speech parameter
    #
    # param >> lm: False >> means useing own dict and gram
    # param >> dict_path: ~.dict file's path
    # param >> jsgf_path: ~.gram file's path
    # param >> kws_threshold: mean's confidence (1e-○)
    #
    # return >> None
    #
    ###############
    
    global live_speech
    live_speech = LiveSpeech(lm=lm,
                             hmm=os.path.join(model_path, 'en-us'),
                             dic=dict_path,
                             jsgf=jsgf_path,
                             kws_threshold=kws_threshold)


if __name__ == '__main__':
    angular()
