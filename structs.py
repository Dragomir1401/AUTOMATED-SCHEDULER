import copy
from utils import *

class TimetableNode:
    def __init__(self, constraints, students_per_activity, days: dict[str, dict[str, dict[str, (str, str)]]]):
        self.constraints = constraints
        self.students_per_activity = students_per_activity
        self.days = days

    def get_next_states(self):
        next_states = []

        for day_name, intervals in self.days.items():
            for interval_tuple, assignments in intervals.items():
                for place, assigment in assignments.items():
                    if assigment == None:
                        next_states += self.apply_constraints_on_possible_states(day_name, interval_tuple, place)
        return next_states
    
    def apply_constraints_on_possible_states(self, day_name, interval_tuple, assigmment_place):
        possible_states = []

        # MS, AD, IA, PCOM, etc
        for activity in self.constraints[SALI][assigmment_place][MATERII]:
            # 100 students, 50 students, etc
            if self.students_per_activity[activity] > 0:
                # prof, constraint
                for prof, prof_constraints in self.constraints[PROFESORI].items():
                    if self.check_constraint(prof_constraints, day_name, interval_tuple, activity, prof):
                        new_spot = self.choose_interval(day_name, interval_tuple, assigmment_place, prof, activity, self.constraints[SALI][assigmment_place][CAPACITATE])
                        possible_states.append(new_spot)

        return possible_states

    def check_constraint(self, constraints, day_name, interval_tuple, activity, profesor):
        if activity not in constraints[MATERII]:
            return False
        
        # If profesor is already assigned to an activity in the same interval
        for place, assignment in self.days[day_name][interval_tuple].items():
            if assignment and assignment[0] == profesor:
                return False
        return True
    
    def choose_interval(self, day_name, interval_tuple, space, prof, activity, capacity):
        # Deep copy the current node info in a new node
        new_constraints = copy.deepcopy(self.constraints)
        new_students_per_activity = copy.deepcopy(self.students_per_activity)
        new_days = copy.deepcopy(self.days)

        new_node = TimetableNode(new_constraints, new_students_per_activity, new_days)
        new_node.days[day_name][interval_tuple][space] = (prof, activity)
        new_node.students_per_activity[activity] -= capacity
        
        return new_node
        
    def eval_heuristic(self):
        sum = 0
        for activity, students in self.students_per_activity.items():
            sum += students
        return sum


