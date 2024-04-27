def count_pause_violations(imposed_max_pause, prof_assignments):
    '''Returns the number of pause violations for a professor'''
    last_interval = (6, 8)
    bigger_pauses = []
    day = prof_assignments[0][0]
    
    for prof_assignment in prof_assignments:
        # If day changed, reset last interval
        if prof_assignment[0] != day:
            last_interval = (6, 8)
            day = prof_assignment[0]
        pause = prof_assignment[1][0] - last_interval[1]
        if pause > imposed_max_pause:
            bigger_pauses.append(pause)
        last_interval = prof_assignment[1]
            
    return len(bigger_pauses)

def test_count_pause_violations():
    # Test setup
    imposed_max_pause = 0
    prof_assignments = [
        ('Tuesday', (8, 10)),
        ('Monday', (8, 10)),
        ('Tuesday', (18, 20)),
        ('Monday', (14, 16)),
        ('Tuesday', (14, 16)),
        ('Monday', (18, 20)),
    ]

    prof_assignments.sort(key=lambda x: (x[0], x[1]))
    print (prof_assignments)
    
    # Call the function with test data
    result = count_pause_violations(imposed_max_pause, prof_assignments)

    print (result)

# Running the test function
test_count_pause_violations()
