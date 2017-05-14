import os
from textblob.classifiers import NaiveBayesClassifier

def add(args):
    with open('data.csv', 'a',encoding='utf-8') as outfile:
        outfile.write(args['text']+","+args['label']+"\n")


def readWords():
    stop = False
    with open('sentences2.csv','r',encoding='utf-8') as fin,open('sentences2_1.csv','w',encoding='utf-8') as fou:
        for line in fin:
            if not stop:
                entry = {};
                entry['text'] = line[:-1]
                label = input(line[:-1])
                if label != "pos" and label != "neg" and label!="":
                    fou.write(line)
                    stop = True;
                elif label == "":
                    pass
                else:
                    entry['label'] = label
                    add(entry)
            else:
                fou.write(line)
    os.remove('sentences2.csv')
    os.rename('sentences2_1.csv','sentences2.csv')

readWords()

with open('data.csv','r') as f:
    cl = NaiveBayesClassifier(f,format="csv")

print("finish")




