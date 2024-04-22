
from random import choice
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
            
            best_neighbor = neighbors[0]
            for neighbor in neighbors:
                if neighbor.eval_node() < best_neighbor.eval_node():
                    best_neighbor = neighbor
            
            current_state = best_neighbor
            current_state.apply_assignment_on_best_node()


        return current_state
        