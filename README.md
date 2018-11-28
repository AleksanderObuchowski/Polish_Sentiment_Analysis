# Polish_Sentiment_Analysis
## Descripton on hackmd:
https://hackmd.io/Nz9iiJDVRCujYjQJ3HG7OA
## Files and what do they do?

**data.csv** contains reviews and their score downloaded from mediakrytyk.pl

**preprocesing.py** creates **dictionary.json** file containing information how often were the words used in positive or negative context. It uses **data.csv** file to get the data
 
**learning.py** uses data from **dictionary.json** to create sentiment lexicon storred in **sentiment.json**

**classifier.py** uses data form **sentiment.json** to classify new new sentences

**accuracy.py** uses **classifier.py** to perform sentiment analisys on data from **data.csv**

**pan_tadeusz.py** uses **classifier.py** to perform sentiment analisys on **pan_tadeusz.txt**
