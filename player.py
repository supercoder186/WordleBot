import re


# result array format
# 0 - not in word, 1 - in word but wrong place, 2 - in word & right place
words = []  # list of words. Initially taken from the word dictionary. Words are removed after recieving each guess result
word_picture = []  # the confirmed list of which letter is where
letters_in_word = []  # the list of all the confirmed letters in the word, not in order
OPENING_WORD = 'tears'  # the first guess


# resets the bot's state
# word_file_name is the name of the file with the bot's dictionary. The dictionary can be rearranged to optimize performance
def reset(word_file_name):
    global words, word_picture, letters_in_word
    with open(word_file_name, 'r+') as word_file:
        # read the list of words from the dictionary file
        words = [word[:5] for word in word_file.readlines()]
    # reset the word picture
    word_picture = [r'\w', r'\w', r'\w', r'\w', r'\w']
    letters_in_word = []  # reset the letters in the word


# this is the basic guess function, which guesses simply the first word in the list of uneliminated words. very effective
# state is the number of guesses so far. word_list is the current list of words being used by the bot
def guess_first(state, word_list):
    if not state:
        return OPENING_WORD
    return word_list[0]


# the standard word eliminator function
# result_t is the result given by the result calculation function
def process_result_eliminator(result_t):
    # extract the word and its result from the result tuple
    word = result_t[0]
    result = result_t[1]

    eliminate_word(word)  # eliminate the previous guess

    for i in range(5):  # iterate over each letter in the word
        # extract the letter and its corresponding state
        l = word[i]
        r = result[i]

        if(r == 0):  # letter is not in the word
            # eliminate all words in the word list with this letter
            eliminate_words_0(l)
        elif(r == 1):
            # add this letter to the list of confirmed letters
            letters_in_word.append(l)
            # eliminate all words with this letter in this particular position, and all the words without this letter
            eliminate_words_1(i, l)
        else:
            # add this letter to the list of confirmed letters
            letters_in_word.append(l)
            # update the word picture
            word_picture[i] = l
            # eliminate all words that don't correspond to the updated word picture
            eliminate_words_2()


# w is the word to be eliminated
def eliminate_word(w):  # remove a word from the word list
    global words

    new_words = []
    for word in words:
        if(not word == w):
            new_words.append(word)

    words = new_words


# eliminate all words without this letter, unless the letter exists in the word
# l is letter
def eliminate_words_0(l):
    # the letter can exist in the word but have a state of 0 when the guess has more than 1 instance of the letter but the letter only appears once in the word

    global words

    if(l in letters_in_word):
        return

    new_words = []
    for word in words:
        if(l not in word):
            new_words.append(word)

    words = new_words


# eliminate all words with this letter in this particular position, and all the words without this letter
# l is the letter and i is its index
def eliminate_words_1(i, l):
    global words

    new_words = []
    for word in words:
        if(l in word and word[i] != l):
            new_words.append(word)

    words = new_words


def eliminate_words_2():  # eliminate all words that don't correspond to the updated word picture
    global words

    # build a regex pattern corresponding to the word picture
    pattern = ''
    for l in word_picture:
        pattern += l

    # eliminate all the words that do not match the regex pattern
    new_words = []
    regex = re.compile(pattern)
    for word in words:
        if (regex.match(word)):
            new_words.append(word)

    words = new_words


# basic function to get the result of each guess from the user's input
# input is formatted as one string of 5 numbers corresponding to the state of each letter
# black - 0  yellow - 1  green - 2
# eg a guess of 'audit' for an answer of 'audio' would be 22220
# will return a tuple. 0th element is the user's guess and 1st element is the state of each letter
# the example above would return ('audit', [2, 2, 2, 2, 0])
# the guess is the string value of the guess. eg 'audit'
def get_result_uinput(guess):
    result_str = input('Guess: {} Enter result: '.format(guess))
    return (guess, [int(i) for i in result_str][:5])


# simulates a game of wordle
def play(result_function=get_result_uinput, guess_function=guess_first, result_process_function=process_result_eliminator,\
        opener='tears', to_print=True, word_file='sgb-words.txt'):
    global OPENING_WORD
    reset(word_file)  # reset the bot state

    OPENING_WORD = opener

    for i in range(20):
        # make a guess using the inputted guess function
        bot_guess = guess_function(i, words)
        # use the result function to get a result for the guess
        result = result_function(bot_guess)

        if(result[1] == [2, 2, 2, 2, 2]):  # check if the guess is successful
            if to_print:
                print('Success! Guess count: {}'.format(i + 1))
            return i + 1

        # process the returned result from the guess to prepare for the next guess
        result_process_function(result)


if(__name__ == "__main__"):
    play()
