#!/usr/bin/env python3
import argparse
from collections import defaultdict

DEFAULT_WORDS_SPACE = './all_words.txt'
DEFAULT_LETTERS_FREQS = './letter_freqs.tsv'
DEFAULT_TRANSITIONS_FREQS = './transitions_freqs.tsv'


def main(args):

    letters_freqs_dict = defaultdict(lambda: 0)
    transitions_freqs_dict = defaultdict(lambda: 0)

    words_file = open(args.words_path, 'r')
    words_space = words_file.readlines()

    letters_space_size = 5 * len(words_space)
    transitions_space_size = 4 * len(words_space)

    for word in words_space:
        word = word.strip()

        for ii, char in enumerate(word):
            letters_freqs_dict[char] += 1

            if ii != 4:
                transitions_freqs_dict[(char, word[ii+1])] += 1

    letters_freqs = open(args.letters_path, 'w')
    for key, value in letters_freqs_dict.items():
        freq = value / letters_space_size
        letters_freqs.write(f'{key}\t{freq}\n')

    transitions_freqs = open(args.transitions_path, 'w')
    for key, value in transitions_freqs_dict.items():
        freq = value / transitions_space_size
        transitions_freqs.write(f'{key[0]}\t{key[1]}\t{freq}\n')

    letters_freqs.close()
    transitions_freqs.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='crawl Fakebook')
    parser.add_argument('-w', dest="words_path", type=str, default=DEFAULT_WORDS_SPACE, help="Path to all valid words")
    parser.add_argument('-l', dest="letters_path", type=str, default=DEFAULT_LETTERS_FREQS, help="Path to letter frequencies file")
    parser.add_argument('-t', dest="transitions_path", type=str, default=DEFAULT_TRANSITIONS_FREQS, help="Path to transition frequencies file")
    args = parser.parse_args()

    main(args)
