__author__ = 'Preethi'
import sys

file_name = sys.argv[1]
input = open(file_name,"r")
model_file = open("hmmmodel.txt","r")
output = open("hmmoutput.txt","w")

transition_prob = {}
emission_prob = {}

pointer = model_file.readline().strip("\n")
while len(pointer.strip()) != 0:
    previous,current,prob = pointer.split("\t")
    if previous not in transition_prob:
        transition_prob[previous] = dict()
    if current not in transition_prob[previous]:
        transition_prob[previous][current] = prob

    pointer = model_file.readline().strip("\n")


pointer = model_file.readline().strip("\n")

while len(pointer.strip()) != 0:
    word,tag ,probs = pointer.split("\t")
    if word not in emission_prob:
        emission_prob[word] = dict()
    if tag not in emission_prob[word]:
        emission_prob[word][tag] = probs
    pointer = model_file.readline().strip("\n")

for line in input:
    arr = line.split()
    start_word = arr[0]
    start_prob = {}
    if start_word in emission_prob:
        for state in emission_prob[start_word]:
            proxy = float(transition_prob["START"][state]) * float(emission_prob[start_word][state])
            start_prob[state] = proxy
        prev_tag = max(start_prob, key = lambda x: start_prob.get(x))
        prev_prob = start_prob[prev_tag]
    else:
        words = start_word.split("_")
        total_split = len(words)
        for state in transition_prob["START"]:
            proxy = float(transition_prob["START"][state])
            start_prob[state] = proxy
        prev_tag = max(start_prob, key = lambda x: start_prob.get(x))
        prev_prob = start_prob[prev_tag]
        if total_split > 1:
            prev_tag = "NP"

    output.write(start_word+"/"+prev_tag)

    for i in range(1,len(arr)):
        cont_prob = {}
        word = arr[i]
        if word in emission_prob:
            for state in emission_prob[word]:
                proxy = float(prev_prob) * float(transition_prob[prev_tag][state]) * float(emission_prob[word][state])
                cont_prob[state] = proxy
            prev_tag = max(cont_prob, key = lambda x: cont_prob.get(x))
            prev_prob = cont_prob[prev_tag]
        else:
            for state in transition_prob[prev_tag]:
                proxy = prev_prob * float(transition_prob[prev_tag][state])
                cont_prob[state] = proxy
            prev_tag = max(cont_prob, key = lambda x: cont_prob.get(x))
            prev_prob = cont_prob[prev_tag]
            if word[0].isupper():
                prev_tag = "NP"

        output.write(" "+word+"/"+prev_tag)
    output.write("\n")

