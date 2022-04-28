#!/usr/bin/env python3

from smart_wordle_solver import SmartWordlePlayer
from smart_wordle_solver import SmartWordlePlayer2
from wordle_solver import BasicWordlePlayer
from wordle import WordleGame
from collections import defaultdict
import plotly.graph_objects as go

DEFAULT_WORDS = './all_words.txt'
DEFAULT_ATTEMPTS = 6
DEFAULT_PLAYER = 'interactive'
GREEN_TILE = '🟩'
YELLOW_TILE = '🟨'
WHITE_TILE = '⬜'

def main():

    games_num = 100
    count = 0
    basic_game_results = defaultdict(lambda:0)
    smart_game_results = defaultdict(lambda:0)
    old_smart_game_results = defaultdict(lambda:0)

    while count < games_num:
        wordle_game_1 = WordleGame("", DEFAULT_WORDS, DEFAULT_ATTEMPTS)
        wordle_game_2 = WordleGame(wordle_game_1.wordle, DEFAULT_WORDS, DEFAULT_ATTEMPTS)
        wordle_game_3 = WordleGame(wordle_game_1.wordle, DEFAULT_WORDS, DEFAULT_ATTEMPTS)

        player_1 = BasicWordlePlayer(wordle_game_1.wordle_space.copy())
        player_2 = SmartWordlePlayer(wordle_game_2.wordle_space.copy())
        player_3 = SmartWordlePlayer2(wordle_game_3.wordle_space.copy())

        wordle_game_1.player = player_1
        wordle_game_2.player = player_2
        wordle_game_3.player = player_3

        print('Player 1: Basic')
        game_1_result = wordle_game_1.run()
        basic_game_results[game_1_result] += 1

        print('\n')

        print('Player 2: New Smart')
        game_2_result = wordle_game_2.run()
        smart_game_results[game_2_result] += 1

        print('\n')

        print('Player 3: Old Smart')
        game_3_result = wordle_game_3.run()
        old_smart_game_results[game_3_result] += 1

        count += 1




    print(f'Basic Player results: {basic_game_results}')
    print(f'Smart Game results: {smart_game_results}')
    #print(f'Old Smart Game results: {old_smart_game_results}')
    print(f'Basic won: {games_num - basic_game_results[7]}, avg = {avg_win(basic_game_results)}\nOld Smart won: {games_num - old_smart_game_results[7]}, avg = {avg_win(old_smart_game_results)}\nNew Smart won: {games_num - smart_game_results[7]}, avg = {avg_win(smart_game_results)}')

    guesses_num=['1', '2', '3', '4', '5', '6', '6 <']

    fig = go.Figure(data=[
        go.Bar(name='Random Guesser (UCS)', x=guesses_num, y=bar_plot_input(basic_game_results), opacity=0.7, marker= dict(color="#797c7e")),
        go.Bar(name='Probabilistic Guesser (A*)', x=guesses_num, y=bar_plot_input(smart_game_results), opacity=0.7, marker= dict(color="#6AA964")),
        #go.Scatter(name='UCS avg guess', x=animals, y=[4.75, 4.75, 4.75, 4.75, 4.75, 4.75, 4.75, 4.75], mode="lines", marker= dict(color="#797c7e")),
        #go.Scatter(name='A* avg guess', x=animals, y=[4.375, 4.375, 4.375, 4.375, 4.375, 4.375, 4.375], mode="lines", marker= dict(color="#6AA964"))
    ], layout=go.Layout(
        title=go.layout.Title(text="UCS vs A* probability heuristic - 100 Games")
    ))
    # Change the bar mode
    #fig.update_layout(barmode='group')
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
