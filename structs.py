import copy
import random
from utils import *

class TimetableNode:
    '''Class that represents a node in searching algorithm'''

    def __init__(self, 
                 constraints, 
                 students_per_activity, 
                 days: dict[str, dict[str, dict[str, (str, str)]]],
                 professors : dict[str, int],
                 chosen_assignment = None):
        '''Constructor for the TimetableNode class'''
        self.constraints = constraints
        self.students_per_activity = students_per_activity
        self.days = days
        self.professors = professors
        self.chosen_assignment = chosen_assignment

    def get_next_states(self):
        '''Returns a list of next states for the current node'''
        next_states = []
        for day_name, intervals in self.days.items():
            for interval_tuple, assignments in intervals.items():
                # Sort assignments by places with least activities accepted
                sorted_assignments = sorted(assignments.items(), key=lambda x: self.compute_number_of_accepted_activities_per_place(x[0]))
                for place, assigment in sorted_assignments:
                    if assigment == None:
                        next_states += self.apply_constraints_on_possible_states(day_name, interval_tuple, place)
        return next_states
    
    def apply_constraints_on_possible_states(self, day_name, interval_tuple, place):
        '''Returns a list of possible states for the current node'''
        possible_states = []
        
        # Sort activities by the number of students needing assignment
        sorted_activities = sorted(self.constraints[SALI][place][MATERII],
                                   key=lambda act: -self.students_per_activity[act])

        for activity in sorted_activities:
            if self.students_per_activity[activity] > 0:
                for prof, prof_constraints in self.constraints[PROFESORI].items():
                    if self.check_constraint(prof_constraints, day_name, interval_tuple, activity, prof):
                        capacities = self.constraints[SALI][place][CAPACITATE]
                        parameters = (day_name, interval_tuple, place, prof, activity, capacities)
                        new_spot = self.choose_interval(parameters)
                        possible_states.append(new_spot)

        return possible_states

    def check_constraint(self, constraints, day_name, interval_tuple, activity, profesor):
        '''Returns True if the constraints are met, False otherwise'''

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
            
        return True
    
    def find_empty_spaces(self):
        '''Returns a list of empty spaces in the timetable'''
        empty_spaces = []
        for day_name, intervals in self.days.items():
            for interval_tuple, assignments in intervals.items():
                for place, assignment in assignments.items():
                    if assignment == None:
                        empty_spaces.append((day_name, interval_tuple, place))
        return empty_spaces
    
    def choose_interval(self, parameters):
        '''Returns a new node with the assignment chosen'''
        day_name, interval_tuple, space, prof, activity, capacity = parameters
        assignment = (day_name, interval_tuple, space, prof, activity)

        new_student_per_activity = copy.copy(self.students_per_activity)
        new_professors = copy.copy(self.professors)
        new_student_per_activity[activity] -= capacity
        new_professors[prof] += 1

        new_node = TimetableNode(self.constraints, new_student_per_activity, self.days, new_professors, assignment)
        
        return new_node
    
    def apply_assignment_on_best_node(self):
        '''Applies the best assignment on the current node'''
        day, interval, space, prof, activity = self.chosen_assignment
        self.days[day][interval][space] = (prof, activity)

    def compute_number_of_accepted_activities_per_place(self, place):
        '''Returns the number of accepted activities per place'''
        number = 0
        for activity in self.constraints[SALI][place][MATERII]:
            number += 1

        return number
        
    def eval_node(self):
        '''Returns the evaluation of the current node for hill climbing'''
        remaining_students = self.get_remaining_students() * 67
        penalty = self.number_of_soft_restrictions_violated() * 2000
        return remaining_students + penalty

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
        prof_constraints = self.constraints[PROFESORI][prof][CONSTRANGERI]
            
        for interval_constraint in prof_constraints:
            if "!" in interval_constraint:
                if '-' in interval_constraint:
                    # Break the interval into start and end
                    start, end = interval_constraint.split('-')
                    start = start[1:]
                    start = int(start)
                    end = int(end)
                    if start <= interval_tuple[0] <= interval_tuple[1] <= end:
                        number += 1
                else:
                    if day_name in interval_constraint:
                        number += 1
        return number

    

    def clone(self):
        '''Creates a deep copy of this TimetableNode'''
        # Deep copy ensures that all dicts and lists are new objects
        new_constraints = copy.deepcopy(self.constraints)
        new_students_per_activity = copy.deepcopy(self.students_per_activity)
        new_days = copy.deepcopy(self.days)
        new_professors = copy.deepcopy(self.professors)
        new_chosen_assignment = copy.deepcopy(self.chosen_assignment)
        
        # Create a new instance of TimetableNode with the copied data
        return TimetableNode(new_constraints, new_students_per_activity, new_days, new_professors, new_chosen_assignment)
