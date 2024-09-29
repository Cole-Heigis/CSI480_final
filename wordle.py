#words from https://github.com/tabatkins/wordle-list
import random
from colorama import Fore, Back, Style
MAX_TRIES = 4
NUM_BOARDS = 3
game = []
wordFile = open('words.txt', 'r')
validWords = wordFile.read()
validWords = validWords.split('\n')\
    
class Board:
    def __init__(self, word):
        self.word = word
        self.solved = False
        self.board = [[] for x in range(MAX_TRIES+1)]

def getRandWord():
    index = random.randrange(0, len(validWords))
    return validWords[index]


def eval(board, guessWord, guessNum):
    for pastGuessWord in board.board:
        if pastGuessWord:
            for i in range(5):
                if pastGuessWord[i] == board.word[i]:
                    print(Back.GREEN + pastGuessWord[i], end = '')
                elif pastGuessWord[i] in board.word:
                    print(Back.YELLOW + pastGuessWord[i], end = '')
                else:
                    print(Back.WHITE+ pastGuessWord[i], end = '')
            print(Style.RESET_ALL)
    for i in range(MAX_TRIES - guessNum):
        print(Back.WHITE+ '_____', end = '')    
        print(Style.RESET_ALL)
        
    if guessWord == board.word:
        board.solved = True
        print("YOU WON!!!")
        for board in game:
            if not board.solved:
                return True
        return False
    if guessNum >= MAX_TRIES:
        print("Out of time")
        return False
    print('\n')
    return True


def play(words):
    print(words)
    playing = True
    guessNum = 0
    won = 0
    while playing:
        guess = input()
        if guess in validWords:
            for board in game:
                board.board[guessNum]=guess
                playing = eval(board, guess, guessNum)
            guessNum += 1

if __name__=="__main__": 
    words = [getRandWord() for _ in range(NUM_BOARDS)]
    for word in words:
        game.append(Board(word))
    play(words)