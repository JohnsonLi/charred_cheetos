import random

word_bank = ['cat','bobcat','rhinoceros','communism','dog']
word_bank.sort(key=len)

size = 10
max_tries = 10

ws = [['_' for i in range(size)] for i in range(size)]
offset = [0, 1, -1]

def generate(word_search, word_bank):
    for word in word_bank:
        r = random.randint(0,9)
        c = random.randint(0,9)
        while(word[0] != word_search[r][c] and word_search[r][c] != '_'):
            r = random.randint(0,9)
            c = random.randint(0,9)
        insert_word(ws, word, r, c)
    return word_search

def insert_word(word_search, word, r, c):
    offset_r = random.choice(offset)
    offset_c = random.choice(offset)

    for i in range(max_tries):
        try:
            for char in word:
                word_search[r][c] = char;
                r += offset_r
                c += offset_c
        except:
            continue

# print(word_bank)
generate(ws, word_bank)
print(ws)
