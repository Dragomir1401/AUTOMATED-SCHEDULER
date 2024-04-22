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

    def randomize(self):
        '''Randomly shuffles days and intervals for initial state'''
        day_list = list(self.days.keys())
        random.shuffle(day_list)
        for day in day_list:
            intervals = list(self.days[day].keys())
            random.shuffle(intervals)
            for interval in intervals:
                spaces = list(self.days[day][interval].keys())
                random.shuffle(spaces)
                for space in spaces:
                    if self.days[day][interval][space] is None:
                        # Assign a random activity and professor
                        possible_activities = list(self.students_per_activity.keys())
                        activity = random.choice(possible_activities)
                        possible_professors = list(self.professors.keys())
                        professor = random.choice(possible_professors)
                        self.days[day][interval][space] = (professor, activity)

    def get_next_states(self):
        '''Returns a list of next states for the current node'''
        next_states = []
        unassigned_places = [
            (day, interval, place)
            for day, intervals in self.days.items()
            for interval, assignments in intervals.items()
            for place, assignment in assignments.items()
            if assignment is None
        ]
        random.shuffle(unassigned_places)

        for day, interval, place in unassigned_places:
            next_states += self.apply_constraints_on_possible_states(day, interval, place)

        return next_states
    
    def apply_constraints_on_possible_states(self, day_name, interval_tuple, place):
        '''Returns a list of possible states for the current node'''
        possible_states = []

        # Start with classrooms because they eliminate the most possibilities
        # MS, AD, IA, PCOM, etc
        for activity in self.constraints[SALI][place][MATERII]:
            # If we still have students to assign to this activity
            # 100 students, 50 students, etc
            if self.students_per_activity[activity] > 0:
                # For each prof, check if the constraints are met
                # prof, constraint
                for prof, prof_constraints in self.constraints[PROFESORI].items():
                    if self.check_constraint(prof_constraints, day_name, interval_tuple, activity, prof):
                        # Make a list with all parameters for the new state
                        # day, interval, classroom, prof, activity, capacity
                        capacitites = self.constraints[SALI][place][CAPACITATE]
                        parameters = (day_name, interval_tuple, place, prof, activity, capacitites)
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
        
    def eval_node(self):
        '''Returns the evaluation of the current node for hill climbing'''
        sum = 0
        for activity, students in self.students_per_activity.items():
            sum += students
        return sum + self.number_of_soft_restrictions_violated() * 1000000

    def number_of_soft_restrictions_violated(self):
        '''Returns the number of soft restrictions violated'''
        number = 0

        for day_name, intervals in self.days.items():
            for interval_tuple, assignments in intervals.items():
                for place, assignment in assignments.items():
                    if assignment:
                        prof, activity = assignment
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
