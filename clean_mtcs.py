
import math
import random
import time
from collections import Counter

from colorama import Back, Style

#from board import MAX_TRIES
#from wordle import getValidMoves
#from wordle import getValidMoves, validWords
# file structure generated by chat GPT, implemented by the team
# Resources: https://ai-boson.github.io/mcts/

MAX_TRIES = 6
NUM_BOARDS = 8

def getRandWord():
    index = random.randrange(0, len(validWords))
    return validWords[index]

def evaluate(word1, word2):
  #if the guess letter is in the right spot add 2 to score, if its just in the word add 1 to score
  score = 0 
  for i in range(5):
      if word1[i] == word2[i]:
          score += 2
      elif word1[i] in word2:
          score += 1
  #print(word1, "+", word2, '=', score)
  return score #If you evaluate team and meet it returns 7 instead of 6

def get_valid_moves(valid_word_list, guess, correct_word):
    validMoves = []
    invalidMoves = []
    greys, greens, yellows = get_bad_letters(guess, correct_word)
    for word in valid_word_list: #look through all words
        
        goodWord = True
        if word == guess:
           goodWord = False
        if greens:
           for letter in greens:
              if word[letter[1]] != letter[0]:
                 goodWord = False
        if greys:
          for letter in greys:
              if letter in word:
                goodWord = False
        if yellows:
           for letter in yellows:
              if word[letter[1]] == letter[0]:
                 goodWord = False
        
        if goodWord:
          validMoves.append(Node(word))
        # if 0 in score_word(word, correct_word):
        #    invalidMoves.append(word)
        # else:
        #   validMoves.append(Node(word))
    #print(len(validMoves))

    return validMoves

#This class is the game
class Board:
  def __init__(self, valid_words):
    self.valid_words = [Node(valid_word) for valid_word in valid_words]
    self.correct_word = getRandWord()
    self.solved = False
    self.board = [[] for x in range(MAX_TRIES+1)] #This is the wordle boards
    self.guesses = []
    self.current_guess = Node("adieu")
    self.guess_number = 0
    self.play(self.current_guess.word) #We start with adieu every time so we automatically play it when the board is created
  
  def play(self, word_played):
    if not self.solved:
      if word_played in validWords:
        self.board[self.guess_number] = word_played
        #Change valid word list to shorten runtime
        self.valid_words = get_valid_moves(node_to_string(self.valid_words), word_played, self.correct_word)
        evaluate(word_played, self.correct_word)
        #if (sum(evaluate(word_played, self.correct_word)) < 10):
        #self.solved = True
        self.guesses.append(word_played)
        self.guess_number += 1


def get_bad_letters(guess, correct):
  bad_letters = []
  greens = []
  yellows = []
  # count_correct = Counter(correct)
  # count_guess = Counter(guess)
  for i in range(5):

          if guess[i] not in correct:
             bad_letters.append(guess[i])
          elif guess[i] == correct[i]:
             greens.append((guess[i], i))
          elif guess[i] in correct:
             yellows.append((guess[i], i))
  return bad_letters, greens, yellows


def node_to_string(node_list):
  string_list = []
  for x in node_list:
    string_list.append(x.word)
  return string_list 


class Node:
  def __init__(self, word, parent = None):
    self.word = word
    self.parent = parent
    self.children = []
    self.visits = 0
    self.value = 0

  def best_child(self):
    """Return the child with the best UCT value."""
    return max(self.children, key=lambda child: child.uct_value(self.visits))

  def uct_value(self, total_visits): #Total visits will always be self.visits (Idk if it is correct)
      """Calculate the UCT value for this node."""
      """Adapted from: https://ai-boson.github.io/mcts/"""
      if self.visits == 0:
          return float('inf')  # Ensure unvisited nodes are prioritized
      return self.value / self.visits + 1.41 * (math.sqrt(math.log(total_visits) / self.visits))


class MCTS:
    def __init__(self, initial_board):
      self.board = initial_board
      self.root = self.board.current_guess
      self.root.children = get_valid_moves(node_to_string(self.board.valid_words), self.root.word, self.board.correct_word)

    def select(self, node):
        """Select a node to explore based on UCT."""
        while node.children:
            node = node.best_child()  # Traverse to the best child
        return node

    def expansion(self, node : Node):
      """The goal of evaluate is to find the most promising child node and simulating a game based on that node"""
      #Finds the most promising child node and indicates it has been visited
      top_score = 0
      best_child = None
      i = 0
      for child in self.root.children:
          i+=1
          #print(i, "/", len(self.root.children))
          score = 0
          child.children = get_valid_moves(node_to_string(self.root.children), self.board.guesses[self.board.guess_number - 1], self.board.correct_word)
          for subchild in child.children:
            score += evaluate(child.word, subchild.word)
          if score > top_score:
            top_score = score
            best_child = child
      return best_child.word
      # for i in self.root.children:
      #   #best_child = self.select(node)
      #   best_child = i
      #   best_child.visits += 1
      #   #Finds all valid moves of the child node and that list becomes the node's children
      #   best_child.children = get_valid_moves(node_to_string(self.root.children), self.board.guesses[0], self.board.correct_word)
      #   #Simulates a random game if the child node was the move selected
      #   self.simulate(best_child) #NOT DONE
    
    def simulate(self, node):
        """Simulate a random game from the current node."""
        #This is where we want to test the node based on all the other valid children 
        for child1 in node.children:
          for child2 in node.children:
            node.value += evaluate(child1.word, child2.word)

    def search(self, time_limit, start_time, current_node):
        """Conduct MCTS for a specified time limit."""
        # if we are starting here make sure current_node is set to the root
        # do we need to do this or..... ??!?!?!?!?
        if not current_node:
            current_node = self.root

        #actually searching
        best_eval: float = float("-inf")  # arbitrarily low starting point
        for move in getValidMoves(self.valid_words):
            # Update time
            current_time = time.time() - start_time
            print(current_time)

            # Check time
            if current_time > time_limit:
                return best_eval

            # Sim
            self.simulate(Node(current_node.board, current_node))
            best_eval = max(best_eval, self.backpropagate(current_node, "???REWARD????"))

        return best_eval

def eval(board, guessNum):
        for pastGuessWord in board.board:
            real_count = Counter(pastGuessWord)
            guessCount = {}

            if pastGuessWord:
                for i in range(5):
                    if i in guessCount:
                      guessCount[i]  += 1
                    else:
                      guessCount[i]  = 1

                    if pastGuessWord[i] == board.correct_word[i]:
                        print(Back.GREEN + pastGuessWord[i], end = '')
                    elif pastGuessWord[i] in board.correct_word:
                      
                        if guessCount[i] < real_count[i]:
                          print(Back.YELLOW + pastGuessWord[i], end = '')
                        else:
                          print(Back.WHITE+ pastGuessWord[i], end = '')
                    else:
                        print(Back.WHITE+ pastGuessWord[i], end = '')
                print(Style.RESET_ALL)
        for i in range(MAX_TRIES - guessNum):
            print(Back.WHITE+ '_____', end = '')
            print(Style.RESET_ALL)


# TESTING

if __name__ == "__main__":
    game = []
    wordFile = open('words.txt', 'r')
    validWords = wordFile.read()
    validWords = validWords.split('\n')
    wordle_board = Board(validWords)
    
    monte_carlo = MCTS(wordle_board)
    best = monte_carlo.expansion(monte_carlo.root)
    while best != wordle_board.correct_word:
        wordle_board.play(best)
        eval(wordle_board, wordle_board.guess_number)
        monte_carlo = MCTS(wordle_board)
        best = monte_carlo.expansion(monte_carlo.root)
        print(best, wordle_board.correct_word)
    wordle_board.play(best)
    eval(wordle_board, wordle_board.guess_number)
    print(monte_carlo.root.best_child().word)
