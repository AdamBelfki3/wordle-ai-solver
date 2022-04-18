#!/usr/bin/env python3
import argparse
import random

DEFAULT_WORDS = './all_words.txt'
GREEN_TILE = '🟩'
YELLOW_TILE = '🟨'
WHITE_TILE = '⬜'

class WordleGame:
    def __init__(self, word, words_path):
        self.wordle_space = self.create_wordle_space(words_path)
        self.wordle = self.generate_wordle(word)
        self.attempt_number = 0
        #self.confirmed_letters = set()
        #self.misplaced_letters = set()
        #self.wrong_letters = set()
        self.guesses = dict()

    def create_wordle_space(self, path):
        wordle_space = set()
        words_file = open(path, 'r')
        all_words = words_file.readlines()

        for word in all_words:
            wordle_space.add(word.strip())

        words_file.close()

        return wordle_space

    def generate_wordle(self, word):
        if word not in self.wordle_space:
            words = list(self.wordle_space)
            rand_index = random.randint(0, len(words) - 1)

            return words[rand_index]
        else:
            return word

    def verify_guess(self, guess):
        print(guess)
        guess_stats = [-1, -1, -1, -1, -1]
        guess_stats_emoji = list("zzzzz")
        if len(guess) != 5:
            raise ValueError('Invalid word length, correct length is 5')

        if guess not in self.wordle_space:
            raise ValueError('Invalid guess word')

        guess_list = list(enumerate(guess))
        wordle_list = list(enumerate(self.wordle))

        counter = 0
        while counter < len(guess_list):
            if guess_list[counter] == wordle_list[counter]:
                idx = guess_list[counter][0]
                guess_stats[idx] = 2
                guess_stats_emoji[idx] = GREEN_TILE
                guess_list.remove(guess_list[counter])
                wordle_list.remove(wordle_list[counter])
            else:
                counter += 1

        if len(guess_list) == 0:
            guess_stats_emoji = ''.join(guess_stats_emoji)
            print(guess_stats)
            print(guess_stats_emoji)
            return guess_stats

        counter = 0
        wordle_letters_remaining = [x[1] for x in wordle_list]
        while counter < len(guess_list):
            if guess_list[counter][1] not in wordle_letters_remaining:
                idx = guess_list[counter][0]
                guess_stats[idx] = 0
                guess_stats_emoji[idx] = WHITE_TILE
                guess_list.remove(guess_list[counter])
            else:
                counter += 1

        if len(guess_list) == 0:
            guess_stats_emoji = ''.join(guess_stats_emoji)
            print(guess_stats)
            print(guess_stats_emoji)
            return guess_stats

        counter = 0
        for letter in guess_list:
            if letter[1] in wordle_letters_remaining:
                guess_stats[letter[0]] = 1
                guess_stats_emoji[letter[0]] = YELLOW_TILE
                wordle_letters_remaining.remove(letter[1])
            else:
                guess_stats[letter[0]] = 0
                guess_stats_emoji[letter[0]] = WHITE_TILE


        guess_stats_emoji = ''.join(guess_stats_emoji)
        print(guess_stats)
        print(guess_stats_emoji)
        return guess_stats

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Wordle Game')
    parser.add_argument('-w', dest="wordle", type=str, default="", help="Worlde word")
    parser.add_argument('-l', dest="words_path", type=str, default=DEFAULT_WORDS, help="Path to all valid words")
    args = parser.parse_args()

    wordle_game = WordleGame(args.wordle, args.words_path)
    print(wordle_game.wordle)
    wordle_game.verify_guess('freer')
