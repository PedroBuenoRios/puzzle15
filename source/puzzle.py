from enviroment import ABCEnviroment
import random
import time
from enum import Flag, auto
import numpy as np

class Actions(Flag):
    ESQUERDA = auto()
    DIREITA = auto()
    CIMA =  auto()
    BAIXO = auto()

class PuzzleEnv(ABCEnviroment):
    def __init__(self, initial_state, goal_state, colls = 4, rows = 4):
        self.rows = rows
        self.colls = colls
        self.initial_state = initial_state
        self.state = [row.copy() for row in initial_state]
        self.goal_state = goal_state
        self.action_taked = None
        self.parent = None
        self.distance = 0
        self.opened = True

    def __str__(self):
        str = ""
        for i in range(self.rows):
            str += f"{self.state[i]}\n"
        return str

    def generate_initial_state(self):
        ''' 
        Gera um estado inicial aleatório
        '''
        rows, colls = self.rows, self.colls
        self.initial_state = list(range(1, colls*rows))
        self.initial_state.append(-1)
        random.seed(time.time())
        random.shuffle(self.initial_state)
        stride = 0
        state = []

        for i in range(colls):
            step = colls*(i+1)
            row = self.initial_state[stride:step]
            stride = step
            state.append(row)

        self.initial_state = state
        self.state = [row.copy() for row in state]
        self.empty_row, self.empty_coll = self.get_indices()

    def is_goal_state(self):
        '''
        Retorna 1 se está no estado final e 0 se não está
        '''
        for row_idx, row in enumerate(self.goal_state):
            for coll_idx, value in enumerate(row):
                if self.state[row_idx][coll_idx] != self.goal_state[row_idx][coll_idx]:
                    return 0
        return 1

    def get_possible_actions(self):
        '''
        Retorna as possíveis as ações em forma de flags da classe Actions.\n
        Podem usar operadores bitwise | (OR), & (AND), ^ (XOR), ~ (NOT)
        '''
        row_index, coll_index = self.get_indices()
        actions = Actions.ESQUERDA | Actions.DIREITA | Actions.CIMA | Actions.BAIXO
        if row_index == 0:
            actions = actions & ~Actions.CIMA
        if row_index == self.rows-1:
            actions = actions & ~Actions.BAIXO
        if coll_index == 0:
            actions =  actions & ~Actions.ESQUERDA
        if coll_index == self.colls-1:
            actions = actions & ~Actions.DIREITA
        return actions

    def generate_possible_states(self):
        '''
         Retorna os possíveis estados futuros
        '''
        possible_actions = self.get_possible_actions()
        possible_states = []

        for action in possible_actions:
            state = self.take_action(action)
            possible_states.append(state)
        
        self.possible_actions = possible_actions
        self.possible_states = possible_states

    def take_action(self, action):
        '''
            Retorna um estado no qual a ação foi tomada
        '''
        row, coll = self.get_indices()
        new_state = [row.copy() for row in self.state]
        if action == Actions.DIREITA:
            temp = new_state[row][coll+1]
            new_state[row][coll+1] = new_state[row][coll]
            new_state[row][coll] = temp 
        elif action == Actions.BAIXO:
            temp = new_state[row+1][coll]
            new_state[row+1][coll] = new_state[row][coll]
            new_state[row][coll] = temp
        elif action == Actions.ESQUERDA:
            temp = new_state[row][coll-1]
            new_state[row][coll-1] = new_state[row][coll]
            new_state[row][coll] = temp
        elif action == Actions.CIMA:
            temp = new_state[row-1][coll]
            new_state[row-1][coll] = new_state[row][coll]
            new_state[row][coll] = temp
        return [row.copy() for row in new_state]
        
    def get_indices(self):
        '''
        Retorna a linha e coluna onde está o quadrado vazio
        '''
        for rowIdx, row in enumerate(self.state):
            for collIdx, value in enumerate(row):
                if value == -1:
                    return rowIdx, collIdx
    
    def print_possible_states(self):
        print(self.possible_actions)
        for i in range(5):
            for stateIdx, env in enumerate(self.possible_states):
                if i == 0:
                    print(f"Estado: {stateIdx+1}\t\t", end="")
                else:
                    print(f"{env.state[i-1]}\t\t", end="")
            print()

    def __eq__(self, env):
        '''
        Retorna 1 se os estados dos nós são iguais e 0 se são diferentes
        '''
        for row_idx, row in enumerate(self.state):
            for coll_idx, value in enumerate(row):
                if self.state[row_idx][coll_idx] != env.state[row_idx][coll_idx]:
                    return False
        return True

    def calculate_distance_to(self, goal):
        goal_flat_mtx = np.asarray(goal).flatten().tolist()
        state_flat_mtx = np.asarray(self.state).flatten().tolist()

        sum = 0
        for idx_child, value in enumerate(state_flat_mtx):
            idx_goal = goal_flat_mtx.index(value)
            r1 = int(idx_child) / int(self.rows)
            c1 = int(idx_child) % int(self.colls)
            r2 = int(idx_goal) / int(self.rows)
            c2 = int(idx_goal) % int(self.colls)
            d = abs(r1 - r2) + abs(c1 - c2)
            sum += d
        return sum