import io
import json
import codecs
import Polish_sentiment
filename= "sentiment.json"
sentence ="nie podoba mi się ten test"


file =codecs.open(filename, 'r', 'windows-1250',errors='ignore')
dict = json.load(file)
file.close()

c = Polish_sentiment.Classifier("sentiment.json",False)


sentence = input()
print(c.evaluate(sentence))
