from sklearn import svm
import csv
import json
import os
import io
from tqdm import tqdm
import codecs
import time
import matplotlib.pyplot as plt
import math
try:
    with codecs.open("sentiment.json", 'r', "windows-1250",errors="ignore") as file:
        dict = json.load(file)

except:
    pass



class Classifier:


   def __init__(self,filename, info = True):
        self.info = info
        file = io.open(filename, 'r', encoding='utf8')
        self.dict = json.load(file)
        file.close()


   @staticmethod
   def evaluate(sentence ,use_class_probabilites = True, logaritmic = True, info = True, curve =True):
        
        
        words = sentence.replace(",", "").lower().replace(".","").replace("/","").split(" ")
        
        
        if(use_class_probabilites):
            if(logaritmic):
                positive = math.log10(dict["Positive"])
                negative = math.log10(dict["Negative"])
            else:
                positive = dict["Positive"]
                negative = dict["Negative"]

        
        else:
            positive = 1
            negative = 1

        for word in words:
            if word in dict["Words"]:
                if info:
                    print(word + " : Word in dictionary")
            

                if logaritmic:
                    positive += math.log10(dict["Words"][word]["Positive"]/len(dict["Words"]))
                    negative += math.log10(dict["Words"][word]["Negative"]/len(dict["Words"]))
                else:

                    positive *= dict["Words"][word]["Positive"]/len(dict["Words"])
                    negative *= dict["Words"][word]["Negative"]/len(dict["Words"])

            
        if info:
            print("Sentence score:")
            print("Positive: " +str(positive))
            print("Negative: " + str(negative))
            
        if positive> negative:
            if(curve):
                return ("Positive",positive,negative)
            else:    
                return "Positive"
        elif negative>positive:
            if(curve):
                return ("Negative",positive,negative)
            else:
                return "Negative"
        else:
            return "Undefined"

    



   @staticmethod
   def loadDictionary(mode = "append",filename= 'dictionary.json'):
        print(mode)
        try:
            if mode =="append":
                with codecs.open(filename, 'r', encoding='utf8',errors="ignore") as file:
                    print("Dictionary file detected, loading dictionary")
                    dictionary =json.load(file)
            else:
                 print("Creating new dictionary")
                 dictionary = {'Words':{}}

        
        except:
            print("No dictinary file detected, creating a new dictionary")
            dictionary = {'Words':{}}

        
        return dictionary
   @staticmethod
   def updateFile(filename,dictionary):
        file = codecs.open(filename, 'w', encoding='utf8')
        json.dump(dictionary, file, ensure_ascii=False)
        file.close()

   @staticmethod
   def preprocess_comments(mode ="apppend",positive_file='positive_comments_form_score.txt',negative_file = 'negative_comments_form_score.txt' ,stopwords_file = "stopwords-pl.json", dictionaryFile = "dictionary.json",split = 1.0):
        
        dict = Classifier.loadDictionary(mode = mode,filename = dictionaryFile)
      
        
        with codecs.open(stopwords_file, 'r', "windows-1250",errors='ignore') as file:
            stopwords = json.load(file)
        


        print("Loading positive comments")
        with open(positive_file) as f:
            lines_p = f.readlines()
        print("Positive comments loaded succesfully")
        print("Prasing positive comments")
        num_words = 0
        num_positive= 0

        for i in tqdm(range(int(len(lines_p)* split))):
            words = lines_p[i].replace(",", "").replace(".","").lower().replace("/","").split(" ")
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
        
        print("Finished prasing positive comments")
        print("Loading negative comments")
        with open(negative_file) as f:
            lines_n = f.readlines()
        print("Positive comments loaded succesfully")
        print("Prasing negative comments")
        num_negative = 0

        for i in tqdm(range(int(len(lines_n)* split))):
            words = lines_n[i].replace(",", "").replace(".","").lower().replace("/","").split(" ")
            new_words= []
            for word in words:
                if word not in new_words:
                    new_words.append(word)
            for word in new_words:
                if word in stopwords:
                    #print("Stopword")
                    continue
                num_words+=1
                
                num_negative +=1
                

                if word not in dict["Words"]:
                    
                    dict["Words"][word]={'Negative':1}
                    dict["Words"][word]["Positive"]=0
                    
                else:
                
                    dict["Words"][word]["Negative"]+=1

        print("Negative comments prased succesfully")

        
        dict["Negative_sentences"] = len(lines_n)
        dict["Positive_sentences"] = len(lines_p)
        


        dict["Positive_words"] = num_positive
        dict["Negative_words"] = num_negative

        dict["Words_count"] = num_words
        print("Word count: " + str(num_words))
        print("Positive words: " + str(num_positive))
        print("Negativee words: " + str(num_negative))
        


        Classifier.updateFile(dictionaryFile,dict)

   @staticmethod
   def preprocess_reviews(stopwords_file = "stopwords-pl.json",data = "data.csv",dictionaryFile = "dictionary.json",treshold = 5,normalize= False):
        print("START PREPROCESS REVIEWS")
        dict = {'Words':{}}

        file =codecs.open(stopwords_file, 'r', "windows-1250",errors='ignore')
        stopwords = json.load(file)
        file.close()


        f =codecs.open(data,'r',"windows-1250",errors='ignore')
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
                if (i >105000):
                    break
                if float(row[1]) > treshold+2:
                    positive_sentences.append(row[0])
                elif float(row[1]) <= treshold-2:
                    negative_sentences.append(row[0])
                    
        i=0           

        num_positive_sentences = len(positive_sentences)
        num_negative_sentences = len(negative_sentences)



        lower_number = min(num_negative_sentences,num_positive_sentences)



        if(normalize):
            
            num_positive_sentences = lower_number
            num_negative_sentences = lower_number


        for i in tqdm(range(num_positive_sentences)):
            
            #print(i)
            #print(positive_sentences[i].strip(",").strip(".").split(" "))
            words = positive_sentences[i].replace(",", "").replace(".","").lower().replace("/","").split(" ")
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




        for i in tqdm(range(num_negative_sentences)):               
            words = negative_sentences[i].replace(",", "").lower().replace(".","").replace("/","").split(" ")
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


        Classifier.updateFile(dictionaryFile,dict)
        if not normalize:

            print("Negative sentences :" + str(len(positive_sentences)))
            print("Positive sentences :" + str(len(negative_sentences)))

        

            dict["Negative_sentences"] = len(positive_sentences)
            dict["Positive_sentences"] = len(negative_sentences)

        else:
            dict["Negative_sentences"] = lower_number
            dict["Positive_sentences"] = lower_number 
        


        dict["Positive_words"] = num_positive
        dict["Negative_words"] = num_negative

        dict["Words_count"] = num_words
        print("Word count: " + str(num_words))
        print("Positive words: " + str(num_positive))
        print("Negativee words: " + str(num_negative))
        print(str(len(dict["Words"])))

        Classifier.updateFile(dictionaryFile,dict)
   @staticmethod
   def learn(mode = "append",filename= "dictionary.json",sentimentfile = "sentiment.json"):
        print("START LEARNING")
        dict = Classifier.loadDictionary(filename = filename)
    
        sentdict = Classifier.loadDictionary(mode = mode,filename= sentimentfile)
        

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
        


            P_word_positive= (dict["Words"][word]["Positive"]+1)/(dict["Positive_words"]+len(dict["Words"]))
            
            #print("P_positive_word: "+ str(P_positive_word))

            

            P_word_negative = (dict["Words"][word]["Negative"]+1)/(dict["Negative_words"]+len(dict["Words"]))

            

            sentdict["Words"][word] = {"Positive":0}

            sentdict["Words"][word]["Positive"] = P_word_positive
            sentdict["Words"][word]["Negative"] = P_word_negative
        
        
        sentdict["Negative"] = dict["Negative_sentences"]/(dict["Negative_sentences"] + dict["Positive_sentences"])
        sentdict["Positive"] = dict["Positive_sentences"]/(dict["Negative_sentences"] + dict["Positive_sentences"])
        Classifier.updateFile(sentimentfile,sentdict)
        print(sentdict["Positive"])
        print(sentdict["Negative"])
        print("Finished succesfully")
   @staticmethod
   def accuracy_check(info = True,positive_file="positive_comments.txt", negative_file = "negative_comments.txt",curve = True, log = "",split = 1.0):
        P_positiveP = []
        P_negativeP = []
        P_positiveN = []
        P_negativeN = []

        print("START ACCURACY CHECK")
        m = confusion_matrix(log)
        with codecs.open(positive_file, 'r', "windows-1250",errors="ignore") as file:
            lines_p =  file.readlines()

        print("loaded positive comments")
        with codecs.open(negative_file, 'r', "windows-1250",errors="ignore") as file:
            lines_n =  file.readlines()
        print("loaded negaative comments")

        for i in tqdm(range(len(lines_p)-1,int(len(lines_p)-(len(lines_p)*split)),-1)):
            score = Classifier.evaluate(lines_p[i],info=False,curve = True)
            P_positiveP.append(score[1])
            P_negativeP.append(score[2])
            if score[0] == "Positive":
                        m.TP+=1
            if score[0] == "Negative":
                        m.FN+=1


        for i in tqdm(range(len(lines_n)-1,int(len(lines_n)-(len(lines_n)*split)),-1)):
            score = Classifier.evaluate(lines_n[i],info=False,curve = True)
            P_positiveN.append(score[1])
            P_negativeN.append(score[2])
            if score[0] == "Negative":
                        m.TN+=1
            if score[0] == "Positive":
                        m.FP+=1

        print("Finished analyzing " + str(i) + "sentences")
        
        m.print_results()
        m.save_results()
        
        '''
        X = []
        Y = []
        for i in range(len(P_positiveP)):
            X.append([P_positiveP[i],P_negativeP[i]])
            Y.append(0)
        for i in range(len(P_positiveP)):
            X.append([P_positiveN[i],P_negativeN[i]])
            Y.append(1)

        clf = svm.SVC(kernel ='linear')
        #print(X[0:5])
        clf.fit(X,Y)
        clf.score(X,Y)

        print(clf.decision_function([[10,10]]))
        plt.plot(P_positiveP,P_negativeP,'bo')
        plt.plot(P_positiveN,P_negativeN,'ro')
        plt.plot(range(-400,0),range(-400,0))
       
        plt.show()
        '''


   @staticmethod
   def test_on_play(data,log="test"):
       P_positiveP = []
       P_negativeP = []
       P_positiveN = []
       P_negativeN = []

       print("START ACCURACY CHECK")
       m = confusion_matrix(log)

       f =codecs.open(data,'r',"windows-1250",errors='ignore')
       reader = csv.reader(f)
       for row in tqdm(reader):
       
           score = Classifier.evaluate(row[0],info=False,curve = True)
           if (row[1]=="1" and score[0] == "Positive"):
               m.TP+=1
           if (row[1]=="1" and score[0] == "Negative"):
               m.FN+=1
           if (row[1]=="3" and score[0] == "Negative"):
               m.TN+=1
           if (row[1]=="3" and score[0] == "Positive"):
               m.FP+=1

       m.print_results()
       m.save_results()
           
        


        

   @staticmethod
   def convert_score(data = 'Data/data.csv',lower = 2, upper = 8,positive_file = "Data/positive_comments_from_score.txt",negative_file = "Data/negative_comments_from_score.txt"):
        f =codecs.open(data,'r',"windows-1250",errors='ignore')
        reader = csv.reader(f)
        
        positive_sentences = []
        negative_sentences = []


     
        for row in tqdm(reader):
            
        
            if (row!=[]):
                if row[0]=="Wymaga uzupełnienia.":
                    continue
                
                
             
                if float(row[1]) > upper:
                    positive_sentences.append(row[0])
                elif float(row[1]) <= lower:
                    negative_sentences.append(row[0])
        
        
        with open(positive_file,"a") as text_file:
            text_file.write("\n".join(positive_sentences))


        with open(negative_file,"a") as text_file:
            text_file.write("\n".join(negative_sentences))


        















class confusion_matrix(object):
    TP=0
    TN=0
    FP=0
    FN=0
    def __init__(self,log):
        self.log = log
        self.TP=0
        self.TN=0
        self.FP=0
        self.FN=0



    def print_results(self):
        print("\n\n\n"+" C O N F U S I O N      M A T R I X" + "\n")
        print("True Positives: " + str(self.TP))
        print("True Negatives: " + str(self.TN))
        print("False Positives: " + str(self.FP))
        print("False Negatives: " + str(self.FN))
        print("\n")
        print("sensitivity: " + str(self.TP/(self.TP + self.FN)))
        print("specitivity: " + str(self.TN / (self.TN + self.FP)))
        print("precison: " + str(self.TP / (self.TP + self.FP)))
        print("accuracy: " + str((self.TP + self.TN) / (self.TP + self.TN + self.FP + self.FN)))


    def save_results(self):
        file = open('matrix_log.txt','a') 
        file.write("/n")
        file.write(time.strftime('%d/%m/%Y'))
        
        
        file.write("\n\n\n"+" C O N F U S I O N      M A T R I X  " +time.strftime('%d/%m/%Y ')+time.strftime("%H:%M:%S")+ "\n")
        file.write(self.log)
        file.write("\nTrue Positives: " + str(self.TP))
        file.write("\nTrue Negatives: " + str(self.TN))
        file.write("\nFalse Positives: " + str(self.FP))
        file.write("\nFalse Negatives: " + str(self.FN))
        file.write("\n")
        file.write("\nsensitivity: " + str(self.TP/(self.TP + self.FN)))
        file.write("\nspecitivity: " + str(self.TN / (self.TN + self.FP)))
        file.write("\nprecison: " + str(self.TP / (self.TP + self.FP)))
        file.write("\naccuracy: " + str((self.TP + self.TN) / (self.TP + self.TN + self.FP + self.FN)))
        file.write("\nROC: " + str((self.TP/(self.TP + self.FN))/ (1- (self.TN / (self.TN + self.FP)))))

       
         
        file.close() 

