#!/usr/bin/env python3 -u
import argparse
import random
from wordle_solver import InteractiveWordlePlayer
from wordle_solver import BasicWordlePlayer
from smart_wordle_solver import SmartWordlePlayer, SmartWordlePlayer2
from wordle_play_agents import WordleSearchProblem, custom_depth_first_search

DEFAULT_WORDS = './all_words.txt'
DEFAULT_ATTEMPTS = 6
DEFAULT_PLAYER = 'interactive'
GREEN_TILE = '🟩'
YELLOW_TILE = '🟨'
WHITE_TILE = '⬜'

class WordleGame:
    def __init__(self, word, words_path, attempts_lim, visuals = True, player=None):
        self.wordle_space = self.create_wordle_space(words_path)
        self.wordle = self.generate_wordle(word)
        self.attempt_number = 0
        self.attempts_lim = attempts_lim
        self.wrong_letters = set()
        self.guesses = dict()
        self.emoji_score_sheet = list()
        self.player = player
        self.visuals = visuals  

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

        return guess == self.wordle

    def get_guess_feedback(self, guess):
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
            return guess_stats, guess_stats_emoji

        counter = 0
        wordle_letters_remaining = [x[1] for x in wordle_list]
        while counter < len(guess_list):
            if guess_list[counter][1] not in wordle_letters_remaining:
                idx = guess_list[counter][0]
                guess_stats[idx] = 0
                guess_stats_emoji[idx] = WHITE_TILE
                self.wrong_letters.add(guess_list[counter][1])
                guess_list.remove(guess_list[counter])
            else:
                counter += 1

        if len(guess_list) == 0:
            guess_stats_emoji = ''.join(guess_stats_emoji)
            return guess_stats, guess_stats_emoji

        counter = 0
        for letter in guess_list:
            if letter[1] in wordle_letters_remaining:
                guess_stats[letter[0]] = 1
                guess_stats_emoji[letter[0]] = YELLOW_TILE
                wordle_letters_remaining.remove(letter[1])
            else:
                guess_stats[letter[0]] = 0
                guess_stats_emoji[letter[0]] = WHITE_TILE
                self.wrong_letters.add(letter[1])


        guess_stats_emoji = ''.join(guess_stats_emoji)
        return guess_stats, guess_stats_emoji

    def run(self, guesses=list()):
        self.attempt_number = 0
        self.wrong_letters = set()
        self.guesses = dict()
        self.emoji_score_sheet = list()

        while self.attempt_number < self.attempts_lim:
            self.attempt_number += 1

            guess_input = None
            if guesses != list():
                guess_input = guesses[self.attempt_number - 1]
                if self.visuals:
                    print(f'Guess {self.attempt_number}: {guess_input}')
            else:
                guess_input = self.player.make_next_guess(self.attempt_number)

            if guess_input == '-wl':
                print('Wrong letters found ' + WHITE_TILE)
                print(list(self.wrong_letters))
                self.attempt_number -= 1
                continue

            guess_input = guess_input.lower()

            try:
                guess_stats, guess_stats_emoji = self.get_guess_feedback(guess_input)
            except:
                print('Invalid guess. Try with another word!')
                self.attempt_number -= 1
                continue

            if guesses == list():
                self.player.update_valid_guesses(guess_stats)

            self.guesses[guess_input] = guess_stats
            self.emoji_score_sheet.append(guess_stats_emoji)

            if self.visuals:
                print(guess_stats_emoji)

            if guess_input == self.wordle:
                if self.visuals:
                    print('\n')
                    print('You win!')
                    print('\n'.join(self.emoji_score_sheet))

                return self.attempt_number

        if self.visuals:
            print('\n')
            print('You are out of guess. Better luck next time ;)')
            print(f'The Wordle was {self.wordle}')
            print('\n'.join(self.emoji_score_sheet))

        return self.attempts_lim + 1

class InteractiveWordlePlayer:

    def __init__(self):
        pass

    def make_next_guess(self, attempt_number):

        guess_input = input(f'Guess {attempt_number}: ')

        return guess_input

    def update_valid_guesses(self, guess_stats):
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Wordle Game')
    parser.add_argument('-w', dest="wordle", type=str, default="", help="Worlde word")
    parser.add_argument('-l', dest="words_path", type=str, default=DEFAULT_WORDS, help="Path to all valid words")
    parser.add_argument('-a', dest="attempts", type=int, default=DEFAULT_ATTEMPTS, help="Number of attemps allowed for a game session")
    parser.add_argument('-p', dest="player", type=str, default=DEFAULT_PLAYER, help="Player to solve the Wordle")
    args = parser.parse_args()

    print('>>>>>> Wordle Game <<<<<<\n')

    if args.player == 'compare':
        wordle_game = WordleGame(args.wordle, args.words_path, args.attempts)

        guesser = WordleSearchProblem(wordle_game)

        guesses_1 = custom_depth_first_search(guesser, True)
        guesses_2 = custom_depth_first_search(guesser, False)

        print('Random Guesser:')
        wordle_game.run(guesses_1)

        print('\n')

        print('Probabilistic Guesser:')
        wordle_game.run(guesses_2)

    else:
        wordle_game = WordleGame(args.wordle, args.words_path, args.attempts)
        guesser = WordleSearchProblem(wordle_game)

        player = None
        guesses = list()
        if args.player == 'interactive':
            player = InteractiveWordlePlayer()
        elif args.player == 'random':
            guesses = custom_depth_first_search(guesser, True)
        elif args.player == 'probabilistic':
            guesses = custom_depth_first_search(guesser, False)

        wordle_game.player = player

        wordle_game.run(guesses)
