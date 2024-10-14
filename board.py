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

