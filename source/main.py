from agent import DFS, BFS, Dijkstra
from puzzle import PuzzleEnv
from graph import Node
from copy import deepcopy

"""
[   [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, -1] ]

[   [1, 2, 3, 4],
    [5, 6, 7, 8],
    [-1, 10, 11, 12],
    [9, 13, 14, 15] ]

[   [1, 2, 3],
    [4, 5, 6],
    [7, 8, -1]]

[ [-1, 2, 3],
    [1, 5, 6],
    [4, 7, 8]]

"""


if __name__ == "__main__":
    initial = [[1, 2, 3, 4], [5, 6, 7, 8], [-1, 10, 11, 12], [9, 13, 14, 15]]
    goal = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, -1]]
    puzzle = PuzzleEnv(initial, goal, 4, 4)
    root = Node(puzzle, None)
    # Gera Aleatoriamente o estado inicial
    puzzle.generate_initial_state()
    agentBFS = BFS(2000)
    agentDFS = DFS(2000)
    dijkstra = Dijkstra(0)
    print("Estado Inicial: ")
    print(puzzle)

    agentBFS.search(deepcopy(root))
    print(agentBFS)
    agentDFS.search(deepcopy(root))
    print(agentDFS)
    dijkstra.search(deepcopy(root))
    print(dijkstra)

# puzzleUI = PuzzleUI(600, 600, 4, 4, puzzle, agent)
# puzzleUI.show()
