# words from https://github.com/tabatkins/wordle-list
# file for game logic

import random
from colorama import Fore, Back, Style
from mcts import MCTS
from board import MAX_TRIES, NUM_BOARDS, evalNoPrint, Board


class Wordle:
    game = []
    wordFile = open('words.txt', 'r')
    validWords = wordFile.read()
    validWords = validWords.split('\n')\

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

    # By cole, I accidentally removed it and a git conflict prevented me from restoring it properly.
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

    # play with the MCTS file
    def playWithMcts(words):
        print(words)
        guess_num = 0
        playing = True
        # Initialize the MCTS with one of the boards
        mcts = MCTS(Board(words[0]), validWords)  # Pass the board and the validWords to MCTS

        while playing:
            mcts.search(time_limit=1)  # Let MCTS search for the best move
            # Get the best child from MCTS, and determine the best guess
            best_node = mcts.root.best_child()  # Get the best child node
            best_guess = best_node.board.word  # Assuming this is how you want to determine the best guess
            for board in game:
                board.board[guess_num] = best_guess
                playing = sum(eval(board, best_guess, guess_num)) < 10

            guess_num += 1
            if guess_num >= MAX_TRIES:
                print("Out of time")
                break


    # goes through every valid move and gets the one with the highest value
    def findBestMove(validMoves):
        bestMoveValue = -100
        bestMove = ""

        for move in validMoves:
            if evalNoPrint(move) > bestMoveValue:
                bestMoveValue = evalNoPrint
                bestMove = move

        return move

if __name__=="__main__":
    words = [getRandWord() for _ in range(NUM_BOARDS)]
    for word in words:
        game.append(Board(word))
    playWithMcts(words) # Change based on version you want to run
