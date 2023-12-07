---
mathjax: true
---
# puzzle15

## Soluciona o problema do Puzzle-15 com diferentes algoritmos

O intuito deste repositório é servir de estudo para a implementação dos algoritmos de busca em grafos.
Então foram desenvolvidos os algoritmos: BFS; DFS; Dijkstra; GBFS; A*.

A heurística usada no Dijkstra, GBFS e A* é a distância de Manhatan.
Podemos calcular a distâncida de Manhatan como:
$$
    |x_2 - x_1| + |y_2 - y_1|
$$


### BFS (Breadth-First Search ou Busca em Largura):

```py
    def search(self, initial_node): 
        self.initial_node = initial_node
        # Nós visitados
        self.frontier = [initial_node]
        # Nós explorados
        self.explored_nodes = []
        print("BFS procurando...")
        self.total_nodes_generated = 0
        # ---- Início da Busca ----
        while self.steps < self.maxSteps:
            self.steps += 1

            if not self.frontier:
                break
            current_node = self.frontier.pop(0)

            if current_node.is_goal():
                self.final_node = current_node
                break
            self.explored_nodes.append(current_node)
            current_node.generate_children()

            for child in current_node.children:
                IN_FRONTIER, IN_EXPLORED = [], []
                
                IN_FRONTIER = [node for node in self.frontier if child.env == node.env]
                IN_EXPLORED = [node for node in self.explored_nodes if child.env == node.env]
                
                if not (IN_FRONTIER or IN_EXPLORED):
                    self.frontier.append(child)
            
            self.final_node = current_node
        # ---- Fim da Busca ----
        self.count_total_nodes(self.initial_node)
```

---

DFS (Depth-First Search ou Busca em Profundidade):

```py
def search(self, initial_node):
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
        
            if not self.frontier:
                break
            
            current_node = self.frontier[-1]
            self.nodes_history.append(current_node)
            self.frontier.pop()
           
            if current_node.env.is_goal_state():
                self.final_node = current_node
                break
            
            self.explored_nodes.append(current_node)
            current_node.generate_children()
            
            for child in current_node.children:
                IN_FRONTIER, IN_EXPLORED = [], []
               
                IN_FRONTIER = [node for node in self.frontier if child.env == node.env]
                IN_EXPLORED = [node for node in self.explored_nodes if child.env == node.env]

                if not (IN_FRONTIER or IN_EXPLORED):
                    self.frontier.append(child)
            
            self.final_node = current_node
        # ---- Fim da Busca ----
        self.count_total_nodes(self.initial_node)
```
---

### Dijkstra
```py
def search(self, initial_node: Node):
        self.steps = 0
        self.priority_queue = PriorityQueue()
        self.initial_node = initial_node
        initial_node.distance_from_root = 0
        self.explored_nodes = []
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
```
---

### GBFS (Greedy Best-First Search ou Busca Gulosa)
```py
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
```
---
A* (A Star ou Estrela)
```py
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
```