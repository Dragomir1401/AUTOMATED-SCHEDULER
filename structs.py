import copy
from utils import *

class Assignment:
    def __init__(self, prof, subject):
        self.prof = prof
        self.subject = subject

class Activity:
    def __init__(self, space, assignment : Assignment):
        self.space = space
        self.assignment = assignment

class Interval:
    def __init__(self, name, activities : list[Activity]):
        self.name = name
        self.activities = {activity.space: activity for activity in activities}

class Day:
    def __init__(self, name, intervals : list[Interval]):
        self.name = name
        self.intervals = {interval.name: interval for interval in intervals}


class TimetableNode:
    def __init__(self, constraints, students_per_activity, days):
        self.constraints = constraints
        self.students_per_activity = students_per_activity
        self.days = days

    def get_next_states(self):
        next_states = []

        for day_class in self.days:
            intervals = day_class.intervals

            for interval_class in intervals:
                activities = interval_class.activities

                for activity_class in activities:
                    space_name = activity_class.space
                    if activity_class.assignment == None:
                        next_states += self.apply_constraints_on_possible_states(day_class, interval_class, space_name)
        return next_states
    
    def apply_constraints_on_possible_states(self, day_class, interval_class, space_name):
        possible_states = []

        # MS, AD, IA, PCOM, etc
        for activity_iterator in self.constraints[SALI][space_name][MATERII]:
            # 100 students, 50 students, etc
            if self.students_per_activity[activity_iterator] > 0:
                # prof, constraint
                for prof, prof_constraints in self.constraints[PROFESORI].items():
                    if self.check_constraint(prof_constraints, interval_class, activity_iterator, prof):
                        new_spot = self.choose_interval(day_class, interval_class, space_name, prof, activity_iterator, self.constraints[SALI][space_name][CAPACITATE])
                        possible_states.append(new_spot)

        return possible_states

    def check_constraint(self, constraints, interval_class, activity, profesor):
        if activity not in constraints[MATERII]:
            return False
        
        # If profesor is already assigned to an activity in the same interval
        for activity in interval_class.activities:
            if activity.assignment is not None and activity.assignment.prof == profesor:
                return False
        
        return True
    
    def choose_interval(self, day_class, interval_class, space, prof, activity, capacity):
        # Deep copy the current node info in a new node
        new_constraints = copy.deepcopy(self.constraints)
        new_students_per_activity = copy.deepcopy(self.students_per_activity)
        new_days = copy.deepcopy(self.days)

        new_node = TimetableNode(new_constraints, new_students_per_activity, new_days)
        day_index = self.get_day_index(day_class.name)
        interval_index = self.get_interval_index(interval_class.name, day_index)
        new_node.days[day_index].intervals[interval_index].activities[activity] = Activity(space, Assignment(prof, activity))
        new_node.students_per_activity[space] -= capacity
        
        return new_node
    
    def get_day_index(self, day_name):
        for idx, day in enumerate(self.days):
            if day.name == day_name:
                return idx
        return -1

    def get_interval_index(self, interval_name, day_index):
        for idx, interval in enumerate(self.days[day_index].intervals):
            if interval.name == interval_name:
                return idx
        return -1
        
    def eval_heuristic(self):
        sum = 0
        for students in self.students_per_activity:
            sum += students
        return sum


