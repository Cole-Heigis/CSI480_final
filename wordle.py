#words from https://github.com/tabatkins/wordle-list
import random
from colorama import Fore, Back, Style
MAX_TRIES = 4
NUM_BOARDS = 8
game = []
wordFile = open('words.txt', 'r')
validWords = wordFile.read()
validWords = validWords.split('\n')\

# random comment for test
    
class Board:
    def __init__(self, word):
        self.word = word
        self.solved = False
        self.board = [[] for x in range(MAX_TRIES+1)]

def getRandWord():
    index = random.randrange(0, len(validWords))
    return validWords[index]

def getValidMoves(words, guess):

    validMoves = [] 
    invalidMoves = []
    for word in validWords: #look through all words
        for letter in guess: #look through letters in the guess array
            if letter == 0 and str(letter) in word: #if the letter isn't green or yellow and is in a word then its an invalid word
                invalidMoves.append(word)
                break
        validMoves.append(word)
    return validMoves


def eval(board, guessWord, guessNum):
    returnValues = [0, 0, 0, 0, 0]
    for pastGuessWord in board.board:
        if pastGuessWord:
            for i in range(5):
                if pastGuessWord[i] == board.word[i]:
                    print(Back.GREEN + pastGuessWord[i], end = '')
                    returnValues[i] = 2
                elif pastGuessWord[i] in board.word:
                    print(Back.YELLOW + pastGuessWord[i], end = '')
                    returnValues[i] = 1
                else:
                    print(Back.WHITE+ pastGuessWord[i], end = '')
                    returnValues[i] = 0
            print(Style.RESET_ALL)
    for i in range(MAX_TRIES - guessNum):
        print(Back.WHITE+ '_____', end = '')    
        print(Style.RESET_ALL)

    if guessWord == board.word:
        board.solved = True
        print("YOU WON!!!")
        for board in game:
            if not board.solved:
                return returnValues
        return returnValues
    if guessNum >= MAX_TRIES:
        print("Out of time")
        return returnValues
    print('\n')
    for x in getValidMoves(board.word, returnValues):
        print(x)
    
    return returnValues


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
                playing = (sum(eval(board, guess, guessNum)) < 10)
            guessNum += 1

if __name__=="__main__": 
    words = [getRandWord() for _ in range(NUM_BOARDS)]
    for word in words:
        game.append(Board(word))
    play(words)
