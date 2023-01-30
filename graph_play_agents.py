#!/usr/bin/env python3

from wordle import WordleGame
from wordle_play_agents import WordleSearchProblem, custom_depth_first_search
from collections import defaultdict
import plotly.graph_objects as go

DEFAULT_WORDS = './all_words.txt'
DEFAULT_ATTEMPTS = 6
DEFAULT_PLAYER = 'interactive'

def main():

    games_num = 100
    count = 0
    random_guesser_results = defaultdict(lambda:0)
    probabilistic_guesser_results = defaultdict(lambda:0)

    while count < games_num:
        wordle_game = WordleGame("", DEFAULT_WORDS, DEFAULT_ATTEMPTS, False)

        guesser = WordleSearchProblem(wordle_game)
        guesses_1 = custom_depth_first_search(guesser, True)
        guesses_2 = custom_depth_first_search(guesser, False)

        random_guesser_results[wordle_game.run(guesses_1)] += 1
        probabilistic_guesser_results[wordle_game.run(guesses_2)] += 1

        count += 1

    print(f'Random Guesser Results: avg win = {avg_win(random_guesser_results)}')
    print(f'Probabilistic results: avg win = {avg_win(probabilistic_guesser_results)}')

    guesses_num=['1', '2', '3', '4', '5', '6', '6 <']

    fig = go.Figure(data=[
        go.Bar(name='Random Guesser (UCS)', x=guesses_num, y=bar_plot_input(random_guesser_results), opacity=0.7, marker= dict(color="#797c7e")),
        go.Bar(name='Probabilistic Guesser (A*)', x=guesses_num, y=bar_plot_input(probabilistic_guesser_results), opacity=0.7, marker= dict(color="#6AA964")),
    ], layout=go.Layout(
        title=go.layout.Title(text="UCS (Random Guesser) vs A* (Probabilistic Guesser) - 100 Games")
    ))

    fig.update_yaxes(title='Number of Games')
    fig.update_xaxes(title='Guesses used to win')
    fig.write_image("ucs_vs_A*_results.png")
    fig.show()

def bar_plot_input(results_dict):
    bar_vals = [0, 0, 0, 0, 0, 0, 0]

    for key, val in results_dict.items():
        bar_vals[key - 1] = val

    return bar_vals

def avg_win(results_dict):

    wins = 0
    for key, val in results_dict.items():
        if key != 7:
            wins += key * val

    return wins / (100 - results_dict[7])



if __name__ == '__main__':
    main()
