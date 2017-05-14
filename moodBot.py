import discord
import asyncio
import os
from textblob.classifiers import NaiveBayesClassifier

client = discord.Client()
cl = None

usersMood = {}

def add(args):
    with open('data.csv', 'a',encoding='utf-8') as outfile:
        outfile.write(args['text']+","+args['label']+"\n")

def restart(cl):
    pass

def anaylseSentence(cl,sentence):
    #print(sentence)
    prob_dist = cl.prob_classify(sentence)
    out = ""
    out += "max "+prob_dist.max()+"\n"
    out += "pos "+str(round(prob_dist.prob("pos"), 2))+"\n"
    out += "neg "+str(round(prob_dist.prob("neg"), 2))+"\n"
    return out


def printEmoticon(value):
    # :smiley: :grinning: :grin: :slight_smile: :neutral_face: :disappointed: :worried: :angry: :rage:
    if(value <0.1):
        return ":rage:"
    elif(value <0.2):
        return ":angry:"
    elif(value <0.3):
        return ":worried:"
    elif(value <0.4):
        return ":disappointed:"
    elif(value < 0.6):
        return ":neutral_face:"
    elif(value <0.7):
        return ":slight_smile:"
    elif(value<0.8):
        return ":grin:"
    elif(value<0.9):
        return ":grinning:"
    else:
        return ":smiley:"

def avg(l):
    return sum(l, 0.0) / len(l)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author != client.user:
        if message.content.startswith("!teach "):
            entry = {}
            str = message.content[7:].split(",")
            entry['text'] = str[0]
            entry['label'] = str[1]
            add(entry)
            await client.send_message(message.channel, "success")
        elif message.content.startswith("!show"):
            output = ""
            for key, value in usersMood.items():
                a = avg(value)
                print(key,usersMood[key],a)
                output += key+" "+printEmoticon(avg(value))+"\n"
            if output != "":
                await client.send_message(message.channel,output)
        else:
            prob_dist = cl.prob_classify(message.content[6:])
            if message.author.name not in usersMood:
                usersMood[message.author.name] = []
            usersMood[message.author.name].append(round(prob_dist.prob("pos"), 2))
            #await client.send_message(message.channel,anaylseSentence(cl,message.content[6:]))

with open('data.csv', 'r') as f:
    cl = NaiveBayesClassifier(f, format="csv")

with open('tokenfile.txt','r') as f:
    for line in f:
        client.run(line)
