import codecs
n_folds = 5

results = 0

with codecs.open("positive_comments.txt",'r',"windows-1250",errors='ignore')as file:
    lines_p = file.readlines()

with codecs.open("negative_comments.txt",'r',"windows-1250",errors='ignore')as file:
    lines_n = file.readlines()


for i in range(n_folds):
    with open('p_comments'+str(i)+'.txt', 'w') as f:
        for j in range(i*int((len(lines_p))/n_folds),(i+1)*int((len(lines_p))/n_folds)):
            f.write("%s" % lines_p[j])


for i in range(n_folds):
    with open('n_comments'+str(i)+'.txt', 'w') as f:
        for j in range(i*int((len(lines_n))/n_folds),(i+1)*int((len(lines_n))/n_folds)):
            f.write("%s" % lines_n[j])











for i in range(n_folds):
    Classifier.preprocess_comments(mode = 'a',positive_file='p_comments'+str(i)+'.txt', negative_file= 'n_comments'+str(i)+'.txt',split=1.0)
    n =1
    while n<n_folds-1:
        Classifier.preprocess_comments(mode = 'a',positive_file='p_comments'+str((i+n)%n_folds)+'.txt', negative_file= 'n_comments'+str((i+n)%n_folds)+'.txt',split=1.0)
        n+=1

    Classifier.learn(mode ='a')
    results += Classifier.accuracy_check(info = False,split=0.2)
