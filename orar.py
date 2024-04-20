from utils import *

# Create a node struct
class Node:
    def __init__(self, day, interval, space, prof, subject):
        self.day = day
        self.interval = interval
        self.space = space
        self.prof = prof
        self.subject = subject
    
    def __str__(self):
        return f'{self.day} {self.space} {self.prof} {self.subject}'
    
def create_node(day, space, prof, subject):
    return Node(day, space, prof, subject)


def __init__():
    input_dir = 'inputs'
    yaml_dict = read_yaml_file(input_dir + '/dummy.yaml')
    name_to_initials, initials_to_name = get_profs_initials(yaml_dict[PROFESORI].keys())


__init__()