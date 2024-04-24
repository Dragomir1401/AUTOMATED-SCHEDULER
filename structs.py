import copy
from functools import lru_cache
import random
from utils import *

class ConstraintManager:
    '''Class that handles constraints shared across all TimetableNodes'''
    def __init__(self, constraints, initial_total_students):
        self.constraints = constraints
        self.initial_total_students = initial_total_students

    @lru_cache(maxsize=None)
    def compute_number_of_accepted_activities_per_place(self, place):
        '''Returns the number of accepted activities per place'''
        number = 0
        for activity in self.constraints[SALI][place][MATERII]:
            number += 1

        return number
    
    @lru_cache(maxsize=None)
    def number_of_places_accepting_activity(self, activity):
        '''Returns the number of places accepting the activity'''
        number = 0
        for place in self.constraints[SALI]:
            if activity in self.constraints[SALI][place][MATERII]:
                number += 1

        return number

class TimetableNode:
    '''Class that represents a node in searching algorithm'''

    def __init__(self, 
                 constraints_manager: ConstraintManager, 
                 students_per_activity: dict[str, int],
                 days: dict[str, dict[str, dict[str, (str, str)]]],
                 professors : dict[str, int],
                 chosen_assignment = None,
                 g = 0):
        '''Constructor for the TimetableNode class'''
        self.constraints_manager = constraints_manager
        self.students_per_activity = students_per_activity
        self.days = days
        self.professors = professors
        self.chosen_assignment = chosen_assignment

    def get_next_states(self):
        '''Returns a list of next states for the current node with added randomness for diversity.'''
        next_states = []
        for day_name, intervals in self.days.items():
            for interval_tuple, assignments in intervals.items():
                sorted_assignments = sorted(assignments.items(), key=lambda x: self.constraints_manager.compute_number_of_accepted_activities_per_place(x[0]))
                random.shuffle(sorted_assignments)  # Shuffle to introduce randomness
                for place, assignment in sorted_assignments:
                    if assignment == None:
                        possible_states = self.apply_constraints_on_possible_states(day_name, interval_tuple, place)
                        next_states.extend(possible_states)
                        # Introduce a random selection element
                        if random.random() < 0.1 and possible_states:  # 10% chance to break the pattern
                            random_choice = random.choice(possible_states)
                            next_states.append(random_choice)
        return next_states
    
    def apply_constraints_on_possible_states(self, day_name, interval_tuple, place):
        '''Returns a list of possible states for the current node'''
        possible_states = []
        
        # Sort activities by the number of students needing assignment
        sorted_activities = sorted(self.constraints_manager.constraints[SALI][place][MATERII],
                                   key=lambda act: -self.students_per_activity[act])
        
        # Then sort activities by the number of places accepting the activity
        sorted_activities = sorted(sorted_activities,
                                   key=lambda act: self.constraints_manager.number_of_places_accepting_activity(act))

        for activity in sorted_activities:
            if self.students_per_activity[activity] > 0:
                for prof, prof_constraints in self.constraints_manager.constraints[PROFESORI].items():
                    if self.check_constraint(prof_constraints, day_name, interval_tuple, activity, prof):
                        capacities = self.constraints_manager.constraints[SALI][place][CAPACITATE]
                        parameters = (day_name, interval_tuple, place, prof, activity, capacities)
                        new_spot = self.choose_interval(parameters)
                        possible_states.append(new_spot)

        return possible_states

    def check_constraint(self, constraints, day_name, interval_tuple, activity, profesor):
        '''Returns True if the constraints are met, False otherwise'''

        # If day is not available
        if day_name not in self.constraints_manager.constraints[ZILE]:
            return False

        # Profesors can't have more than 7 activities
        if self.professors[profesor] > 6:
            return False

        # If activity is not in the constraints
        if activity not in constraints[MATERII]:
            return False
        
        # If profesor is already assigned to an activity in the same interval
        for place, assignment in self.days[day_name][interval_tuple].items():
            if assignment and assignment[0] == profesor:
                return False

        # If room is already used in that interval
        for place, assignment in self.days[day_name][interval_tuple].items():
            if assignment and assignment[1] == activity:
                return False
            
        return True
    
    def choose_interval(self, parameters):
        '''Returns a new node with the assignment chosen'''
        day_name, interval_tuple, space, prof, activity, capacity = parameters
        assignment = (day_name, interval_tuple, space, prof, activity)

        new_student_per_activity = copy.copy(self.students_per_activity)
        new_professors = copy.copy(self.professors)
        new_student_per_activity[activity] -= capacity
        new_professors[prof] += 1

        new_node = TimetableNode(self.constraints_manager, new_student_per_activity, self.days, new_professors, assignment)
        
        return new_node
    
    def apply_assignment_on_best_node(self):
        '''Applies the best assignment on the current node'''
        day, interval, space, prof, activity = self.chosen_assignment
        self.days[day][interval][space] = (prof, activity)

        
    def eval_node(self):
        '''Returns the evaluation of the current node for hill climbing with adjusted weights and penalties.'''
        remaining_students = self.get_remaining_students()
        soft_violations = self.number_of_soft_restrictions_violated()

        # Using exponential penalties for remaining students to ensure it's a priority
        student_penalty = (remaining_students ** 2) * 50

        # Dynamically adjust weights based on the current state
        if remaining_students < remaining_students / 5:
            constraint_penalty = soft_violations * 300000  # Increase penalty as we get closer to assigning all students
        else:
            constraint_penalty = soft_violations * 100000

        return student_penalty + constraint_penalty
    
    def h(self):
        # Adjust the heuristic based on the number of unassigned students
        remaining_students = self.get_remaining_students()
        return (remaining_students ** 2) * 50  # Exponential penalty to push for student assignment

    def g(self):
        # Add a dynamic element based on the number of assignments and violations
        return self.number_of_assignments() + 1000 * self.number_of_soft_restrictions_violated()

    def total_cost(self):
        return self.g() + self.h()

    def number_of_assignments(self):
        '''Returns the number of assignments in the current node'''
        number = 0
        for day_name, intervals in self.days.items():
            for interval_tuple, assignments in intervals.items():
                for place, assignment in assignments.items():
                    if assignment:
                        number += 1

        # Make one more step for the chosen assignment
        if self.chosen_assignment:
            number += 1

        return number
    
    def __lt__(self, other):
        # Custom comparison for heapq
        # First compare based on total cost, then by other criteria
        if self.total_cost() == other.total_cost():
            # Secondary criteria
            return self.eval_node() < other.eval_node()

    def get_remaining_students(self):
        '''Returns the number of remaining students to be assigned'''
        return sum(self.students_per_activity.values())

    def number_of_soft_restrictions_violated(self):
        '''Returns the number of soft restrictions violated'''
        number = 0

        for day_name, intervals in self.days.items():
            for interval_tuple, assignments in intervals.items():
                for place, assignment in assignments.items():
                    if assignment:
                        prof = assignment[0]
                        number = self.number_of_constrains_violated(day_name, interval_tuple, prof, number)

        # Make one more step for the chosen assignment
        if self.chosen_assignment:
            prof = self.chosen_assignment[3]
            number = self.number_of_constrains_violated(self.chosen_assignment[0], self.chosen_assignment[1], prof, number)

        return number
    
    def number_of_constrains_violated(self, day_name, interval_tuple, prof, number):
        prof_constraints = self.constraints_manager.constraints[PROFESORI][prof][CONSTRANGERI]
            
        for constraint in prof_constraints:
            if "!" in constraint:
                if '-' in constraint:
                    # Break the interval into start and end
                    start, end = constraint.split('-')
                    start = start[1:]
                    start = int(start)
                    end = int(end)
                    if start <= interval_tuple[0] <= interval_tuple[1] <= end:
                        number += 1
                elif '>' in constraint:
                    pause = int(constraint.split()[2])
                    # If the interval tuple creates a pause greater than the constraint
                    if interval_tuple[1] - interval_tuple[0] > pause:
                        number += 1
                else:
                    if day_name in constraint:
                        number += 1
        return number

    
    def clone(self):
        '''Creates a deep copy of this TimetableNode'''
        # Deep copy ensures that all dicts and lists are new objects
        new_students_per_activity = copy.deepcopy(self.students_per_activity)
        new_days = copy.deepcopy(self.days)
        new_professors = copy.deepcopy(self.professors)
        new_chosen_assignment = copy.deepcopy(self.chosen_assignment)
        
        # Create a new instance of TimetableNode with the copied data
        return TimetableNode(self.constraints_manager, new_students_per_activity, new_days, new_professors, new_chosen_assignment)
