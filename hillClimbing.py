
from structs import TimetableNode

class HillClimbing:
    def __init__(self, max_iterations, initial_state : TimetableNode):
        self.max_iterations = max_iterations
        self.initial_state = initial_state
    
    def hill_climbing(self):
        iterations = 0
        current_state = self.initial_state

        while iterations < self.max_iterations:
            iterations += 1

            neighbors = current_state.get_next_states()

            if not neighbors:
                break

            for neighbor in neighbors:
                if neighbor.eval_heuristic() < current_state.eval_heuristic():
                    best_neighbor = neighbor
                    break
            
            if best_neighbor.eval_heuristic() >= current_state.eval_heuristic():
                break

            current_state = best_neighbor

        return current_state
        