import heapq
import random
from collections import defaultdict

class GuessState:
    def __init__(self, word, guess_space, guess_num, feedback, cost=1):
        self.word = word
        self.guess_space = guess_space
        self.guess_num = guess_num
        self.feedback = feedback
        self.cost = cost

    def __str__(self):

        return f'Word: {self.word}, Guess Number: {self.guess_num}'

class WordleSearchProblem:

    def __init__(self, game):
        self.wordle_game = game
        self.words_space = game.wordle_space.copy()

    def get_start_state(self, words_space):
        start_state = GuessState("", list(self.wordle_game.wordle_space.copy()), 0, {0: set(), 1: set(), 2: set()}, 0)
        return start_state

    def is_goal_state(self, state):

        return self.wordle_game.verify_guess(state.word)

    def get_successors(self, state):
        successors = list()

        next_guess_space = state.guess_space.copy()
        cumulative_feedback = state.feedback.copy()

        if state.word != "":
            guess_feedback = self.get_state_feedback(state)

            self.update_guess_space(next_guess_space, cumulative_feedback, guess_feedback, state.word)

        for word in next_guess_space:
            new_guess_state = GuessState(word, next_guess_space, state.guess_num + 1, cumulative_feedback)
            successors.append(new_guess_state)

        return successors


    def get_state_feedback(self, state):
        feedback = self.wordle_game.get_guess_feedback(state.word)[0]

        return feedback

    def get_state_cost(self, state):
        return 1

    def update_guess_space(self, guess_space, all_feedback, guess_feedback, guess_word):

        ## Map each letter of the guess word to its numerical value obtained in the last reply
        guess_word_list = list(guess_word)
        assert len(guess_word_list) == len(guess_feedback), 'word length and marks must have the same length'
        ## Then append these letters to the entire history of guesses
        for mark, char in zip(guess_feedback, guess_word_list):
            all_feedback[mark].add(char)

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
        present_and_confirmed_letters = set.union(all_feedback[1], all_feedback[2])

        ## Adding letters from the latest guess to their categories
        for ii in range(0, len(guess_word_list)):
            if (guess_feedback[ii] == 0):
                if (guess_word_list[ii] in present_and_confirmed_letters):
                    false_duplicates.add((guess_word_list[ii], ii))
                else:
                    forbidden_letters.add((guess_word_list[ii], ii))
            elif (guess_feedback[ii] == 1):
                if (guess_word_list[ii] in all_feedback[2]):
                    false_duplicates.add((guess_word_list[ii], ii))
                else:
                    present_letters.add((guess_word_list[ii], ii))
            elif (guess_feedback[ii] == 2):
                confirmed_letters.add((guess_word_list[ii], ii))

        ## Step 2: Removing wrong guesses from the word list

        # Remove latest try from the list of words
        guess_space.remove(guess_word)

        ## Use hints to filter out the word list of wrong guesses
        size = len(guess_space)
        ii = 0
        while (ii < size):
            word = guess_space[ii]
            word_removed = False

            for confirmed_letter in confirmed_letters:
                if (word[confirmed_letter[1]] != confirmed_letter[0]):
                    guess_space.remove(word)
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
                    guess_space.remove(word)
                    word_removed = True
                    ii -= 1
                    size -= 1
                    break

            if (word_removed == True):
                ii += 1
                continue

            for forbidden_letter in forbidden_letters:
                if (forbidden_letter[0] in word):
                    guess_space.remove(word)
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
                    guess_space.remove(word)
                    word_removed = True
                    ## Adjust indexing of the list after removing element
                    ii -= 1
                    size -= 1
                    break

            ii += 1

def uniformCostSearch(game):
    """Search the node of least total cost first."""
    ## Set up the frontier as a queue with the initial state
    start_node = Node(game.get_start_state(game.words_space), [], 0)
    frontier = PriorityQueue()
    frontier.push(start_node, start_node.priority)
    explored_states = []

    while (not frontier.isEmpty()):
        current_node = frontier.pop()
        explored_states.append(current_node.state)

        if game.is_goal_state(current_node.state):
            return current_node.path
        else:
            successors = game.get_successors(current_node.state)
            for successor in successors:
                updated_path = current_node.path.copy()
                updated_path.append(successor.word)
                successor_node = Node(successor, updated_path, current_node.priority + 1)

                if successor_node.state not in explored_states:
                    current_state_in_frontier = False
                    for node in frontier.heap:
                        if (successor_node.state == node[2].state):
                            current_state_in_frontier = True

                    if (not current_state_in_frontier):
                        frontier.push(successor_node, successor_node.priority)
                    else:
                        frontier.update(successor_node, successor_node.priority)

    raise ValueError('Path to the goal state could not be found')

def probability_heuristic(state):

    letters_freqs, transitions_freqs = letter_transition_probs(state.guess_space)

    successors_costs = get_successors_cost(letter_freqs, transitions_freqs, state.guess_space)

    return 1 - successors_costs[state.words]

def aStarSearch(game, heuristic=probability_heuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    start_node = Node(game.get_start_state(game.words_space), [], 0)
    frontier = util.PriorityQueue()
    frontier.push(start_node, start_node.priority)
    explored_states = []

    while (not frontier.isEmpty()):
        current_node = frontier.pop()
        explored_states.append(current_node.state)

        if problem.isGoalState(current_node.state):
            return current_node.path
        else:
            ## Expand current node
            successors = game.get_successors(current_node.state)
            for successor in successors:
                updated_path = current_node.path.copy()
                updated_path.append(successor.word)
                successor_node = Node(successor, updated_path, current_node.priority + 1)

                if successor_node.state not in explored_states:
                    current_state_in_frontier = False
                    for node in frontier.heap:
                        if (successor_node.state == node[2].state):
                            current_state_in_frontier = True

                    if (not current_state_in_frontier):
                        frontier.push(successor_node, successor_node.priority + heuristic(successor_node.state))
                    else:
                        frontier.update(successor_node, successor_node.priority + + heuristic(successor_node.state))

    raise ValueError('Path to the goal state could not be found')

def letter_transition_probs(words_space):
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

def get_successors_cost(letters_freqs, transitions_freqs, words_space):
    successors_costs = dict()

    repeated_letters_prob = duplicate_letter_probability(words_space)

    repeated_transitions_prob = duplicate_transition_probability(words_space)

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

        successors_costs[word] = word_prob

    return successors_costs

def duplicate_transition_probability(words_space):

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

def duplicate_letter_probability(words_space):

    letters_space_size = len(words_space) * 5
    repeated_letters_count = 0

    for word in words_space:
        seen_letters = list()
        for ii in range(0, 5):
            if word.count(word[ii]) > 1 and word[ii] not in seen_letters:
                repeated_letters_count += word.count(word[ii]) - 1
                seen_letters.append(word[ii])

    repeated_letters_prob = repeated_letters_count / letters_space_size

    return repeated_letters_prob

def custom_depth_first_search(game, random):
    start_state = game.get_start_state(game.words_space)

    next_state = start_state

    guess_path = list()

    while game.is_goal_state(next_state) != True:
        successors = game.get_successors(next_state)

        next_guess_space = successors[0].guess_space.copy()
        letters_freqs, transitions_freqs = letter_transition_probs(next_guess_space)

        successors_costs = get_successors_cost(letters_freqs, transitions_freqs, next_guess_space)

        best_guess = get_best_guess(successors_costs, random)
        guess_path.append(best_guess)
        for successor in successors:
            if successor.word == best_guess:
                next_state = successor
                break

    return guess_path

def get_best_guess(guesses_costs, randomize):
    if randomize:
        rand_idx = random.randint(0, len(guesses_costs.keys()) - 1)
        words = list(guesses_costs.keys())
        return words[rand_idx]
    else:
        best_guess = (None, 0)
        for word, prob in guesses_costs.items():
            if prob > best_guess[1]:
                best_guess = (word, prob)

        return best_guess[0]

class Node:
    def __init__(self, state, path=[], priority=0):
        self.state = state
        self.path = path
        self.priority = priority

    def update_path(self, new_path):
        self.path = new_path

    def update_priority(self, new_priority):
        self.priority = new_priority

    def __eq__(self, obj):
        return isinstance(obj, Node) and (self.state == obj.state)

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)
