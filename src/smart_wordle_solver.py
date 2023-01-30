#!/usr/bin/env python3

from wordle_solver import BasicWordlePlayer
from collections import defaultdict

TWIN_TRANSITION = 112 / 51788
REPEATED_LETTERS = 511 / 64735

class SmartWordlePlayer2(BasicWordlePlayer):

    def make_next_guess(self, attempt_num):

        ## Compute letters and transitions frequencies from remaining pool of guesses
        letter_freqs, transitions_freqs = self.letter_transition_probs(self.valid_guesses)

        #next_guess, prob = self.find_best_guess(letter_freqs, transitions_freqs, self.valid_guesses)

        best_guesses = self.find_next_guess(letter_freqs, transitions_freqs, self.valid_guesses)
        next_guess = (None, 0)
        for ii in range(0, 5):
            if best_guesses[ii][1] > next_guess[1]:
                next_guess = best_guesses[ii]

        print(f'Guess {attempt_num}: {next_guess[0]}')
        #print(f'Valid words remaining = {len(self.valid_guesses)}')
        print(f'Other potential candidates: {best_guesses}')

        self.latest_guess = next_guess[0]

        return next_guess[0]

    def recompute_letter_transition_freqs(self, words_space):
        letters_freqs = defaultdict(lambda: 0)
        transitions_freqs = defaultdict(lambda: 0)

        letters_space_size = 5 * len(words_space)
        transitions_space_size = 4 * len(words_space)

        for word in words_space:
            word = word.strip()

            penalize = False
            for ii, char in enumerate(word):
                letters_freqs[char] += 1

                if ii != 4:
                    transitions_freqs[(char, word[ii+1])] += 1

        for key, val in letters_freqs.items():
            letters_freqs[key] = letters_freqs[key] / letters_space_size

        for key, val in transitions_freqs.items():
            transitions_freqs[key] = transitions_freqs[key] / transitions_space_size

        return letters_freqs, transitions_freqs

    def letter_transition_probs(self, words_space):
        letters_freqs = defaultdict(lambda: 0)
        transitions_freqs = defaultdict(lambda: 0)

        for word in words_space:
            word = word.strip()

            for ii, char in enumerate(word):
                letters_freqs[(char, ii)] += 1

                if ii != 4:
                    transitions_freqs[(char, ii, word[ii+1], ii+1)] += 1

        for key, val in letters_freqs.items():
            letters_freqs[key] = letters_freqs[key] / len(words_space)

        for key, val in transitions_freqs.items():
            transitions_freqs[key] = transitions_freqs[key] / len(words_space)

        return letters_freqs, transitions_freqs

    def find_best_guess(self, letters_freqs, transitions_freqs, words_space):

        best_guess = [(None, 0), (None, 0), (None, 0), (None, 0), (None, 0)]

        repeated_letters_prob = self.duplicate_letter_probability(words_space)

        repeated_transitions_prob = self.duplicate_transition_probability(words_space)
        for word in words_space:
            word_prob = 1
            word_list = list(word)
            penalize = False
            seen_letters = list()
            for ii, ll in enumerate(word_list):
                if word.count(ll) > 1 and ll not in seen_letters:
                    word_prob = word_prob * pow(repeated_letters_prob, word.count(ll) - 1)
                    seen_letters.append(ll)

                if ii == 0:
                    word_prob = word_prob * letters_freqs[ll]
                else:
                    if ii != 4 and word.count(word[ii:ii+2]) > 1:
                        penalize = True

                    word_prob = word_prob * transitions_freqs[(word_list[ii - 1], ll)] / letters_freqs[word_list[ii - 1]]

            if penalize:
                word_prob = word_prob * repeated_transitions_prob

            for ii in range(0, 5):
                if best_guess[ii][1] < word_prob and (word, word_prob) not in best_guess:
                    best_guess[ii] = (word, word_prob)
            #if best_guess[1] < word_prob:
                #best_guess = (word, word_prob)

        return best_guess

    def find_next_guess(self, letters_freqs, transitions_freqs, words_space):

        best_guess = [(None, 0), (None, 0), (None, 0), (None, 0), (None, 0)]

        repeated_letters_prob = self.duplicate_letter_probability(words_space)

        repeated_transitions_prob = self.duplicate_transition_probability(words_space)
        for word in words_space:
            word_prob = 1
            word_list = list(word)
            penalize = False
            seen_letters = list()
            for ii, ll in enumerate(word_list):
                if word.count(ll) > 1 and ll not in seen_letters:
                    word_prob = word_prob * pow(repeated_letters_prob, word.count(ll) - 1)
                    seen_letters.append(ll)

                if ii == 0:
                    word_prob = word_prob * letters_freqs[(ll, ii)]
                else:
                    if ii != 4 and word.count(word[ii:ii+2]) > 1:
                        penalize = True

                    word_prob = word_prob * transitions_freqs[(word_list[ii - 1], ii - 1, ll, ii)] / letters_freqs[(word_list[ii - 1], ii -1)]

            if penalize:
                word_prob = word_prob * repeated_transitions_prob

            for ii in range(0, 5):
                if best_guess[ii][1] < word_prob and (word, word_prob) not in best_guess:
                    best_guess[ii] = (word, word_prob)
            #if best_guess[1] < word_prob:
                #best_guess = (word, word_prob)

        return best_guess

    def duplicate_transition_probability(self, words_space):

        transitions_space_size = len(words_space) * 4
        transitions_count = 0
        for word in words_space:
            transitions = False
            for ii in range(0, 4):
                if word.count(word[ii:ii + 2]) > 1:
                    transitions = True
                    break
            if transitions:
                transitions_count += 1

        transitions_prob = transitions_count / transitions_space_size

        return transitions_prob

    def duplicate_letter_probability(self, words_space):

        letters_space_size = len(words_space) * 5
        repeated_letters_count = 0

        for word in words_space:
            seen_letters = list()
            for ii in range(0, 5):
                if word.count(word[ii]) > 1 and word[ii] not in seen_letters:
                    repeated_letters_count += word.count(word[ii]) - 1
                    seen_letters.append(word[ii])

        repeated_letters_prob = repeated_letters_count / letters_space_size

        #print(repeated_letters_count)

        #print(letters_space_size)

        #print(repeated_letters_prob)

        return repeated_letters_prob

class SmartWordlePlayer(BasicWordlePlayer):

    def make_next_guess(self, attempt_num):

        ## Compute letters and transitions frequencies from remaining pool of guesses
        letter_freqs, transitions_freqs = self.recompute_letter_transition_freqs(self.valid_guesses)

        #next_guess, prob = self.find_best_guess(letter_freqs, transitions_freqs, self.valid_guesses)

        best_guesses = self.find_best_guess(letter_freqs, transitions_freqs, self.valid_guesses)
        next_guess = (None, 0)
        for ii in range(0, 5):
            if best_guesses[ii][1] > next_guess[1]:
                next_guess = best_guesses[ii]

        print(f'Guess {attempt_num}: {next_guess[0]}')
        #print(f'Valid words remaining = {len(self.valid_guesses)}')
        print(f'Other potential candidates: {best_guesses}')

        self.latest_guess = next_guess[0]

        return next_guess[0]

    def recompute_letter_transition_freqs(self, words_space):
        letters_freqs = defaultdict(lambda: 0)
        transitions_freqs = defaultdict(lambda: 0)

        letters_space_size = 5 * len(words_space)
        transitions_space_size = 4 * len(words_space)

        for word in words_space:
            word = word.strip()

            penalize = False
            for ii, char in enumerate(word):
                letters_freqs[char] += 1

                if ii != 4:
                    transitions_freqs[(char, word[ii+1])] += 1

        for key, val in letters_freqs.items():
            letters_freqs[key] = letters_freqs[key] / letters_space_size

        for key, val in transitions_freqs.items():
            transitions_freqs[key] = transitions_freqs[key] / transitions_space_size

        return letters_freqs, transitions_freqs

    def letter_transition_probs(self, words_space):
        letters_freqs = defaultdict(lambda: 0)
        transitions_freqs = defaultdict(lambda: 0)

        letters_space_size = 5 * len(words_space)
        transitions_space_size = 4 * len(words_space)

        for word in words_space:
            word = word.strip()

            #penalize = False
            for ii, char in enumerate(word):
                letters_freqs[(char, ii)] += 1

                if ii != 4:
                    transitions_freqs[(char, ii, word[ii+1], ii+1)] += 1

        for key, val in letters_freqs.items():
            letters_freqs[key] = letters_freqs[key] / len(words_space)

        for key, val in transitions_freqs.items():
            transitions_freqs[key] = transitions_freqs[key] / len(words_space)

        return letters_freqs, transitions_freqs

    def find_best_guess(self, letters_freqs, transitions_freqs, words_space):

        best_guess = [(None, 0), (None, 0), (None, 0), (None, 0), (None, 0)]

        repeated_letters_prob = self.duplicate_letter_probability(words_space)

        repeated_transitions_prob = self.duplicate_transition_probability(words_space)
        for word in words_space:
            word_prob = 1
            word_list = list(word)
            penalize = False
            seen_letters = list()
            for ii, ll in enumerate(word_list):
                if word.count(ll) > 1 and ll not in seen_letters:
                    word_prob = word_prob * pow(repeated_letters_prob, word.count(ll) - 1)
                    seen_letters.append(ll)

                if ii == 0:
                    word_prob = word_prob * letters_freqs[ll]
                else:
                    if ii != 4 and word.count(word[ii:ii+2]) > 1:
                        penalize = True

                    word_prob = word_prob * transitions_freqs[(word_list[ii - 1], ll)] / letters_freqs[word_list[ii - 1]]

            if penalize:
                word_prob = word_prob * repeated_transitions_prob

            for ii in range(0, 5):
                if best_guess[ii][1] < word_prob and (word, word_prob) not in best_guess:
                    best_guess[ii] = (word, word_prob)
            #if best_guess[1] < word_prob:
                #best_guess = (word, word_prob)

        return best_guess

    def find_next_guess(self, letters_freqs, transitions_freqs, words_space):

        best_guess = [(None, 0), (None, 0), (None, 0), (None, 0), (None, 0)]

        repeated_letters_prob = self.duplicate_letter_probability(words_space)

        repeated_transitions_prob = self.duplicate_transition_probability(words_space)
        for word in words_space:
            word_prob = 1
            word_list = list(word)
            penalize = False
            seen_letters = list()
            for ii, ll in enumerate(word_list):
                if word.count(ll) > 1 and ll not in seen_letters:
                    word_prob = word_prob * pow(repeated_letters_prob, word.count(ll) - 1)
                    seen_letters.append(ll)

                if ii == 0:
                    word_prob = word_prob * letters_freqs[(ll, ii)]
                else:
                    if ii != 4 and word.count(word[ii:ii+2]) > 1:
                        penalize = True

                    word_prob = word_prob * transitions_freqs[(word_list[ii - 1], ii - 1, ll, ii)] / letters_freqs[(word_list[ii - 1], ii -1)]

            if penalize:
                word_prob = word_prob * repeated_transitions_prob

            if word == 'stair':
                print(f'Prob of stair: {word_prob}')

            for ii in range(0, 5):
                if best_guess[ii][1] < word_prob and (word, word_prob) not in best_guess:
                    best_guess[ii] = (word, word_prob)
            #if best_guess[1] < word_prob:
                #best_guess = (word, word_prob)

        return best_guess

    def duplicate_transition_probability(self, words_space):

        transitions_space_size = len(words_space) * 4
        transitions_count = 0
        for word in words_space:
            transitions = False
            for ii in range(0, 4):
                if word.count(word[ii:ii + 2]) > 1:
                    transitions = True
                    break
            if transitions:
                transitions_count += 1

        transitions_prob = transitions_count / transitions_space_size

        return transitions_prob

    def duplicate_letter_probability(self, words_space):

        letters_space_size = len(words_space) * 5
        repeated_letters_count = 0

        for word in words_space:
            seen_letters = list()
            for ii in range(0, 5):
                if word.count(word[ii]) > 1 and word[ii] not in seen_letters:
                    repeated_letters_count += word.count(word[ii]) - 1
                    seen_letters.append(word[ii])

        repeated_letters_prob = repeated_letters_count / letters_space_size

        #print(repeated_letters_count)

        #print(letters_space_size)

        #print(repeated_letters_prob)

        return repeated_letters_prob




if __name__ == '__main__':
    all_words = open('../all_words.txt')
    words_space = list()

    for line in all_words.readlines():
        words_space.append(line.strip())

    player = SmartWordlePlayer2(words_space)
    #player.valid_guesses = ['stare', 'tears']

    #player.duplicate_letter_probability()

    #player.duplicate_transition_probability()

    player.make_next_guess(1)

    all_words.close()
