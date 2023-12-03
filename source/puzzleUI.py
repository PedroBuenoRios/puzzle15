from puzzle import Actions
from tkinter import *
from tkinter import ttk

class PuzzleUI():
    def __init__(self, width, height, rows, colls, initial_env, agent):
        # Cria uma instancia da janela
        window = Tk()
        # Configurando a Janela
        window.title('PUZZLE-15')
        window.config(padx=10, pady=10)
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        # Mainframe
        mainframe = ttk.Frame(window, padding="3 3 12 12", width=width, height=height)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        # Labels
        self.numNodes = StringVar()
        numNodes_label = ttk.Label(mainframe, textvariable=self.numNodes)
        numNodes_label.grid(row=rows+4, column=3, sticky=(W, E))

        self.numActions = StringVar()
        numActions_label = ttk.Label(mainframe, textvariable=self.numActions)
        numActions_label.grid(row=rows+5, column=3, sticky=(W, E))

        self.solved_label = StringVar()
        ttk.Label(mainframe, textvariable=self.solved_label).grid(row=rows+6, column=3, sticky=(W, E))

        ttk.Label(mainframe, text="Número de Nós: ").grid(row=rows+4, column=0, columnspan=3, sticky=W)
        ttk.Label(mainframe, text="Número de Ações: ").grid(row=rows+5, column=0, columnspan=3, sticky=W)
        ttk.Label(mainframe, text="Solucionado: ").grid(row=rows+6, column=0, columnspan=3, sticky=W)

        self.labels_grid = []
        self.contents = []
        for r in range(rows):
            for c in range(colls):
                lb = ttk.Label(mainframe)
                lb.grid(row=r, column=c, sticky=(W, E))
                cont = StringVar()
                lb['textvariable'] = cont
                cont.set(f"{initial_env.current_state[r][c]}")
                self.contents.append(cont)
                self.labels_grid.append(lb)

        # Buttons
        btnSolve = ttk.Button(mainframe, text="Resolver", command=self.solve)
        btnSolve.grid(row=rows+1, column=0, sticky=W, columnspan=colls+1)

        btnNext = ttk.Button(mainframe, text="Proximo", command=self.next)
        btnNext.grid(row=rows+2, column=0, sticky=W, columnspan=colls+1)

        btnBack = ttk.Button(mainframe, text="Anterior", command=self.back)
        btnBack.grid(row=rows+3, column=0, sticky=W, columnspan=colls+1)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
        
        window.bind("<Return>", self.solve)
        self.window = window
        self.mainframe = mainframe
        self.agent = agent
        self.width = width
        self.height = height
        self.rows = rows
        self.colls = colls
        self.current_env = initial_env
        self.solved = False
        self.final_env = initial_env
        self.numActions.set('0')
        self.numNodes.set('0')
        self.actions_history = []
        self.current_action = 0
        self.current_index_action = 0
        # 51, 77, 77

    def solve(self, *args):
        if self.solved:
            return
        self.final_env = self.agent.search()
        self.numNodes.set(f"{self.agent.steps}")
        self.actions_history = self.agent.get_actions_history(self.final_env)
        self.current_action = self.actions_history[0]
        self.numActions.set(f"{len(self.actions_history) - 1}")
        self.current_index_action = 0
        if self.agent.steps == self.agent.maxSteps:
            self.solved_label.set("Não")
        else:
            self.solved_label.set("Sim")
        self.solved = True
       
        
    def next(self, *args):
        if self.current_index_action < len(self.actions_history) and self.solved:
            self.current_action = self.actions_history[self.current_index_action]
        else:
            return

        if self.current_action == 'ROOT':  
            self.current_index_action += 1

        self.current_action = self.actions_history[self.current_index_action]
        self.current_env.current_state = self.current_env.take_action(self.current_action)
        for r in range(self.rows):
            for c in range(self.colls):
                cont = self.contents[c + (r * self.rows)]
                cont.set(f"{self.current_env.current_state[r][c]}")
        self.current_index_action += 1
    
    def back(self, *args):
        if self.current_index_action > 0 and self.solved:
            self.current_action = self.actions_history[self.current_index_action-1]
        else:
            return

        if self.current_action == Actions.ESQUERDA:
            self.current_action = Actions.DIREITA
        elif self.current_action == Actions.DIREITA:
            self.current_action = Actions.ESQUERDA
        elif self.current_action == Actions.BAIXO:
            self.current_action = Actions.CIMA
        elif self.current_action == Actions.CIMA:
            self.current_action = Actions.BAIXO

        self.current_env.current_state = self.current_env.take_action(self.current_action)

        for r in range(self.rows):
            for c in range(self.colls):
                cont = self.contents[c + (r * self.rows)]
                cont.set(f"{self.current_env.current_state[r][c]}")
        self.current_index_action -= 1

    def show(self):
        self.window.mainloop() 