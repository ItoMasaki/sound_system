import os
from pocketsphinx import LiveSpeech, get_model_path
import csv
import module_speak

counter = 0
qa_dict = {}
noise_words = []

spr_dic_path = "../dictionary/spr_question.dict"
spr_gram_path = "../dictionary/spr_question.gram"
model_path = get_model_path()

with open('../Q&A/q&a.csv', 'r') as f: 
    for line in csv.reader(f):
        qa_dict.setdefault(str(line[0]), str(line[1]))

# listen question
def QandA(person=None):
    global counter
    global qa_dict
    global noise_words
    global live_speech
    if person != None:
        person = person.split("|")
        if person[0] != "1" and person[1] != "1":
            person_number = "There are {} people, the number of men are {}, the number of femen are {}.".format((int(person[0]) + int(person[1])), person[0], person[1])
        elif person[0] != "1":
            person_number = "There are {} people, the number of men are {}, the number of femen is 1.".format((int(person[0]) + int(person[1])), person[0])
        elif person[1] != "1":
            person_number = "There are {} people, the number of men is 1, the number of femen are {}.".format(int(person[0]) + int(person[1]), person[1])

        print(person_number)
        module_speak.speak(person_number)
        
    else:                    
        #noise list
        noise_words = read_noise_word()
        # make dict and gram files path
        dict_path = spr_dic_path
        gram_path = spr_gram_path
        
        # if I have a question witch I can answer, count 1
        while counter < 2:
            print("\n[*] LISTENING ...")
            # setup live_speech
            setup_live_speech(False, dict_path, gram_path, 1e-10)
            for question in live_speech:
                if str(question) not in noise_words:
                    if str(question) in qa_dict.keys():
                        print("\n-------your question--------\n",str(question),"\n----------------------------\n")
                        print("\n-----------answer-----------\n",qa_dict[str(question)],"\n----------------------------\n")
                        pause()
                        module_speak.speak(qa_dict[str(question)])
                        counter += 1
                        break
                #noise
                else:
                    print(".*._noise_.*.")
                    print("\n[*] LISTENING ...")
                    pass
    #counter += 1 
    #return counter

def pause():
    global live_speech
    live_speech = LiveSpeech(no_search=True)
    

#make noise list
def read_noise_word():
    words = []
    with open(spr_gram_path) as f:
        for line in f.readlines():
            if "<noise>" not in line:
                continue
            if "<rule>" in line:
                continue
            line = line.replace("<noise>", "").replace("=", "").replace(" ", "").replace("\n", "").replace(";", "")
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
