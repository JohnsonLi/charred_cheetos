import random

import wordApi

# word_bank = ['cat','bobcat','rhinoceros','communism','dog']
# word_bank.sort(key=len, reverse=True)
alphabet = "abcdefghijklmnopqrstuvwxyz"

# ws = [['_' for i in range(size)] for i in range(size)]
offset = [0, 1, -1]

def create_puzzle(mode, ws, size, custom_category):
    word_bank = []
    if (mode == "random"):
        word_bank = wordApi.random_list(int(size / 2 + 6))
        # print(word_bank)
    elif (mode == "custom"):
        api_words = wordApi.category(custom_category);
        try:
            word_bank = random.sample(api_words, int(size / 2 + 6))
        except:
            word_bank = api_words
    else:
        api_words = wordApi.category(mode);
        try:
            word_bank = random.sample(api_words, int(size / 2 + 6))
        except:
            word_bank = api_words

    word_bank.sort(key=len, reverse=True)
    max_tries = len(word_bank) * 100
    return generate(word_bank, max_tries, ws, size)

def generate(word_bank, trials, ws, size):
    wb = []
    for word in word_bank:
        # print("trying: " + word)
        for tries in range(trials): # keep inserting until max tries exceeded
            if insert_word(word, ws, size): # go on to next word if current word is inserted
                # print("added: " + word)
                wb.append(word)
                break
    fillRandom(ws, size)
    result = {}
    result['puzzle'] = [[letter.upper() for letter in row] for row in ws]
    result['words'] = [word.upper() for word in wb]

    return result

def is_outside(r, c, size):
    return r < 0 or r >= size or c < 0 or c >= size

def insert_word(word, ws, size):
    # select a direction
    offset_r = random.choice(offset)
    offset_c = random.choice(offset)
    # select a random position on board
    r = random.randint(0,size)
    c = random.randint(0,size)

    if(offset_r == 0 and offset_c == 0):
        return False

    for i in range(len(word)):
        row_ind = r + offset_r * i
        col_ind = c + offset_c * i

        # print(str(row_ind) + " " + str(col_ind))

        if is_outside(row_ind, col_ind, size): # word does not fit
            return False

        if word[i] != ws[row_ind][col_ind] and ws[row_ind][col_ind] != '_': # spot occupied by a different word
            return False

    for char in word:
        # print(str(r) + " " + str(c))
        ws[r][c] = char
        r += offset_r
        c += offset_c

    return True

def to_string(ws):
    string  = ""
    for row in ws:
        for thing in row:
            string += thing + " "
        string += "\n"

    return string

def fillRandom(ws, size):
    for r in range(size):
        for c in range(size):
            if ws[r][c] == "_":
                ws[r][c] = random.choice(alphabet)

# generated = create_puzzle("random")
# print(to_string(generated['puzzle']))
# print(generated['words'])
# print(str(len(generated['words'])) + " words added")
