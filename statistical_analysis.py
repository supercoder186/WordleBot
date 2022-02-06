import player

current_answer = ''
guess_counts = []


def result_function(guess, alt_answer=''):
    global current_answer

    result = [0, 0, 0, 0, 0]
    answer = alt_answer if(alt_answer) else current_answer
    answer_list = list(answer)

    to_pop = []

    # First, find all 2s
    for i in range(5):
        if(guess[i] == answer[i]):
            result[i] = 2
            to_pop.append(i)

    if to_pop:
        for i in range(len(to_pop) - 1, 0):
            answer_list.pop(i)

    # Next find all 1s
    for i in range(5):
        if(guess[i] in answer_list and result[i] != 2):
            result[i] = 1
            answer_list.remove(guess[i])

    return (guess, result)


def sort_key(e):
    return e[1]


def analyse_opener(word_filename='sgb-words.txt', output_filename='avg_guess_counts.txt'):
    global current_answer

    words = []
    with open('sgb-words.txt', 'r+') as word_file:
        words = [word[:5] for word in word_file.readlines()]

    answers = []
    with open('old_answers.txt', 'r+') as word_file:
        answers = [answer[:-1].lower() for answer in word_file.readlines()]

    for i in range(len(words)):  # for each opening word
        opener = words[i]
        guess_count = 0
        num_guesses = 0
        for answer in answers:
            current_answer = answer
            c = player.play(result_function, opener=opener, to_print=False, word_file=word_filename)
            if c != 1:
                guess_count += c
                num_guesses += 1

        avg_guesses = float(guess_count) / float(num_guesses)
        guess_counts.append((opener, avg_guesses))
        print('{}: Opener {} of {} Average Guess Count:{}'.format(
            opener, i + 1, len(words), avg_guesses))

    guess_counts.sort(key=sort_key)
    print(guess_counts[:20])

    with open(output_filename, 'w') as f:
        for g in guess_counts:
            f.write('{}\n'.format(g))


def analyse_word_list(word_filename):
    global current_answer

    answers = []
    with open('old_answers.txt', 'r+') as word_file:
        answers = [answer[:-1].lower() for answer in word_file.readlines()]
    
    guess_count = 0
    num_guesses = 0
    for answer in answers:
        current_answer = answer
        c = player.play(result_function, to_print=False, word_file=word_filename)
        if c != 1:
            guess_count += c
            num_guesses += 1

    avg_guesses = float(guess_count) / float(num_guesses)
    print('Average guesses: {}'.format(avg_guesses))


if(__name__ == "__main__"):
    analyse_opener(word_filename='updated_words.txt', output_filename='avg_guess_counts_updated.txt')
    # analyse_word_list('sgb-words.txt')
    