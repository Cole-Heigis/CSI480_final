#words from https://github.com/tabatkins/wordle-list
import random
from colorama import Fore, Back, Style
MAX_TRIES = 2
NUM_BOARDS = 8
game = []

class Board:
    def __init__(self, word):
        self.word = word
        self.solved = False
        self.board = [[] for x in range(MAX_TRIES+1)]

def getRandWord():
    wordFile = open('words.txt', 'r')
    words = wordFile.read()
    words = words.split('\n')
    index = random.randrange(0, len(words))
    return words[index]


def eval(trueWord, guessWord, guessNum):
    for board in game:
        board.board[guessNum]=guessWord
        for guessWord in board.board:
            if guessWord:
                for i in range(5):
                    if guessWord[i] == trueWord[i]:
                        print(Back.GREEN + guessWord[i], end = '')
                    elif guessWord[i] in trueWord:
                        print(Back.YELLOW + guessWord[i], end = '')
                    else:
                        print(Back.WHITE+ guessWord[i], end = '')
                print(Style.RESET_ALL)
    for i in range(MAX_TRIES - guessNum):
        print(Back.WHITE+ '_____', end = '')    
        print(Style.RESET_ALL)
    if guessWord == trueWord:
        print("YOU WON!!!")
        return False
    if guessNum >= MAX_TRIES:
        print("Out of time")
        return False
    return True


def play(words):
    print(words)
    playing = True
    guessNum = 0
    won = 0
    while playing:
        guess = input()
        for board in game:
            playing = eval(board.word, guess, guessNum)
        guessNum += 1

if __name__=="__main__": 
    words = [getRandWord() for _ in range(NUM_BOARDS)]
    for word in words:
        game.append(Board(word))
    play(words)