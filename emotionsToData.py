marginPos = 0.15
marginNeg = -0.15

with open('emoticons.csv', 'r', encoding='utf-8') as fin, open('emoticonsData.csv', 'w', encoding='utf-8') as fou:
    for line in fin:
        currentEmoticon = line.split(",")
        emoticon = currentEmoticon[0]
        unicode = currentEmoticon[1]
        occurence = float(currentEmoticon[2])
        negative = float(currentEmoticon[4])
        positive = float(currentEmoticon[6])

        result = (-negative + positive) / occurence
        if result <= marginNeg:
            fou.write(emoticon + ",neg\n")
        elif result >= marginPos:
            fou.write(emoticon + ",pos\n")
