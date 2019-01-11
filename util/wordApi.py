import urllib.request, json, ssl, random

ctxt = ssl._create_unverified_context()

dmUrl = "https://api.datamuse.com/words?topics={0}"

def randomWords(wordList, num): #returns random words from a list (num is number of words returned)
    newList = []
    i = 0
    while ( i < num ):
        r = random.randint(0, len(wordList))
        i += 1
        newList.append(wordList[i])
    return newList


def category(category): #returns all words in a category
    url = dmUrl.format(category)
    req = urllib.request.urlopen(url, context = ctxt)
    data = json.loads(req.read())
    words = []
    for d in data:
        if ' ' not in d["word"]:
            words.append(d["word"])
    return words

def rangeWords(start,end,wordList): #returns words between start and end index of a list (ex: words 28-45 of food category)
    i = start
    words = []
    while ( i < end ):
        try:
            words.append(wordList[i])
        except:
            break
        i += 1
    return words

nature = category("nature")
print(nature)
print(randomWords(nature, 15))
print(rangeWords(0,10,nature))
