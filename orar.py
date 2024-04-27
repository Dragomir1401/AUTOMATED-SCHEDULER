import os
from structs import TimetableNode, ConstraintManager
from algorithms import RandomRestartHillClimbing, AStarSearch
from utils import *

MAX_HC_ITERATIONS = 1000
MAX_RESTARTS = 20


def create_days_dict(yaml_dict):
    """Creates the days dictionary from the yaml dictionary"""
    days = {}
    for day_name in yaml_dict[ZILE]:
        intervals = {}
        for interval_string in yaml_dict[INTERVALE]:
            interval_start, interval_end = interval_string.split(",")

            # Strip interval start and end of ()
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
    """Creates the professors dictionary from the yaml dictionary"""
    profs = {}
    for prof in list(yaml_dict[PROFESORI].keys()):
        profs[prof] = 0
    return profs


def write_result_to_file(result, input_dir, output_dir, filename):
    """Writes the result to a file"""
    table_str = pretty_print_timetable(result.days, input_dir + filename + ".yaml")

    with open(output_dir + filename + ".txt", "w") as file:
        file.write(table_str)


def __init__():
    """Main function"""
    algorithm = sys.argv[1]
    filename = sys.argv[2]
    input_dir = "inputs/"
    output_dir = "outputs/"

    # Check if the file exists
    if not os.path.isfile(input_dir + filename + ".yaml"):
        print("File not found")
        return

    # Read the yaml file
    yaml_dict = read_yaml_file(input_dir + filename + ".yaml")

    # Create the days and professors dictionaries
    days = create_days_dict(yaml_dict)

    # Create the professors dictionary
    profs = create_professors_dict(yaml_dict)

    # Compute number of initial total students
    total_students = 0
    for subject in yaml_dict[MATERII]:
        total_students += yaml_dict[MATERII][subject]

    # Create the initial node
    constraints_manager = ConstraintManager(yaml_dict, total_students)
    initial_node = TimetableNode(constraints_manager, yaml_dict[MATERII], days, profs)

    if algorithm == "hc":
        print("Hill Climbing...")
        hill_climbing = RandomRestartHillClimbing(
            MAX_RESTARTS, MAX_HC_ITERATIONS, initial_node
        )
        result, total_iterations = hill_climbing.random_restart_hill_climbing()
        print(f"Total iterations: {total_iterations}")
        write_result_to_file(result, input_dir, output_dir, filename)
    elif algorithm == "astar":
        print("A*...")
        astar = AStarSearch(initial_node)
        result = astar.search()
        write_result_to_file(result, input_dir, output_dir, filename)
    else:
        print("Algorithm not implemented")


__init__()
