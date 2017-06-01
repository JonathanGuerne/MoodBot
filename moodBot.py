"""
Moodbot is a bot that analyze the message from a discord server for guessing the mood of the people.

When people become angry, Moodbot tries to clam down the situation by sending a clown.
"""

import csv
import discord
from textblob.classifiers import NaiveBayesClassifier
from statistics import mean

client = discord.Client()
cl = None

usersMood = {}

emoijs_value = {}

prev_analys_value = []


smiley_faces = [':rage',':angry',':worried:',':disappointed:',':neutral_face:',':neutral_face:',':slight_smile:',':grin:',':grinning:',':smiley:',':smiley:']

def add(args):
    """Add the word in the classifier and in the memory."""
    data_update = [(args['text'], args['label'])]
    cl.update(data_update)
    with open('data_small.csv', 'a', newline='\n', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow((args['text'], args['label']))


def analyseSentence(cl, sentence):
    """Return the data from the analyse."""
    prob_dist = cl.prob_classify(sentence)
    out = ""
    out += "max " + prob_dist.max() + "\n"
    out += "pos " + str(round(prob_dist.prob("pos"), 2)) + "\n"
    out += "neg " + str(round(prob_dist.prob("neg"), 2)) + "\n"
    return out


def printEmoticon(value):
    """Return the emotion as an emoticon."""
    # :smiley: :grinning: :grin: :slight_smile: :neutral_face: :disappointed: :worried: :angry: :rage:
    return smiley_faces[int(value*10)]


@client.event
async def on_ready():
    """Executed when the bot is ready."""
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    """Executed when a new message arrive in a channel (private/public)."""
    if message.author != client.user:
        if message.content.startswith("!show"):
            output = ""
            for key, value in usersMood.items():
                a = mean(value)
                print(key, usersMood[key], a)
                output += key + " " + printEmoticon(mean(value)) + "\n"
            if output != "":
                await client.send_message(message.channel, output)
        elif message.content.startswith("!reset"):
            usersMood.pop(message.author.name, None)
        else:
            prob_dist = cl.prob_classify(message.content[6:])
            if message.author.name not in usersMood:
                usersMood[message.author.name] = []
            usersMood[message.author.name].append(round(prob_dist.prob("pos"), 2))
            prev_analys_value.append(round(prob_dist.prob("pos"),2))
            if len(prev_analys_value)>10:
                temp_list = prev_analys_value[-10:]
                prev_analys_value[:] = temp_list
            if len(prev_analys_value) == 10 and mean(prev_analys_value)<0.4 :
                await client.send_message(message.channel,("Voici un clown pour détendre l'atmosphère : \N{CLOWN FACE}"))
                prev_analys_value.clear()
            print(analyseSentence(cl,message.content[6:]))



@client.event
async def on_reaction_add(reaction, user):
    """Executed when a new reaction is added to a message."""
    if reaction.message.author != client.user and reaction.emoji in emoijs_value.keys() :
        for part in reaction.message.content.split(","):
            entry ={}
            part = part.strip()
            entry['text'] = part
            entry['label'] = emoijs_value[reaction.emoji]
            add(entry)

with open('emoticonsData.csv', 'r') as f:
    for line in f:
        emoijs_value[chr(int(line.split(",")[0],0))]=line.split(",")[1][:-1]

with open('data_small.csv', 'r') as f:
    cl = NaiveBayesClassifier(f, format="csv")

with open('tokenfile.txt', 'r') as f:
    for line in f:
        client.run(line)
