"""
Moodbot is a bot that analyze the message from a discord server for guessing the mood of the people.

When people become angry, Moodbot tries to clam down the situation by sending a clown.
"""

import csv
import discord
import re
from textblob.classifiers import NaiveBayesClassifier
from statistics import mean

client = discord.Client()
cl = None

usersMood = {}

emojis_value = {}

prev_analys_value = []

rate_on_server = False

smiley_faces = [':rage',':angry:',':worried:',':disappointed:',':neutral_face:',':neutral_face:',':slight_smile:',':grin:',':grinning:',':smiley:',':smiley:']
# The duplicated values are necessary.

def add(args):
    """Add the word in the classifier and in the memory."""
    data_update = [(args['text'], args['label'])]
    cl.update(data_update)
    with open('data_small.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow((args['text'], args['label']))


def analyse_sentence(cl, sentence):
    """Return the data from the analyse."""
    prob_dist = cl.prob_classify(sentence)
    return f"""\
max {prob_dist.max()}
pos {prob_dist.prob('pos'):.2f}
neg {prob_dist.prob('neg'):.2f}
    """


def print_emoticon(value):
    """Return the emotion as an emoticon."""
    return smiley_faces[int(value * 10)]


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
    global rate_on_server
    if message.author != client.user:
        if message.content.startswith("!show"):
            output = ""
            for key, value in usersMood.items():
                a = mean(value)
                print(key, usersMood[key], a)
                output += key + " " + print_emoticon(mean(value)) + "\n"
            if output != "":
                await client.send_message(message.channel, output)
        elif message.content.startswith("!reset"):
            usersMood.pop(message.author.name, None)
        elif message.content.startswith("!rate"):
            if re.search(r'\bon\b', message.content):
                rate_on_server = True
            elif re.search(r'\boff\b', message.content):
                rate_on_server = False
        else:
            content = re.sub(r'([a-z]*):(//)?\S*\.+([^\s]*)', '', message.content).strip()
            content = ' '.join(content.split())
            if content != "":
                prob_dist = cl.prob_classify(message.clean_content)
                if message.author.name not in usersMood:
                    usersMood[message.author.name] = []
                usersMood[message.author.name].append(round(prob_dist.prob("pos"), 2))
                prev_analys_value.append(round(prob_dist.prob("pos"), 2))
                if len(prev_analys_value) > 10:
                    temp_list = prev_analys_value[-10:]
                    prev_analys_value[:] = temp_list
                if len(prev_analys_value) == 10 and mean(prev_analys_value) < 0.4:
                    await client.send_message(message.channel,"Voici un clown pour détendre l'atmosphère : \N{CLOWN FACE}")
                    prev_analys_value.clear()
                an_sen = analyse_sentence(cl, message.clean_content)
                if rate_on_server:
                    await client.send_message(message.channel,an_sen)
                print(an_sen)


@client.event
async def on_reaction_add(reaction, user):
    """Executed when a new reaction is added to a message."""
    if reaction.message.author != client.user and reaction.emoji in emojis_value.keys():
        for line in reaction.message.clean_content.splitlines():
            for part in line.split(","):
                entry = {}
                part = re.sub(r'([a-z]*):(//)?\S*\.+([^\s]*)', '', part).strip()
                part = ' '.join(part.split())
                entry['text'] = part
                entry['label'] = emojis_value[reaction.emoji]
                if part != "":
                    add(entry)


with open('emoticonsData.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        emojis_value[row[0]] = row[1]

with open('data_small.csv', 'r') as f:
    cl = NaiveBayesClassifier(f, format="csv")

with open('tokenfile.txt', 'r') as f:
    for line in f:
        client.run(line)
