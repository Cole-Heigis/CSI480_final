# assert that the algorithm is working

import unittest
import time
# import wordle
from clean_mtcs import Board, MCTS, score_word

# print(score_word("adieu", "adieu"))
game = []
wordFile = open('words.txt', 'r')
valid_words = wordFile.read().splitlines()
wordFile.close()


class MTCSTestCase(unittest.TestCase):
    def test_initialization(self):
        board_game = Board(valid_words)
        self.assertIsInstance(board_game, Board)

    def test_game(self):
        board_game = Board(valid_words)
        monte_carlo = MCTS(board_game)
        monte_carlo.expansion(monte_carlo.root)
        print(monte_carlo.root.best_child().word)
        self.assertIs(board_game.correct_word, monte_carlo.root.best_child().word)

    def test_time(self):
        self.start_time = time.time()
        board_game = Board(valid_words)
        monte_carlo = MCTS(board_game)
        monte_carlo.expansion(monte_carlo.root)
        print(monte_carlo.root.best_child().word)
        elapsed_time = time.time() - self.start_time
        print(f"{self._testMethodName} took {elapsed_time:.4f} seconds to complete")

    def test_path(self):
        pass


if __name__ == '__main__':
    unittest.main()
