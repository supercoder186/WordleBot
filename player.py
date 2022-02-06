import re


# result array format
# 0 - not in word, 1 - in word but wrong place, 2 - in word & right place
words = []
word_picture = []
letters_in_word = []
OPENING_WORD = 'tears'


def reset(word_file_name):
    global words, word_picture, letters_in_word
    with open(word_file_name, 'r+') as word_file:
        words = [word[:5] for word in word_file.readlines()]
    word_picture = [r'\w', r'\w', r'\w', r'\w', r'\w']
    letters_in_word = []


def guess_first(state, word_list):
    if not state:
        return OPENING_WORD
    return word_list[0]


def process_result_eliminator(result):

    word = result[0]

    eliminate_word(word)

    result = result[-1]
    for i in range(5):
        l = word[i]
        r = result[i]
        if(r == 0):
            eliminate_words_0(l)
        elif(r == 1):
            letters_in_word.append(l)
            eliminate_words_1(i, l)
        else:
            letters_in_word.append(l)
            word_picture[i] = l
            eliminate_words_2()


def eliminate_word(w):
    global words

    new_words = []
    for word in words:
        if(not word == w):
            new_words.append(word)

    words = new_words


def eliminate_words_0(l):
    global words

    if(l in letters_in_word):
        return

    new_words = []
    for word in words:
        if(l not in word):
            new_words.append(word)

    words = new_words


def eliminate_words_1(i, l):
    global words

    new_words = []
    for word in words:
        if(l in word and word[i] != l):
            new_words.append(word)

    words = new_words


def eliminate_words_2():
    global words

    pattern = ''
    for l in word_picture:
        pattern += l

    new_words = []
    regex = re.compile(pattern)
    for word in words:
        if (regex.match(word)):
            new_words.append(word)

    words = new_words


def get_result_uinput(guess):
    result_str = input('Guess: {} Enter result: '.format(guess))
    return (guess, [int(i) for i in result_str][:5])


def play(result_function, guess_function=guess_first, result_process_function=process_result_eliminator, opener='tears', to_print=True, word_file='sgb-words.txt'):
    global OPENING_WORD
    reset(word_file)

    OPENING_WORD = opener

    for i in range(20):
        bot_guess = guess_function(i, words)
        result = result_function(bot_guess)

        if(result[1] == [2, 2, 2, 2, 2]):
            if to_print:
                print('Success! Guess count: {}'.format(i + 1))
            return i + 1

        result_process_function(result)


if(__name__ == "__main__"):
    play(get_result_uinput)
