"""
    File use to train the bot.Show you a list of french 
    sentences that you can call as positive (pos) or negative (neg).
"""
import os
from textblob.classifiers import NaiveBayesClassifier


def add(args):
    """
        Add a new input into the data file read by the bot.
    """
    with open('data.csv', 'a', encoding='utf-8') as outfile:
        outfile.write(args['text']+","+args['label']+"\n")


def readwords():
    """
        Show a list of sentences and ask the user to specify pos/neg/
    """
    stop = False
    with open('sentences2.csv', 'r', encoding='utf-8') as fin, open('sentences2_1.csv', 'w', encoding='utf-8') as fou:
        for line in fin:
            if not stop:
                entry = {'text': line[:-1]}
                label = input(line[:-1])
                if label != "pos" and label != "neg" and label != "":
                    fou.write(line)
                    stop = True
                elif label == "":  # if the user just send a empty value the programm ignore the sentence
                    pass
                else:
                    entry['label'] = label
                    add(entry)
            else:  # save remaining sentences to the file
                fou.write(line)
    os.remove('sentences2.csv')
    os.rename('sentences2_1.csv', 'sentences2.csv')

readwords()

with open('data.csv', 'r') as f:
    cl = NaiveBayesClassifier(f, format="csv")

print("finish")




