import csv
import io
import json
import classifier
import time
filename= "sentiment.json"
treshold = 5


class confusion_matrix(object):
    TP=0
    TN=0
    FP=0
    FN=0
    def __init__(self):
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
        file.write("\nTrue Positives: " + str(self.TP))
        file.write("\nTrue Negatives: " + str(self.TN))
        file.write("\nFalse Positives: " + str(self.FP))
        file.write("\nFalse Negatives: " + str(self.FN))
        file.write("\n")
        file.write("\nsensitivity: " + str(self.TP/(self.TP + self.FN)))
        file.write("\nspecitivity: " + str(self.TN / (self.TN + self.FP)))
        file.write("\nprecison: " + str(self.TP / (self.TP + self.FP)))
        file.write("\naccuracy: " + str((self.TP + self.TN) / (self.TP + self.TN + self.FP + self.FN)))
       
         
        file.close() 

m = confusion_matrix()
c = classifier.Classifier("sentiment.json",False)




f =open("data.csv",'r')
reader = csv.reader(f)

i=0

for row in reader:

    if (row!=[]):


        if row[0]=="Wymaga uzupełnienia.":
            continue
        i+=1
        row[0].strip(",").strip(".")
        words = row[0].split(" ")
        score = c.evaluate(row[0])
        if i>15000:
            if score == "Positive" and float(row[1])>treshold:
                m.TP+=1
            elif score == "Positive" and float(row[1])<treshold:
                m.FP+=1
            elif score == "Negative" and float(row[1])<treshold:
                m.TN+=1
            elif score == "Negative" and float(row[1])>treshold:
                m.FN+=1

    if(i>20000):
        break
print("Finished analyzing " + str(i) + "sentences")
m.print_results()
m.save_results()