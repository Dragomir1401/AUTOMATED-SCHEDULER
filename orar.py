import os
from structs import TimetableNode
from hillClimbing import HillClimbing
from utils import *
MAX_HC_ITERATIONS = 1000

def create_days_dict(yaml_dict):
    days = {}
    for day_name in yaml_dict[ZILE]:
        intervals = {}
        for interval_string in yaml_dict[INTERVALE]:
            interval_start, interval_end = interval_string.split(',')

            # strip interval start and end of ()
            interval_start = interval_start[1:]
            interval_end = interval_end[:-1]

            # Make them integers
            interval_start = int(interval_start)
            interval_end = int(interval_end)

            assignments = {}
            for space in yaml_dict[SALI]:
                assignments[space] = None
            intervals[(interval_start, interval_end)] = assignments
        days[day_name] = intervals
    return days

def create_professors_dict(yaml_dict):
    profs = {}
    for prof in list(yaml_dict[PROFESORI].keys()):
        profs[prof] = 0
    return profs

def write_result_to_file(result, input_dir, output_dir):
    table_str = pretty_print_timetable(result.days, input_dir + file + ".yaml")

    with open(output_dir + file + ".txt", 'w') as file:
        file.write(table_str)

def __init__():
    algorithm = sys.argv[1]
    file = sys.argv[2]
    input_dir = "inputs/"
    output_dir = "outputs/"
    
    # check if the file exists
    if not os.path.isfile(input_dir + file + ".yaml"):
        print("File not found")
        return
    
    yaml_dict = read_yaml_file(input_dir + file + ".yaml")
    days = create_days_dict(yaml_dict)
    profs = create_professors_dict(yaml_dict)

    initial_node = TimetableNode(yaml_dict, yaml_dict[MATERII], days, profs)

    if algorithm == 'hc':
        print("Hill Climbing...")
        hill_climbing = HillClimbing(MAX_HC_ITERATIONS, initial_node)
        result = hill_climbing.hill_climbing()
        write_result_to_file(result, input_dir, output_dir)
    else:
        print("Algorithm not implemented")

__init__()