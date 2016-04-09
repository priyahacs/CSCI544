__author__ = 'Padma'
import sys
import os
import fnmatch
import math
root = sys.argv[1]
outputFile = open("nboutput.txt", 'w')


stop_words = {'at':1,'they':1,'me':1,'my':1,'from':1,'this':1,'so':1,'am':1,'had':1,'for':1,'we':1,'i':1,'the':1,'that':1,
              'to':1,'as':1, 'there':1, 'has':1, 'and':1, 'or':1, 'is':1, 'not':1, 'a':1, 'of':1, 'but':1, 'in':1, 'by':1,
              'on':1,'are':1, 'it':1, 'if':1, 'was':1,'can':1,'will':1,'be':1,'he':1,'get':1,'an':1,'our':1, 'be':1,'most':1,
              'because':1,'were':1,'what':1,'he':1,'she':1,'your':1,'with':1,'their':1,'could':1,'would':1,'have':1,'then':1,
              'where':1,'them':1,'into':1,'when':1,'us':1,'who':1,'which':1,'you':1,'than':1,'while':1,'lets':1,'i''ll':1,
              'hotel':1,'up':1,'down':1,'been':1,'make':1,'should':1,'how':1}

punctuations = ["!", ".", ",", "","-","@",'#','%','&','*','^','~','`',':',';',"?"]

newDict = {}


with open('nbmodel.txt', 'r') as f:
    for i, line in enumerate(f):
        if i == 0:
            prior = line.split()
        else:
            splitLine = line.split()
            newDict[splitLine[0]] = ",".join(splitLine[1:])

if (len(prior) == 4):

    prior_pos  = float(prior[0])
    prior_neg  = float(prior[1])
    prior_truth  = float(prior[2])
    prior_decep = float(prior[3])
else:
    prior_pos = 0.5
    prior_neg = 0.5
    prior_truth = 0.5
    prior_decep = 0.5

for root,dirs,files in os.walk(root, topdown=False):
    for name in fnmatch.filter(files,"*.txt"):
        if name == "README.txt":
            continue
        temp = ""
        final = []
        file = os.path.join(root, name)
        f1 = open(file, "r")
        temp = f1.read()
        split = temp.split()
        for i in range(0,len(split)):
            preprocess = split[i].lower().rstrip('\'\"-,.:;!?)&').lstrip('(-')
            if (preprocess not in punctuations and preprocess not in stop_words):
                final.append(preprocess)

        pos_prob = float()
        neg_prob = float()
        truth_prob = float()
        deceptive_prob = float()

        for j in range(0,len(final)):
            text =final[j]
            if text in newDict.keys():

                values = newDict.get(text).split(',')

                if(len(values) == 4):
                    pos_val = float(values[0])
                    neg_val = float(values[1])
                    truth_val = float(values[2])
                    deceptive_val = float(values[3])


                    if (j == 0):

                        pos_prob = math.log(prior_pos,10) + math.log(pos_val,10)
                        neg_prob = math.log(prior_neg,10) + math.log(neg_val,10)
                        truth_prob = math.log(prior_truth,10) +math.log(truth_val,10)
                        deceptive_prob = math.log(prior_decep,10) + math.log(deceptive_val,10)

                    else:

                        pos_prob = pos_prob + math.log(pos_val,10)
                        neg_prob = neg_prob +math.log(neg_val,10)
                        truth_prob = truth_prob+math.log(truth_val,10)
                        deceptive_prob = deceptive_prob+math.log(deceptive_val,10)

        if (truth_prob >= deceptive_prob):
            outputFile.write("truthful"+" ")
        else:
            outputFile.write("deceptive"+" ")

        if(pos_prob >= neg_prob):
            outputFile.write("positive"+ " ")
        else:
            outputFile.write("negative"+ " ")

        outputFile.write(file+"\n")

outputFile.close()