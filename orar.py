from structs import TimetableNode, Day, Interval
from hillClimbing import HillClimbing
from utils import *
import yaml

def create_pretty_print_dict(timetable):
    pretty_print_dict = {}
    for day in timetable:
        pretty_print_dict[day] = {}
        for interval in timetable[day]:
            pretty_print_dict[day][interval] = {}
            for classroom in timetable[day][interval]:
                if timetable[day][interval][classroom]:
                    prof, subject = timetable[day][interval][classroom]
                    pretty_print_dict[day][interval][classroom] = (prof, subject)
                else:
                    pretty_print_dict[day][interval][classroom] = None
    return pretty_print_dict

def write_yaml_file(filepath, data):
    with open(filepath, 'w') as file:
        yaml.dump(data, file)


def __init__():
    algorithm = sys.argv[1]
    input_dir = "inputs"
    yaml_dict = read_yaml_file(input_dir + '/dummy.yaml')

    days = {}
    for day_name in yaml_dict[ZILE]:
        intervals = {}
        for interval_name in yaml_dict[INTERVALE]:
            interval = Interval(yaml_dict[SALI], None)
            intervals[interval_name] = interval
        day = Day(day_name, intervals)
        days[day_name] = day
    
    initial_node = TimetableNode(yaml_dict, yaml_dict[MATERII], days)
    if algorithm == 'hillClimbing':
        hill_climbing = HillClimbing(1000, initial_node)
        result = hill_climbing.hill_climbing()
        pretty_print_dict = create_pretty_print_dict(result)
        # print the dict in output path as a yaml file
        write_yaml_file('outputs/orar.yaml', pretty_print_dict)
        pretty_print_timetable(pretty_print_dict, 'outputs/orar.yaml')


__init__()