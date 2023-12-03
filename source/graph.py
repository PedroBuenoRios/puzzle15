from dataclasses import dataclass, field 
from puzzle import PuzzleEnv
from typing import Any

@dataclass(order=True)
class PrioritizedNode:
    priority: float
    item: Any = field(compare=False)

class Node:
    def __init__(self, env, parent):
        self.children = []
        self.distance_from_parent = 1
        self.env = env
        self.total_nodes = 0
        self.parent = parent
        self.distance_from_root = 0
        self.opened = True
        self.predecessor = None

    def is_goal(self):
        return self.env.is_goal_state()

    def generate_children(self, callback = None):
        '''
         Retorna os possíveis estados futuros
        '''
        env = self.env

        env.generate_possible_states()

        for action, state in zip(env.possible_actions, env.possible_states):
            newEnv = PuzzleEnv(state, env.goal_state, env.colls, env.rows)
            newEnv.action_taked = action
            newNode = Node(newEnv, self)
            self.children.append(newNode)

        self.calculate_distances_to_children()
        if callback is not None:
            callback(self)

    def calculate_distances_to_children(self):
        for child in self.children:
            child.distance_from_parent = child.env.calculate_distance_to(self.env.goal_state)
           
    def generate_levels(self, num_levels, callback = None):
        if num_levels == 0 or num_levels == 240:
            return
        self.generate_children(callback)
        for child in self.children:
            child.generate_levels(num_levels-1, callback)

    def count_total_nodes(self):
        try:
            self.total_nodes = len(self.children)
            for child in self.children:
                self.total_nodes += child.count_total_nodes()
            return self.total_nodes
        except RecursionError:
            print("Limite de chamadas recursivas atingidas ao contar os número total de nós")
            return 0

class Tree():
    def __init__(self, maxNodes, root: Node):
        self.root = root
        self.maxNodes = maxNodes
        self.total_nodes = 1
        