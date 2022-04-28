import random

class InteractiveWordlePlayer:

    def __init__(self):
        pass

    def make_next_guess(self, attempt_number):

        guess_input = input(f'Guess {attempt_number}: ')

        return guess_input

    def update_valid_guesses(self, guess_stats):
        pass

class BasicWordlePlayer:

    def __init__(self, words_space=list()):
        self.words_space = list(words_space)
        self.valid_guesses = list(words_space)
        self.guesses = list()
        self.all_stats = {0: set(), 1: set(), 2: set()}
        self.latest_guess = None


    def make_next_guess(self, attempt_number):

        random_index = random.randint(0, len(self.valid_guesses) - 1)
        new_guess = self.valid_guesses[random_index]
        self.latest_guess = new_guess

        print(f'Guess {attempt_number}: {new_guess}')
        print(f'Valid words remaining = {len(self.valid_guesses)}')

        return new_guess

    def update_valid_guesses(self, guess_stats):

        guess_word = self.latest_guess
        guess_marks = guess_stats

        ## Map each letter of the guess word to its numerical value obtained in the last reply
        guess_word_list = list(guess_word)
        assert len(guess_word_list) == len(guess_marks), 'word length and marks must have the same length'
        ## Then append these letters to the entire history of guesses
        for mark, char in zip(guess_marks, guess_word_list):
            self.all_stats[mark].add(char)

        ## Step 1: Categories letters based on the marks fetched from the reply received to the latest guess made

        ## Letters that must be at its corresponding index in the winning guess
        confirmed_letters = set()
        ## Letters that cannot be present in the winning guess at its corresponding position. They are also letters that have been identified as confirmed letters in the winning guess but at another position
        false_duplicates = set()
        ## Letters that cannot be at any position in the winning guess
        forbidden_letters = set()
        ## Letters that part of the winning guess but at another index position
        present_letters = set()

        ## Combined set of cumulative confirmed and must have letters
        present_and_confirmed_letters = set.union(self.all_stats[1], self.all_stats[2])

        ## Adding letters from the latest guess to their categories
        for ii in range(0, len(guess_word_list)):
            if (guess_marks[ii] == 0):
                if (guess_word_list[ii] in present_and_confirmed_letters):
                    false_duplicates.add((guess_word_list[ii], ii))
                else:
                    forbidden_letters.add((guess_word_list[ii], ii))
            elif (guess_marks[ii] == 1):
                if (guess_word_list[ii] in self.all_stats[2]):
                    false_duplicates.add((guess_word_list[ii], ii))
                else:
                    present_letters.add((guess_word_list[ii], ii))
            elif (guess_marks[ii] == 2):
                confirmed_letters.add((guess_word_list[ii], ii))

        ## Step 2: Removing wrong guesses from the word list

        # Remove latest try from the list of words
        self.valid_guesses.remove(guess_word)

        ## Use hints to filter out the word list of wrong guesses
        size = len(self.valid_guesses)
        ii = 0
        while (ii < size):
            word = self.valid_guesses[ii]
            word_removed = False

            for confirmed_letter in confirmed_letters:
                if (word[confirmed_letter[1]] != confirmed_letter[0]):
                    self.valid_guesses.remove(word)
                    word_removed = True
                    ## Adjust indexing of the list after removing element
                    ii -= 1
                    size -= 1
                    break

            if (word_removed == True):
                ii += 1
                continue

            for false_duplicate in false_duplicates:
                if (word[false_duplicate[1]] == false_duplicate[0]):
                    self.valid_guesses.remove(word)
                    word_removed = True
                    ii -= 1
                    size -= 1
                    break

            if (word_removed == True):
                ii += 1
                continue

            for forbidden_letter in forbidden_letters:
                if (forbidden_letter[0] in word):
                    self.valid_guesses.remove(word)
                    word_removed = True
                    ## Adjust indexing of the list after removing element
                    ii -= 1
                    size -= 1
                    break

            if (word_removed == True):
                ii += 1
                continue

            for present_letter in present_letters:
                if ((present_letter[0] not in word) or (word[present_letter[1]] == present_letter[0])):
                    self.valid_guesses.remove(word)
                    word_removed = True
                    ## Adjust indexing of the list after removing element
                    ii -= 1
                    size -= 1
                    break

            ii += 1
