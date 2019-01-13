import random

word_bank = ['cat','bobcat','rhinoceros','communism','dog']
added_words = []
word_bank.sort(key=len, reverse=True)
alphabet = "abcdefghijklmnopqrstuvwxyz"
size = 12
max_tries = len(word_bank) * 100

ws = [['_' for i in range(size)] for i in range(size)]
offset = [0, 1, -1]

def generate(word_bank):
    for word in word_bank:
        for tries in range(max_tries): # keep inserting until max tries exceeded
            if insert_word(word): # go on to next word if current word is inserted
                break
    fillRandom()
    result = {}
    result['puzzle'] = ws
    result['words'] = added_words

    return result

def is_outside(r, c, size):
    return r < 0 or r >= size or c < 0 or c >= size

def insert_word(word):
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

    added_words.append(word)
    return True

def to_string(ws):
    string  = ""
    for row in ws:
        for thing in row:
            string += thing + " "
        string += "\n"

    return string

def fillRandom():
    for r in range(size):
        for c in range(size):
            if ws[r][c] == "_":
                ws[r][c] = random.choice(alphabet)

generated = generate(word_bank)
# print(to_string(generated['puzzle']))
# print(generated['words'])
