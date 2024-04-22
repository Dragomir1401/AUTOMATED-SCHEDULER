
from structs import TimetableNode

class HillClimbing:
    '''Class that implements the hill climbing algorithm'''
    def __init__(self, max_iterations, initial_state : TimetableNode):
        '''Constructor for the HillClimbing class'''
        self.max_iterations = max_iterations
        self.initial_state = initial_state
    
    def hill_climbing(self):
        '''Driver function for the hill climbing algorithm'''
        iterations = 0
        current_state = self.initial_state

        while iterations < self.max_iterations:
            iterations += 1

            neighbors = current_state.get_next_states()

            if not neighbors:
                break

            for neighbor in neighbors:
                if neighbor.eval_node() < current_state.eval_node():
                    best_neighbor = neighbor
                    break
            
            if best_neighbor.eval_node() >= current_state.eval_node():
                break

            current_state = best_neighbor

        return current_state
        