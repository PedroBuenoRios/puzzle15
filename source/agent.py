from queue import PriorityQueue

from graph import Node, PrioritizedNode

class Agent():
    def __init__(self, maxSteps):
        self.maxSteps = maxSteps if maxSteps != 0 else 2**15
        self.steps = 0
        self.actions_history = []
        self.nodes_history = []
        self.final_node = None
        self.total_nodes_generated = 0

    def search(self):
        pass
    
    def get_nodes_history(self, node):
        '''
            Retorna o histórico de estados do estado inicial até o final
        '''
        self.__make_nodes_history(node)
        return self.nodes_history

    def __make_nodes_history(self, node):
        '''
            Gera recursivamente o histórico de estados para chegar ao estado raiz,
        '''
        if node.parent is not None:
            self.__make_nodes_history(node.parent)
        self.nodes_history.append(node)

    def get_actions_history(self, node):
        '''
            Gera e retorn o histórico de ações para ir do estado inicial ao final
        '''
        #self.__make_nodes_history(node)
        #for node in self.nodes_history:
        #    if node.env.action_taked is not None:
        #        self.actions_history.append(node.env.action_taked)
        return node.actions_taked

    def __str__(self):
        str = f"Estado Inicial {self.__class__.__name__}: \n"
        str += f"{self.initial_node.env}\n"
        str += f"Estado Final {self.__class__.__name__}: \n"
        str += f"{self.final_node.env}"
        str += f"Nós Gerados: {self.total_nodes_generated}\n"
        str += f"Passos: {self.steps}\n"
        actions = self.get_actions_history(self.final_node)
        actions = [action.name for action in actions if action != 'ROOT']
        total_actions = len(actions)
        str += "Ações para ir do estado inicial para o final: \n"
        if total_actions > 20:
            actions = actions[:20]
            str += f"{actions} ... + {total_actions - 19}\n"
        else:
            str += f"{actions} \n"
        return str

    def count_total_nodes(self, node):
        self.total_nodes_generated = node.count_total_nodes()

# Busca em Profundidade (Depth-First Search)
class DFS(Agent):
    def __init__(self, maxSteps):
        super().__init__(maxSteps)

    def search(self, initial_node):
        '''
            Retorna o estado solução se encontrou ou -1 se não encontrou o estado solução    
        '''
        self.initial_node = initial_node
        # Nós visitados
        self.frontier = [initial_node]
        # Nós explorados
        self.explored_nodes = []
        print("DFS procurando...")
        self.total_nodes_generated = 0
        # ---- Início da Busca ----
        while self.steps < self.maxSteps:
            self.steps += 1
            # Se não há nós para serem explorados então não há solução
            if not self.frontier:
                break
            # O estado atual é o último que foi adicionado
            current_node = self.frontier[-1]
            # Adiciona o estado atual no histórico de estados
            self.nodes_history.append(current_node)
            # Remove da lista de visitados
            self.frontier.pop()
            # Verifica se o estado atual é o objetivo
            if current_node.env.is_goal_state():
                self.final_node = current_node
                break
            # Se não for o objetivo então adiciona na lista de explorados e gera os possíveis estado a partir dele
            self.explored_nodes.append(current_node)
            current_node.generate_children()
            
            for child in current_node.children:
                IN_FRONTIER, IN_EXPLORED = [], []
                # Se está em uma das listas então vau popular a lista e ela retornará True 
                # Se Não estiver em uma lista então não vai popular a lista e ela retornará False
                IN_FRONTIER = [node for node in self.frontier if child.env == node.env]
                IN_EXPLORED = [node for node in self.explored_nodes if child.env == node.env]
                # Verifica se o possíbel estado ja foi visitado ou explorado
                # Se não foi então adiciona na lista de nós visitados para que possa ser explorado em seguida
                if not (IN_FRONTIER or IN_EXPLORED):
                    self.frontier.append(child)
            
            self.final_node = current_node
        # ---- Fim da Busca ----
        self.count_total_nodes(self.initial_node)
        return self.final_node

    def get_actions_history(self, node):
        '''
            Gera e retorna o histórico de ações para ir do estado inicial ao final
        '''
        for node in self.nodes_history:
            if node.env.action_taked is None:
                self.actions_history.append('ROOT')
            else:
                self.actions_history.append(node.env.action_taked)
        return self.actions_history
    
# Busca em Largua (Breadth-First Search)
class BFS(Agent):
    def __init__(self, maxSteps):
        super().__init__(maxSteps)
    
    def search(self, initial_node): 
        self.initial_node = initial_node
        # Nós visitados
        self.frontier = [initial_node]
        # Nós explorados
        self.explored_nodes = []
        # Históricos
        print("BFS procurando...")
        self.total_nodes_generated = 0
        # ---- Início da Busca ----
        while self.steps < self.maxSteps:
            self.steps += 1
            # Se não há nós para explorar então não há solução
            if not self.frontier:
                break
            # Remove da fila e define o estado atual
            current_node = self.frontier.pop(0)
            # Se o estado atual for o objetivo então para e define o estado final como o atual
            if current_node.is_goal():
                self.final_node = current_node
                break
            # Adiciona o estado atual na lista de nós explorados
            self.explored_nodes.append(current_node)
            # Gera os estados possíveis a partir do estado atual
            current_node.generate_children()

            for child in current_node.children:
                IN_FRONTIER, IN_EXPLORED = [], []
                # Se está em uma das listas então vai popular a lista e ela retornará True 
                # Se Não estiver em uma lista então não vai popular a lista e ela retornará False
                IN_FRONTIER = [node for node in self.frontier if child.env == node.env]
                IN_EXPLORED = [node for node in self.explored_nodes if child.env == node.env]
                # Verifica se o possíbel estado ja foi visitado ou explorado
                # Se não foi então adiciona na lista de nós visitados para que possa ser explorado em seguida
                if not (IN_FRONTIER or IN_EXPLORED):
                    self.frontier.append(child)
            
            self.final_node = current_node
        # ---- Fim da Busca ----
        self.count_total_nodes(self.initial_node)
        return self.final_node

# Busca em grafos com pesos: Dijkstra
class Dijkstra(Agent):
    def __init__(self, maxSteps: int):
        super().__init__(maxSteps)

    def search(self, initial_node: Node):
        self.steps = 0
        self.priority_queue = PriorityQueue()
        self.initial_node = initial_node
        initial_node.distance_from_root = 0
        initial_node.opened = True
        initial_node.predecessor = None
        self.explored_nodes = []
        # print('Gerando nós...')
        # initial_node.generate_levels(11)
        self.priority_queue.put(PrioritizedNode(initial_node.distance_from_root, initial_node))
        print("Dijkstra procurando...")
        while not self.priority_queue.empty() and self.steps < self.maxSteps:  
            current_node = self.priority_queue.get()
            self.explored_nodes.append(current_node.item)
            if current_node.item.env.is_goal_state():
                self.final_node = current_node.item
                break
            current_node.item.generate_children()
            self.init_dists(current_node.item)

            for child in current_node.item.children:  
                IN_QUEUE, IN_EXPLORED = False, False
                sum = child.distance_from_parent + current_node.item.distance_from_root
                if sum <= child.distance_from_root:
                    child.distance_from_root = sum
                    child.predecessor = current_node.item

                for node in self.explored_nodes:
                    if node.env == child.env:
                        IN_EXPLORED = True

                for node in self.priority_queue.queue:
                    if node.item.env == child.env:
                        IN_QUEUE = True

                if not IN_QUEUE and not IN_EXPLORED:
                    self.priority_queue.put(PrioritizedNode(child.distance_from_root, child))

            self.final_node = current_node.item
            if self.steps % 1000 == 0 and self.steps != 0:
                print(self)
            self.steps += 1

        self.count_total_nodes(self.initial_node)
        return self.final_node

    def init_dists(self, initial_node: Node):
        for child in initial_node.children:
            child.distance_from_root = float("inf")
            self.init_dists(child)
    
# Busca Gulosa (Greedy Best-First Search)
class GBFS(Agent):
    def __init__(self, maxSteps: int):
        super().__init__(maxSteps)

    def search(self, initial_node: Node):
        self.steps = 0
        self.priority_queue = PriorityQueue()
        self.initial_node = initial_node
        initial_node.distance_from_parent = 0
        self.explored_nodes = []
        self.priority_queue.put(PrioritizedNode(initial_node.distance_from_parent, initial_node))
        print("GBFS procurando...")
        while not self.priority_queue.empty() and self.steps < self.maxSteps:  
            current_node = self.priority_queue.get()
            self.explored_nodes.append(current_node.item)
            if current_node.item.env.is_goal_state():
                self.final_node = current_node.item
                break
            current_node.item.generate_children()
                
            for child in current_node.item.children:  
                IN_QUEUE, IN_EXPLORED = False, False
                for node in self.explored_nodes:
                    if node.env == child.env:
                        IN_EXPLORED = True

                for node in self.priority_queue.queue:
                    if node.item.env == child.env:
                        IN_QUEUE = True

                if not IN_QUEUE and not IN_EXPLORED:
                    self.priority_queue.put(PrioritizedNode(child.distance_from_parent, child))

            self.final_node = current_node.item
            if self.steps % 1000 == 0 and self.steps != 0:
                print(self)
            self.steps += 1

        self.count_total_nodes(self.initial_node)
        return self.final_node
    
# A*
class AStar(Agent):
    def __init__(self, maxSteps: int):
        super().__init__(maxSteps)

    def search(self, initial_node: Node):
        self.steps = 0
        self.priority_queue = PriorityQueue()
        self.initial_node = initial_node
        initial_node.distance_from_parent = 0
        self.explored_nodes = []
        self.priority_queue.put(PrioritizedNode(initial_node.distance_from_parent, initial_node))
        print("GBFS procurando...")
        while not self.priority_queue.empty() and self.steps < self.maxSteps:  
            current_node = self.priority_queue.get()
            self.explored_nodes.append(current_node.item)

            if current_node.item.env.is_goal_state():
                self.final_node = current_node.item
                break

            current_node.item.generate_children()
                
            for child in current_node.item.children:  
                IN_QUEUE, IN_EXPLORED = False, False
                for node in self.explored_nodes:
                    if node.env == child.env:
                        IN_EXPLORED = True

                for node in self.priority_queue.queue:
                    if node.item.env == child.env:
                        IN_QUEUE = True

                if not IN_QUEUE and not IN_EXPLORED:
                    sum = child.distance_from_parent + len(child.actions_taked)
                    self.priority_queue.put(PrioritizedNode(sum, child))

            self.final_node = current_node.item
            if self.steps % 1000 == 0 and self.steps != 0:
                print(self)
            self.steps += 1

        self.count_total_nodes(self.initial_node)
        return self.final_node
