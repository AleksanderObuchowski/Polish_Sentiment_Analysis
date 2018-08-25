import io
import json


filename= "sentiment.json"
sentence ="no nie wiem w sumie"


file =io.open(filename, 'r', encoding='utf8')
dict = json.load(file)
file.close()
while (1):
    sentence = input()
    words = sentence.split(" ")
    score= 0
    for word in words:
        if word in dict:
            score+= dict[word]
            print("Word: "+ word +" Score: " + str(dict[word]))

    print("Total score:" + str(score))
    if score<0:
        print("The sentence is negative")
    else:
        print("The sentence is positve")
