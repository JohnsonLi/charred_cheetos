import urllib.request, json, ssl, random

dmUrl = "https://api.datamuse.com/words?topic={0}"

def randomWords(list, num):
    newList = []
    i = 0
    while ( i < num ):
        r = random.randint(0, len(list))
        i+= 1
        newList.append(list[i])
    return newList


def categoryWords(category, num):
    dmUrl.format(category)
    
