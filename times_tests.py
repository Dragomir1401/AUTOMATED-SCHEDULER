import subprocess
import re
import time


def run_test(test_type, run_number, algorithm="astar"):
    # Prepare to capture the execution time
    start_time = time.time()

    # Run the A* algorithm on the test type
    command = f"python orar.py {algorithm} {test_type}"
    process = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Calculate execution time
    elapsed_time = time.time() - start_time
    output = process.stdout

    if algorithm == "astar":
        # Suppressed detailed A* algorithm output
        output = "A* algorithm output is suppressed."

    # Parse additional metrics as needed from output
    not_assigned = re.search(r"Number of students not assigned: (\d+)", output)
    not_assigned_count = int(not_assigned.group(1)) if not_assigned else 0

    # Log results to file
    with open("times_hc.log", "a") as log_file:
        log_file.write(
            f"Elapsed time for test {run_number} on {test_type}: {elapsed_time:.2f} seconds\n"
        )
        log_file.write(f"{output}\n")
        log_file.write(f"Not Assigned Students: {not_assigned_count}\n\n")

    return elapsed_time


MIC = "orar_mic_exact"
MEDIU = "orar_mediu_relaxat"
MARE = "orar_mare_relaxat"
CONSTRANS = "orar_constrans_incalcat"
DUMMY = "dummy"
BONUS = "orar_bonus_exact"


def main():
    test_types = [MIC, DUMMY, MEDIU, MARE, CONSTRANS]

    for test_type in test_types:
        print(f"Running tests for {test_type}...\n")
        with open("times_hc.log", "a") as log_file:
            log_file.write(
                f"-------------------- Results for {test_type} --------------------\n"
            )

        times = []

        # Run 3 to 5 examples for each test type
        for run_number in range(1, 6):
            elapsed_time = run_test(test_type, run_number, "hc")
            times.append(elapsed_time)

        # Calculate average time and log to file
        average_time = sum(times) / len(times)
        with open("times_hc.log", "a") as log_file:
            log_file.write(
                f"Average run time for {test_type}: {average_time:.2f} seconds\n\n"
            )

        print(f"Average run time for {test_type}: {average_time:.2f} seconds")


if __name__ == "__main__":
    main()
