from structs import TimetableNode
from hillClimbing import HillClimbing
from utils import *
import yaml

def __init__():
    algorithm = sys.argv[1]
    file = sys.argv[2]
    input_dir = "inputs/"
    output_dir = "outputs/"
    yaml_dict = read_yaml_file(input_dir + file + ".yaml")

    days = {}
    for day_name in yaml_dict[ZILE]:
        intervals = {}
        for interval_string in yaml_dict[INTERVALE]:
            interval_start, interval_end = interval_string.split(',')

            # strip interval start and end of ()
            interval_start = interval_start[1:]
            interval_end = interval_end[:-1]

            # Make them integers and not strings
            interval_start = int(interval_start)
            interval_end = int(interval_end)

            assignments = {}
            for space in yaml_dict[SALI]:
                assignments[space] = None
            intervals[(interval_start, interval_end)] = assignments
        days[day_name] = intervals

    # Dictionary with prof names as keys and assigned activities as values
    profs = {}
    for prof in list(yaml_dict[PROFESORI].keys()):
        profs[prof] = 0

    initial_node = TimetableNode(yaml_dict, yaml_dict[MATERII], days, profs)
    if algorithm == 'hc':
        hill_climbing = HillClimbing(1000, initial_node)
        result = hill_climbing.hill_climbing()
        table_Str = pretty_print_timetable(result.days, input_dir + file + ".yaml")
        
        # Create output file as output/dummy.txt
        with open(output_dir + file + ".txt", 'w') as file:
            file.write(table_Str)
    else:
        print("Algorithm not implemented")

__init__()