from agent import DFS, BFS, AStar, Dijkstra, GBFS
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
    #initial = [[1, 2, 3, 4], [5, 6, 7, 8], [-1, 10, 11, 12], [9, 13, 14, 15]]
    #initial = [[1, 2, 3, 4], [5, -1, 7, 8], [9, 6, 10, 11], [13, 14, 15, 12]]
    goal = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, -1]]
    puzzle = PuzzleEnv(None, goal, 4, 4)
    root = Node(puzzle, None)
    # Gera Aleatoriamente o estado inicial
    puzzle.generate_initial_state()
    agentBFS = BFS(2000)
    agentDFS = DFS(2000)
    agentDijkstra = Dijkstra(10000)
    agentGBFS = GBFS(10000)
    agentAStar = AStar(10000)
    print("Estado Inicial: ")
    print(puzzle)

    #agentBFS.search(deepcopy(root))
    #print(agentBFS)
    #agentDFS.search(deepcopy(root))
    #print(agentDFS)
    agentDijkstra.search(deepcopy(root))
    print(agentDijkstra)
    agentGBFS.search(deepcopy(root))
    print(agentGBFS)
    agentAStar.search(deepcopy(root))
    print(agentAStar)

# puzzleUI = PuzzleUI(600, 600, 4, 4, puzzle, agent)
# puzzleUI.show()
