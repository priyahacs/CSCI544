__author__ = 'Padma'
import sys
import os
import fnmatch
import math
import string
root = sys.argv[1]

stop_words = {'at':1,'they':1,'me':1,'my':1,'from':1,'this':1,'so':1,'am':1,'had':1,'for':1,'we':1,'i':1,'the':1,'that':1,
              'to':1,'as':1, 'there':1, 'has':1, 'and':1, 'or':1, 'is':1, 'not':1, 'a':1, 'of':1, 'but':1, 'in':1, 'by':1,
              'on':1,'are':1, 'it':1, 'if':1, 'was':1,'can':1,'will':1,'be':1,'he':1,'get':1,'an':1,'our':1, 'be':1,'most':1,
              'because':1,'were':1,'what':1,'he':1,'she':1,'your':1,'with':1,'their':1,'could':1,'would':1,'have':1,'then':1,
              'where':1,'them':1,'into':1,'when':1,'us':1,'who':1,'which':1,'you':1,'than':1,'while':1,'lets':1,'i''ll':1,
              'hotel':1,'up':1,'down':1,'been':1,'make':1,'should':1,'how':1}

punctuations = ["!", ".", ",", "","-","@",'#','%','&','*','^','~','`',':',';',"?"]

positive_variable = []
negative_variable = []
truth_variable = []
deceptive_variable = []
all_variable = []

positive_dict={}
negative_dict ={}
truth_dict = {}
deceptive_dict ={}

pos_file_count = 0
neg_file_count = 0
truth_file_count = 0
decep_file_count = 0
total_file_count = 0

for root,dirs,files in os.walk(root, topdown=False):
    for name in fnmatch.filter(files,"*.txt"):
        if name == "README.txt":
            continue
        files = os.path.join(root, name)
        f1 = open(files, "r")
        sep = f1.read()

        sep1 = sep.translate(None,string.punctuation).lower()
        sep2 = sep1.split()
        if "positive" in files:
            for word in sep2:
                if word not in stop_words:
                    positive_dict[word] = positive_dict.get(word,0)+1
                    positive_variable.append(word)
                    all_variable.append(word)
            pos_file_count += 1

        if "negative" in files:
            for word in sep2:
                if word not in stop_words:
                    negative_dict[word] = negative_dict.get(word,0)+1
                    negative_variable.append(word)
                    all_variable.append(word)
            neg_file_count +=1

        if "deceptive" in files:
            for word in sep2:
                if word not in stop_words:
                    deceptive_dict[word] = deceptive_dict.get(word,0)+1
                    deceptive_variable.append(word)
                    all_variable.append(word)
            decep_file_count +=1


        if "truth" in files:
            for word in sep2:
                if word not in stop_words:
                    truth_dict[word] = truth_dict.get(word,0)+1
                    truth_variable.append(word)
                    all_variable.append(word)
            truth_file_count +=1

        total_file_count +=1
        f1.close()



pos_prior = float(pos_file_count)/float(total_file_count)
neg_prior =  float(neg_file_count)/float(total_file_count)
decep_prior = float(decep_file_count)/float(total_file_count)
truth_prior =  float(truth_file_count)/float(total_file_count)



positive_length = len(positive_variable)
negative_length = len(negative_variable)
truth_length = len(truth_variable)
deceptive_length = len(deceptive_variable)



all_variable1 = list(set(all_variable))
all_var_length = len(all_variable1)


model = open("nbmodel.txt","w")


pos_prob = float()
neg_prob = float()
truth_prob = float()
deceptive_prob = float()

model.write(str(pos_prior)+"\t")
model.write(str(neg_prior)+"\t")
model.write(str(truth_prior)+"\t")
model.write(str(decep_prior)+"\n")



for j in range (0,len(all_variable1)):

    pos_count = 0
    neg_count = 0
    truth_count = 0
    deceptive_count = 0
    text = all_variable1[j]
    model.write(text+"\t\t\t")
    if text in positive_dict.keys():
        pos_count = positive_dict.get(text)+1
    else:
        pos_count = 1

    p1 = round((float(pos_count)/float(positive_length+all_var_length)),6)
    pos_prob = pos_prob+p1
    model.write(str(p1)+"\t")

    if text in negative_dict.keys():
        neg_count = negative_dict.get(text)+1
    else:
        neg_count = 1

    p2 = round((float(neg_count)/float(negative_length+all_var_length)),6)
    neg_prob = neg_prob+p2
    model.write(str(p2)+"\t")

    if text in truth_dict.keys():
        truth_count = truth_dict.get(text)+1
    else:
        truth_count = 1

    p3 = round((float(truth_count)/float(truth_length+all_var_length)),6)
    truth_prob = truth_prob+p3
    model.write(str(p3)+"\t")

    if text in deceptive_dict.keys():
        deceptive_count = deceptive_dict.get(text)+1
    else:
        deceptive_count = 1

    p4 = round((float(deceptive_count)/float(deceptive_length+all_var_length)),6)
    deceptive_prob = deceptive_prob+p4
    model.write(str(p4)+"\n")

model.close()

