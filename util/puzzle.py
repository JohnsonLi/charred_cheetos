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
        for tries in range(max_tries):
            if insert_word(word):
                break
    fillRandom()
    result = {}
    result['puzzle'] = ws
    result['words'] = added_words

    return ws

def is_outside(r, c, size):
    return r < 0 or r >= size or c < 0 or c >= size

def insert_word(word):
    offset_r = random.choice(offset)
    offset_c = random.choice(offset)

    r = random.randint(0,9)
    c = random.randint(0,9)

    if(offset_r == 0 and offset_c == 0):
        return False

    for i in range(len(word)):
        row_ind = r + offset_r * i
        col_ind = c + offset_c * i

        # print(str(row_ind) + " " + str(col_ind))

        if is_outside(row_ind, col_ind, size):
            return False

        if word[i] != ws[row_ind][col_ind] and ws[row_ind][col_ind] != '_':
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

