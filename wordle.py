#words from https://github.com/tabatkins/wordle-list
import random
from colorama import Fore, Back, Style
maxTries = 2
numBoards = 8
board = [[[] for x in range(maxTries+1)] for x in range(numBoards)]

def getRandWord():
    wordFile = open('words.txt', 'r')
    words = wordFile.read()
    words = words.split('\n')
    index = random.randrange(0, len(words))
    return words[index]


def eval(trueWord, guessWord, guessNum):
    for b in board:
        b[guessNum]=guessWord
        for guessWord in b:
            if guessWord:
                for i in range(5):
                    if guessWord[i] == trueWord[i]:
                        print(Back.GREEN + guessWord[i], end = '')
                    elif guessWord[i] in trueWord:
                        print(Back.YELLOW + guessWord[i], end = '')
                    else:
                        print(Back.WHITE+ guessWord[i], end = '')
                print(Style.RESET_ALL)
    for i in range(maxTries - guessNum):
        print(Back.WHITE+ '_____', end = '')    
        print(Style.RESET_ALL)
    if guessWord == trueWord:
        print("YOU WON!!!")
        return False
    if guessNum >= maxTries:
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
        for word in words:
            playing = eval(word, guess, guessNum)
        guessNum += 1

if __name__=="__main__": 
    play([getRandWord() for _ in range(numBoards)])