from random import choice, seed
import random
from structs import TimetableNode
import heapq

class RandomRestartHillClimbing:
    '''Class that implements the hill climbing algorithm with random restarts'''
    def __init__(self, max_restarts, max_iterations, initial_state: TimetableNode):
        '''Constructor for the RandomRestartHillClimbing class'''
        self.max_restarts = max_restarts
        self.max_iterations = max_iterations
        self.initial_state = initial_state
        self.init_state_base = initial_state.clone()
        self.seeds = [42, 69, 420, 666, 1337, 9001, 80085, 8008135, 80081355, 800813555]

    def random_restart_hill_climbing(self):
        '''Driver function for the random restart hill climbing algorithm'''
        best_solution = None
        best_evaluation = float('inf')
        total_iterations = 0
        number_of_restarts = 0

        for _ in range(self.max_restarts):
            current_state = self.init_state_base.clone()  # Ensure we start with a fresh state
            iterations, solution = self.hill_climbing(current_state)

            total_iterations += iterations
            current_evaluation = solution.eval_node()

            if current_evaluation <= best_evaluation:
                best_evaluation = current_evaluation
                best_solution = solution
            
            if solution.eval_node() == 0:
                print("Solution found faster than programmed restarts!")
                print("Students not assigned per activity: ")
                print(solution.students_per_activity)
                break
            
            number_of_restarts += 1
        
        print(f"Number of students not assigned: {best_solution.get_remaining_students()}")
        print(f"Number of restarts: {number_of_restarts}")
        return best_solution, total_iterations

    def hill_climbing(self, initial_state):
        '''Actual hill climbing algorithm used within each restart'''
        iterations = 0
        current_state = initial_state

        while iterations < self.max_iterations:
            iterations += 1

            neighbors = current_state.get_next_states()
            
            if not neighbors:
                break
            
            if iterations == 1:
                seed = choice(self.seeds)
                random.seed(seed)
                print("First iteration with seed: ", seed)
                random.shuffle(neighbors)
                random.shuffle(self.seeds)
                best_neighbor = neighbors[0]
            else:
                best_neighbor = min(neighbors, key=lambda x: x.eval_node())

            if best_neighbor.get_remaining_students() >= current_state.get_remaining_students():
                break

            current_state = best_neighbor
            current_state.apply_assignment_on_best_node()

        return iterations, current_state

class AStarSearch:
    def __init__(self, initial_state):
        self.initial_state = initial_state

    def search(self):
        open_set = []
        closed_set = set()
        heapq.heappush(open_set, (self.initial_state.total_cost(), self.initial_state))

        while open_set:
            current_node = heapq.heappop(open_set)[1]
            remaining_students = current_node.get_remaining_students()
            
            print("Remaining students: " + str(remaining_students))
            print("Current g: " + str(current_node.g()))
            print("Current h: " + str(current_node.h()))

            if remaining_students == 0:
                print("Students not assigned per activity: ")
                print(current_node.students_per_activity)
                return current_node

            closed_set.add(current_node)
            neighbours = current_node.get_next_states()

            for neighbor in neighbours:
                if neighbor in closed_set:
                    continue

                clone = neighbor.clone()
                clone.apply_assignment_on_best_node()
                heapq.heappush(open_set, (clone.total_cost(), clone))

        return None  # No solution found

