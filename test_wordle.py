# assert that the algorithm is working

import unittest
# import wordle
from board import Board


class MTCSTestCase(unittest.TestCase):
    def test_initialization(self):
        board_game = Board('word')
        self.assertIsInstance(board_game, Board)


if __name__ == '__main__':
    unittest.main()
