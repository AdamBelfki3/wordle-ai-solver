#!/usr/bin/env python3

def main():

    all_words = open('../all_words.txt')
    all_words_lines = all_words.readlines()

    all_words_list = list()

    for word in all_words_lines:
        all_words_list.append(word.strip())

    guess_space_dict = dict()

    max_word = None
    max_guess_space = 0
    min_word = None
    min_guess_space = float('+inf')

    for word in all_words_list:
        #count = 0
        guess_space = list()
        for guess_candidate in all_words_list:
            add = True
            for l in list(word):
                if l in guess_candidate:
                    add = add and False

            if add:
                #count += 1
                guess_space.append(guess_candidate)

        guess_space_dict[word] = guess_space

        if len(guess_space) > max_guess_space:
            max_guess_space = len(guess_space)
            max_word = word

        if len(guess_space) < min_guess_space:
            min_guess_space = len(guess_space)
            min_word = word



    print(f'Word will biggest guess space {max_word}')
    print(f'Guess space size {max_guess_space}')
    print(f'Guess space for word {max_word}')

    print('\n')
    print(f'Word with smallest guess space {min_word}')
    print(f'Guess space size {min_guess_space}')

    total_guess_space_size = 0

    for value in guess_space_dict.values():
        total_guess_space_size += len(value)

    print(f'average guess space size: {total_guess_space_size / len(all_words_lines)}')
    print('\n')
    print(f'Guess space size for word chare: {len(guess_space_dict["chare"])}')


    all_words.close()

if __name__ == '__main__':
    main()
