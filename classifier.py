import io
import json

class Classifier:


   def __init__(self,filename, info = True):
        self.info = info
        file = io.open(filename, 'r', encoding='utf8')
        self.dict = json.load(file)
        file.close()

   def evaluate(self,sentence):
        words = sentence.split(" ")

        positive = self.dict["Positive"]
        
        negative = self.dict["Negative"]
        for word in words:
            if word in self.dict["Words"]:
                if self.info:
                    print("Word in dictionary")
                positive *= self.dict["Words"][word]["Positive"]
                negative *= self.dict["Words"][word]["Negative"]
        if self.info:
            print("Positive: " +str(positive))
            print("Negative: " + str(negative))
            if negative<positive:
                print("The sentence is positve")
        if positive> negative:
            return "Positive"
        else:
            return "Negative"





