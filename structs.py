import copy
from utils import *

class Assignment:
    def __init__(self, prof, subject):
        self.prof = prof
        self.subject = subject

class Interval:
    def __init__(self, places, assignments : dict[str, Assignment]):
        if assignments == None:
            self.assignments = {place : None for place in places}
        else:
            self.assigmments = {place : assignment for place, assignment in zip(places, assignments)}

class Day:
    def __init__(self, names, intervals : dict[str, Interval]):
        self.intervals = {name : interval for name, interval in zip(names, intervals)}

class TimetableNode:
    def __init__(self, constraints, students_per_activity, days: dict[str, Day]):
        self.constraints = constraints
        self.students_per_activity = students_per_activity
        self.days = days

    def get_next_states(self):
        next_states = []

        for day_name, intervals in self.days.items():
            print (day_name)
            print (intervals)
            for interval_name, assignments in intervals.intervals.items():
                for assigmment_place, assigmment in assignments.assignments.items():
                    if assigmment == None:
                        next_states += self.apply_constraints_on_possible_states(day_name, interval_name, assigmment_place)
        return next_states
    
    def apply_constraints_on_possible_states(self, day_name, interval_name, assigmment_place):
        possible_states = []

        # MS, AD, IA, PCOM, etc
        for activity in self.constraints[SALI][assigmment_place][MATERII]:
            # 100 students, 50 students, etc
            if self.students_per_activity[activity] > 0:
                # prof, constraint
                for prof, prof_constraints in self.constraints[PROFESORI].items():
                    if self.check_constraint(prof_constraints, day_name, interval_name, activity, prof):
                        new_spot = self.choose_interval(day_name, interval_name, assigmment_place, prof, activity, self.constraints[SALI][assigmment_place][CAPACITATE])
                        possible_states.append(new_spot)

        return possible_states

    def check_constraint(self, constraints, day_name, interval, activity, profesor):
        if activity not in constraints[MATERII]:
            return False
        
        # If profesor is already assigned to an activity in the same interval
        for place, assignment in self.days[day_name].intervals[interval].assigmments.items():
            if assignment and assignment.prof == profesor:
                return False
        return True
    
    def choose_interval(self, day_name, interval, space, prof, activity, capacity):
        # Deep copy the current node info in a new node
        new_constraints = copy.deepcopy(self.constraints)
        new_students_per_activity = copy.deepcopy(self.students_per_activity)
        new_days = copy.deepcopy(self.days)

        new_node = TimetableNode(new_constraints, new_students_per_activity, new_days)
        new_node.days[day_name].intervals[interval].assigmments[space] = Assignment(prof, activity)
        new_node.students_per_activity[activity] -= capacity
        
        return new_node
        
    def eval_heuristic(self):
        sum = 0
        for students in self.students_per_activity:
            sum += students
        return sum


