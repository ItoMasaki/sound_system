import os
from pocketsphinx import LiveSpeech, get_model_path
import csv
from . import module_speak

counter = 0
qa_dict = {}
noise_words = []
file_path = os.path.abspath(__file__)
spr_dic_path = file_path.replace(
    'ros2_function/module_QandA.py', 'dictionary/spr_question.dict')
spr_gram_path = file_path.replace(
    'ros2_function/module_QandA.py', 'dictionary/spr_question.gram')
model_path = get_model_path()
csv_path = file_path.replace(
    'ros2_function/module_QandA.py', 'dictionary/QandA/qanda.csv')
with open(csv_path, 'r') as f:
    for line in csv.reader(f):
        qa_dict.setdefault(str(line[0]), str(line[1]))

# listen question


def QandA():
    global counter
    global qa_dict
    global noise_words
    global live_speech

    # noise list
    noise_words = read_noise_word()
    # make dict and gram files path
    dict_path = spr_dic_path
    gram_path = spr_gram_path

    # if I have a question witch I can answer, count 1
    while counter < 5:
        print("\n[*] LISTENING ...")
        # setup live_speech
        setup_live_speech(False, dict_path, gram_path, 1e-10)
        for question in live_speech:
            if str(question) not in noise_words:
                if str(question) in qa_dict.keys():
                    print("\n-------your question--------\n",
                          str(question), "\n----------------------------\n")
                    print("\n-----------answer-----------\n",
                          qa_dict[str(question)], "\n----------------------------\n")
                    pause()
                    module_speak.speak(qa_dict[str(question)])
                    counter += 1
                    break
            # noise
            else:
                print(".*._noise_.*.")
                break


def pause():
    global live_speech
    live_speech = LiveSpeech(no_search=True)


# make noise list
def read_noise_word():
    words = []
    with open(spr_gram_path) as f:
        for line in f.readlines():
            if "<noise>" not in line:
                continue
            if "<rule>" in line:
                continue
            line = line.replace("<noise>", "").replace("=", "").replace(
                " ", "").replace("\n", "").replace(";", "")
            words = line.split("|")
    return words

# setup livespeech


def setup_live_speech(lm, dict_path, jsgf_path, kws_threshold):
    global live_speech
    live_speech = LiveSpeech(lm=lm,
                             hmm=os.path.join(model_path, 'en-us'),
                             dic=dict_path,
                             jsgf=jsgf_path,
                             kws_threshold=kws_threshold)


if __name__ == '__main__':
    QandA()
