import pickle

with open ('positive_comments.txt', 'rb') as fp:
    itemlist = pickle.load(fp)
print(itemlist)