# -*- coding: utf-8 -*-

import csv
import json
import os
import io
from tqdm import tqdm


dictionaryFile = "dictionary.json"
treshold =5
dict = {}
dict["Words"] = {}
def loadDictionary(filename):

    file = io.open(filename, 'w', encoding='utf8')
    json.dump(dict,file)
    file.close()
    file =io.open(filename, 'r', encoding='utf8')
    dictionary = json.load(file)
    file.close()
    return dictionary
def updateFile(filename,dictionary):
    file = io.open(filename, 'w', encoding='utf8')
    json.dump(dictionary, file, ensure_ascii=False)
    file.close





dict = {'Words':{}}

file =io.open("stopwords-pl.json", 'r', encoding='utf8')
stopwords = json.load(file)
file.close()


f =open("data.csv",'r')
reader = csv.reader(f)
i=0
num_negative = 0
num_positive = 0
words = []

positive_sentences = []
negative_sentences = []

num_words=0
for row in tqdm(reader):
    #print("reading row " + str(i))
    #print(row)
   
    if (row!=[]):
        if row[0]=="Wymaga uzupełnienia.":
            continue
        
        i+=1
        if (i >15000):
            break
        if float(row[1]) > treshold:
            positive_sentences.append(row[0])
        elif float(row[1]) <= treshold:
            negative_sentences.append(row[0])
            
i=0           


for i in tqdm(range(len(positive_sentences))):
    
    #print(i)
    #print(positive_sentences[i].strip(",").strip(".").split(" "))
    words = positive_sentences[i].strip(",").strip(".").split(" ")
    new_words= []
    for word in words:
        if word not in new_words:
            new_words.append(word)
    for word in new_words:
        if word in stopwords:
            #print("Stopword")
            continue
        num_words+=1
        
        num_positive +=1
        

        if word not in dict["Words"]:
            
            dict["Words"][word]={'Positive':1}
            dict["Words"][word]["Negative"]=0
            
        else:
           
            dict["Words"][word]["Positive"]+=1

            
                
for i in tqdm(range(len(negative_sentences))):               
    words = negative_sentences[i].strip(",").strip(".").split(" ")

    new_words= []
    for word in words:
        if word not in new_words:
            new_words.append(word)
    for word in new_words:
        if word in stopwords:
            #print("Stopword")
            continue
        
        
        num_negative +=1

        if word not in dict["Words"]:
           
            dict["Words"][word]={'Positive':0}
            dict["Words"][word]["Negative"]=1
            
        

        else:
            dict["Words"][word]["Negative"]+=1


updateFile(dictionaryFile,dict)
    
print("Negative sentences :" + str(len(positive_sentences)))
print("Positive sentences :" + str(len(negative_sentences)))

dict["Positive_words"] = num_positive
dict["Negative_words"] = num_negative

dict["Negative_sentences"] = len(positive_sentences)
dict["Positive_sentences"] = len(negative_sentences)

dict["Words_count"] = num_words
print("Word count: " + str(num_words))
print("Positive words: " + str(num_positive))
print("Negativee words: " + str(num_negative))
print(str(len(dict["Words"])))

updateFile(dictionaryFile,dict)

