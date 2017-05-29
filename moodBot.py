import csv

import discord
import math
from textblob.classifiers import NaiveBayesClassifier

client = discord.Client()
cl = None

usersMood = {}

emoijs_value ={}

smiley_faces = [':rage',':angry',':worried:',':disappointed:',':neutral_face:',':neutral_face:',':slight_smile:',':grin:',':grinning:',':smiley:']

def add(args):
    data_update = [(args['text'], args['label'])]
    cl.update(data_update)
    with open('data_small.csv', 'a', newline='\n', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow((args['text'],args['label']))

def analyseSentence(cl, sentence):
    prob_dist = cl.prob_classify(sentence)
    out = ""
    out += "max " + prob_dist.max() + "\n"
    out += "pos " + str(round(prob_dist.prob("pos"), 2)) + "\n"
    out += "neg " + str(round(prob_dist.prob("neg"), 2)) + "\n"
    return out


def printEmoticon(value):
    # :smiley: :grinning: :grin: :slight_smile: :neutral_face: :disappointed: :worried: :angry: :rage:
    return smiley_faces[math.floor(value*10)]

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
        if message.content.startswith("!show"):
            output = ""
            for key, value in usersMood.items():
                a = avg(value)
                print(key, usersMood[key], a)
                output += key + " " + printEmoticon(avg(value)) + "\n"
            if output != "":
                await client.send_message(message.channel, output)
        elif message.content.startswith("!reset"):
            usersMood.pop(message.author.name, None)
        else :
            prob_dist = cl.prob_classify(message.content[6:])
            if message.author.name not in usersMood:
                usersMood[message.author.name] = []
            usersMood[message.author.name].append(round(prob_dist.prob("pos"), 2))
            if round(prob_dist.prob("pos"),2)<0.4 :
                await client.send_message(message.channel,chr(0x1F921))
            await client.send_message(message.channel,analyseSentence(cl,message.content[6:]))


@client.event
async def on_reaction_add(reaction, user):
    if reaction.emoji in emoijs_value.keys() :
        for part in reaction.message.content.split(","):
            entry ={}
            entry['text'] = part
            entry['label'] = emoijs_value[reaction.emoji]
            add(entry)

with open('emoticonsData.csv','r') as f:
    for line in f:
        emoijs_value[chr(int(line.split(",")[0],0))]=line.split(",")[1][:-1]

with open('data_small.csv', 'r') as f:
    cl = NaiveBayesClassifier(f, format="csv")

with open('tokenfile.txt', 'r') as f:
    for line in f:
        client.run(line)
