# board file to keep track of the board and supporting functions


MAX_TRIES = 4
NUM_BOARDS = 8

#creted by cole, moved to seprate file to avoid circular imports
class Board:
    def __init__(self, word):
        self.word = word
        self.solved = False
        self.board = [[] for x in range(MAX_TRIES+1)]
        self.visits = 0


# its the eval function but it does no print anything (for ai mostly)
# Written by John
def evalNoPrint(guessWord, board):
    score = 0

    # if the guess letter is in the right spot add 2, if its just in the word add 1
    for i in range(5):
        if guessWord[i] == board.word[i]:
            score += 2
        elif guessWord[i] in board.word:
            score += 1

    # if the word is completly wrong make it a negative number
    if score == 0:
        return -1

    return score

# Written by cole, moved here for file structure clarity
def eval(board, guessWord, guessNum):
    returnValues = [0, 0, 0, 0, 0]
    for pastGuessWord in board.board:
        if pastGuessWord:
            for i in range(5):
                if pastGuessWord[i] == board.word[i]:
                    print(Back.GREEN + pastGuessWord[i], end='')
                    returnValues[i] = 2
                elif pastGuessWord[i] in board.word:
                    print(Back.YELLOW + pastGuessWord[i], end='')
                    returnValues[i] = 1
                else:
                    print(Back.WHITE + pastGuessWord[i], end='')
                    returnValues[i] = 0
            print(Style.RESET_ALL)
    for i in range(MAX_TRIES - guessNum):
        print(Back.WHITE + '_____', end='')
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
