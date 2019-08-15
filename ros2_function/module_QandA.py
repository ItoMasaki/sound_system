import os
from pocketsphinx import LiveSpeech, get_model_path
import csv
from .import module_speak

counter = 0
question_dictionary = {}
noise_words = []
file_path = os.path.abspath(__file__)

# Define path
spr_dic_path = file_path.replace(
    'ros2_function/module_QandA.py', 'dictionary/spr_question.dict')
spr_gram_path = file_path.replace(
    'ros2_function/module_QandA.py', 'dictionary/spr_question.gram')
model_path = get_model_path()
csv_path = file_path.replace(
    'ros2_function/module_QandA.py', 'dictionary/QandA/qanda.csv')

# Make a dictionary from a csv file
with open(csv_path, 'r') as f:
    for line in csv.reader(f):
        question_dictionary.setdefault(str(line[0]), str(line[1]))

# Listen question, or speak the number of men and women
def QandA(person=None):

    global counter
    global question_dictionary
    global noise_words
    global live_speech

    # Speak the number of men and women, person = "the number of men|the number of women"
    if person != None:
        person = person.split("|")
        person_number = "There are {} people, the number of women is {}, the number of men is {}.".format((int(person[0]) + int(person[1])), person[0], person[1])            
        print(person_number)
        module_speak.speak(person_number)
    
    # Listen question   
    else:                    
        # Noise list
        noise_words = read_noise_word()
        
        # Make dict and gram files path
        dict_path = spr_dic_path
        gram_path = spr_gram_path
        
        # If I have a question witch I can answer, count 1
        while counter < 5:
            print("\n[*] LISTENING ...")
            # Setup live_speech
            setup_live_speech(False, dict_path, gram_path, 1e-10)
            for question in live_speech:
                #print(question)
                if str(question) not in noise_words:
                    if str(question) in question_dictionary.keys():
                        print("\n-------your question--------\n",str(question),"\n----------------------------\n")
                        print("\n-----------answer-----------\n",question_dictionary[str(question)],"\n----------------------------\n")
                        pause()
                        module_speak.speak(question_dictionary[str(question)])
                        counter += 1
                        break
                # noise
                else:
                    print(".*._noise_.*.")
                    print("\n[*] LISTENING ...")
                    pass
    #counter += 1 
    #return counter


# Stop lecognition
def pause():
    global live_speech
    live_speech = LiveSpeech(no_search=True)


# Make noise list
def read_noise_word():
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

# Setup livespeech
def setup_live_speech(lm, dict_path, jsgf_path, kws_threshold):
    global live_speech
    live_speech = LiveSpeech(lm=lm,
                             hmm=os.path.join(model_path, 'en-us'),
                             dic=dict_path,
                             jsgf=jsgf_path,
                             kws_threshold=kws_threshold)


if __name__ == '__main__':
    QandA()
