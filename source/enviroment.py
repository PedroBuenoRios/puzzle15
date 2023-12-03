from abc import ABC, abstractmethod

class ABCEnviroment(ABC):
    def __init__(self):
        pass
        
    def __str__(self):
        return "Current State:\n" + f"{self.current_state}"

    def generate_states(self):
        pass

    def generate_initial_state(self):
        pass

    def cost(self):
        pass
    
    @abstractmethod
    def is_goal_state(self):
        pass

