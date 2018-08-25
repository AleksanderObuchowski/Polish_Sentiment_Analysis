# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 22:11:21 2018

@author: obuch
"""

import classifier

import io

c = classifier.Classifier("sentiment.json",False)


file =io.open("pan_tadeusz.txt", "r",encoding='utf8'
              ) 
sentences = file.read().strip("\n").split(".")

positive = 0
negative = 0
for s in sentences:
    if c.evaluate(s) == "Positive":
        positive+=1
    else:
        negative +=1
        
print(positive/(positive+negative))