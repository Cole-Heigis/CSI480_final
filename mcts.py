import math
import time


# file structure generated by chat GPT, implemented by the team
# Resources: https://ai-boson.github.io/mcts/


class Node:
    def __init__(self, board, parent=None):
        self.board = board          # The state of the board
        self.parent = parent        # Reference to the parent node
        self.children = []          # List of child nodes
        self.visits = 0             # Count of how many times this node has been visited
        self.wins = 0               # Total wins for this node

    def best_child(self):
        """Return the child with the best UCT value."""
        return max(self.children, key=lambda child: child.utc_value(self.visits))

    def uct_value(self, total_visits):
        """Calculate the UCT value for this node."""
        """Adapted from: https://ai-boson.github.io/mcts/"""
        if self.visits == 0:
            return float('inf')  # Ensure unvisited nodes are prioritized
        return self.wins / self.visits + 1.41 * (math.sqrt(math.log(total_visits) / self.visits))


class MCTS:
    def __init__(self, initial_board, valid_words):
        self.root = Node(initial_board)  # Create the root node with the initial board
        self.valid_words = valid_words  # List of valid words

    def search(self, time_limit, start_time):
        """Conduct MCTS for a specified time limit."""

        #update time
        current_time = time.time() - start
        print(current_time)
        current_time = time.time() - start_time

        # base case
        if self.root.wins == 8 or current_time >= time_limit:
            return self.root.evaluate(self.root)
        
        #actually searching 
        
        


    def select(self, node):
        """Select a node to explore based on UCT."""
        while node.children:
            node = node.best_child()  # Traverse to the best child
        return node

    def simulate(self, node):
        """Simulate a random game from the current node."""


    def backpropagate(self, node, reward):
        """Backpropagate the result of the simulation to update the node values."""



# TESTING 

def test_timer():
    print("start")
    tree = MCTS("s0", "sdsd")
    tree.search(5)
    print("end")


if __name__ == "__main__":
    
    # testing timer
    test_timer()




