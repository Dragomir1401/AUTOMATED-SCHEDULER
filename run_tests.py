import subprocess
import re

def run_test(test_type, run_number):
    # Run the hill climbing algorithm on the test type
    hc_command = f"time python orar.py hc {test_type}"
    process = subprocess.run(hc_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Get all the output 
    output = process.stdout
    print (output)

    # Check constraints for the test type
    check_command = f"python check_constraints.py {test_type}"
    result = subprocess.run(check_command, shell=True, stdout=subprocess.PIPE, text=True)

    # Parse the output to find the number of violations
    mandatory_violations = re.search(r"S-au încălcat (\d+) constrângeri obligatorii", result.stdout)
    optional_violations = re.search(r"S-au încălcat (\d+) constrângeri optionale", result.stdout)
    mandatory_count = int(mandatory_violations.group(1)) if mandatory_violations else 0
    optional_count = int(optional_violations.group(1)) if optional_violations else 0

    # Additional metrics to capture
    not_assigned = re.search(r"Number of students not assigned: (\d+)", output)
    restarts = re.search(r"Number of restarts: (\d+)", output)
    iterations = re.search(r"Total iterations: (\d+)", output)

    not_assigned_count = int(not_assigned.group(1)) if not_assigned else 0
    restarts_count = int(restarts.group(1)) if restarts else 0
    iterations_count = int(iterations.group(1)) if iterations else 0

    # Structure to include additional details
    detailed_output = f"Test {run_number} for {test_type}:\n{output}\n\n" \
                      f"Students Not Assigned: {not_assigned_count}\n" \
                      f"Number of Restarts: {restarts_count}\n" \
                      f"Total Iterations: {iterations_count}\n"

    return detailed_output, mandatory_count, optional_count

def log_results(results, test_types):
    with open("tests_hc_b.log", "w") as file:
        for test_type in test_types:
            file.write(f"-------------------- Results for {test_type} --------------------\n")
            for result in results[test_type]:
                file.write(f"{result[0]}\nMandatory Violations: {result[1]}\nOptional Violations: {result[2]}\n\n\n-------------------\n\n\n")
            file.write("\n")  # Add extra newline for spacing between test types

def main():
    test_types = ["orar_bonus_exact"]
    results = {test: [] for test in test_types}

    for test_type in test_types:
        for run_number in range(1, 6):
            print(f"Running test {run_number} for {test_type}...")
            result = run_test(test_type, run_number)
            results[test_type].append(result)
    
    log_results(results, test_types)

if __name__ == "__main__":
    main()
