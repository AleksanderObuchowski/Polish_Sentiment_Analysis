import json
import io
import csv
from tqdm import tqdm
filename= "dictionary.json"
sentimentfile = "sentiment.json"

def updateFile(filename,dictionary):
    file = io.open(filename, 'w', encoding='utf8')
    json.dump(dictionary, file, ensure_ascii=False)
    file.close()



# LOADING DICTIONARY

file =io.open(filename, 'r', encoding='utf8')
dict = json.load(file)
file.close()

sentdict = {'Words': {}}


print(len(dict["Words"].keys()))
print(dict.keys())

size = 0
for word in dict["Words"]:
    size += dict["Words"][word]['Positive']+ dict["Words"][word]['Negative']

size-=2
print(size)
i =0

print("Looping through words")

for word in tqdm(dict["Words"]):
    i+=1
    #print("-------Word :" + word)
   


    P_positive_word = (dict["Words"][word]["Positive"]+1)/(dict["Positive_words"]+len(dict["Words"]))
    #print("P_positive_word: "+ str(P_positive_word))

    

    P_negative_word = (dict["Words"][word]["Negative"]+1)/(dict["Negative_words"]+len(dict["Words"]))

    sentdict["Words"][word] = {"Positive":0}

    sentdict["Words"][word]["Positive"] = P_positive_word
    sentdict["Words"][word]["Negative"] = P_negative_word
sentdict["Negative"] = dict["Negative_sentences"]/(dict["Negative_sentences"] + dict["Positive_sentences"])

updateFile(sentimentfile,sentdict)
sentdict["Positive"] = dict["Positive_sentences"]/(dict["Negative_sentences"] + dict["Positive_sentences"])
updateFile(sentimentfile,sentdict)
print(sentdict["Positive"])
print(sentdict["Negative"])
print("Finished succesfully")