__author__ = 'Preethi'
import sys
file_name = sys.argv[1]
input = open(file_name,"r")
output = open("hmmmodel.txt","w")
total_tags = {}
trans_num = {}
trans_deno = {}
emission_num = {}


total_tags["START"] = 0


for line in input:
    total_tags["START"] += 1
    previous_tag = "START"
    arr = line.split()

    for word in arr:
        words = []
        concat_word = ""
        current_tag = ""
        words = word.split("/")
        total_split = len(words)

        if (total_split > 2):

            current_tag = words[total_split-1]
            words.remove(current_tag)
            concat_word = "/".join(words)
        else:
            concat_word = words[0]
            current_tag = words[1]
        #output.write(concat_word+"-"+current_tag+" ")

        #All unique tags and their count
        if current_tag in total_tags:
            total_tags[current_tag] += 1
        else:
            total_tags[current_tag] = 1

        # Emission numerator
        if concat_word not in emission_num:
            emission_num[concat_word] = dict()
        if current_tag not in emission_num[concat_word]:
            emission_num[concat_word][current_tag] = 0
        emission_num[concat_word][current_tag] += 1


        # Transition numerator
        if previous_tag not in trans_num:
            trans_num[previous_tag] = dict()
        if current_tag not in trans_num[previous_tag]:
            trans_num[previous_tag][current_tag] = 0
        trans_num[previous_tag][current_tag] += 1

        # Transition denominator
        if previous_tag not in trans_deno:
            trans_deno[previous_tag] = 0
        trans_deno[previous_tag] += 1

        previous_tag = current_tag


for x in total_tags:
    if x not in trans_num:
            trans_num[x] = dict()
    for y in total_tags:
        if y not in trans_num[x] and y != "START":
            trans_num[x][y] = 0


for x in trans_num:
    if 0 in trans_num[x].values():
        for y in trans_num[x]:
            trans_num[x][y] += 1
        trans_deno[x] += len(total_tags)-1
    for y in trans_num[x]:
        trans_prob = float(trans_num[x][y])/float(trans_deno[x])
        output.write(x+"\t")
        output.write(y+"\t")
        output.write(str(trans_prob)+"\n")

output.write("\n")

for x in emission_num:
    for y in emission_num[x]:
        emission_prob = float(emission_num[x][y])/float(total_tags[y])
        output.write(x+"\t")
        output.write(y+"\t")
        output.write(str(emission_prob)+"\n")






