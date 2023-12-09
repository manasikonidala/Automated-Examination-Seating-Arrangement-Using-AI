from constraint import Problem, AllDifferentConstraint

def graph_coloring_csp(vertices, edges, colors):
    problem = Problem()

    # Add variables for each vertex with possible color values
    for vertex in vertices:
        problem.addVariable(vertex, colors)

    # Add constraints for adjacent vertices to have different colors
    for edge in edges:
        problem.addConstraint(lambda color1, color2: color1 != color2, (edge[0], edge[1]))

    # Solve the CSP
    solutions = problem.getSolutions()

    return solutions

def load_classroom_details(classroom_id):
    # Fetch classroom details from the database based on classroom_id
    # Replace this with your actual database query
    # For example:
    # cursor.execute("SELECT BENCH_COUNT, CLASSROOM_CAPACITY FROM CLASSROOM WHERE CLASSROOM_ID = ?;", (classroom_id,))
    # bench_count, classroom_capacity = cursor.fetchone()
    # return bench_count, classroom_capacity
    return 20, 40  # Replace with the actual values fetched from the database

def classroom_constraint(*students):
    # Constraint: No two students from the same department should sit nearer to each other in the same bench
    departments = [student[1][:3] for student in students]  # Assuming department information is encoded in the first three characters
    for i in range(len(students) - 1):
        if departments[i] == departments[i + 1]:
            if abs(students[i][0] - students[i + 1][0]) == 1:
                return False
    return True

# Example usage
vertices = ['CSE1', 'CSE2', 'CSE3', 'IT1', 'IT2', 'IT3', 'ECE1', 'ECE2', 'ECE3']
edges = [('CSE1', 'CSE2'), ('CSE2', 'CSE3'), ('IT1', 'IT2'), ('IT2', 'IT3'), ('ECE1', 'ECE2'), ('ECE2', 'ECE3')]
colors = ['red', 'green', 'blue']

coloring_solutions = graph_coloring_csp(vertices, edges, colors)

# Assume classroom_id and roll_number_range_cse, roll_number_range_it, roll_number_range_ece are defined
classroom_id = 'ITA'
roll_number_range_cse = ['CSE1', 'CSE2', 'CSE3']
roll_number_range_it = ['IT1', 'IT2', 'IT3']
roll_number_range_ece = ['ECE1', 'ECE2', 'ECE3']

problem = Problem()

# Load classroom details from the database
bench_count, classroom_capacity = load_classroom_details(classroom_id)

# Define variable domains for CSE department
for roll_number in roll_number_range_cse:
    problem.addVariable(roll_number, range(1, bench_count * 2 + 1, 2))

# Define variable domains for IT department
for roll_number in roll_number_range_it:
    problem.addVariable(roll_number, range(2, bench_count * 2 + 1, 2))

# Define variable domains for ECE department
for roll_number in roll_number_range_ece:
    problem.addVariable(roll_number, range(bench_count * 2 + 1, (bench_count + 1) * 2 + 1, 2))

# Add constraint for classroom capacity
problem.addConstraint(AllDifferentConstraint(),
                      roll_number_range_cse + roll_number_range_it + roll_number_range_ece)
problem.addConstraint(classroom_constraint,
                      roll_number_range_cse + roll_number_range_it + roll_number_range_ece)

# Solve the CSP
seating_solutions = problem.getSolutions()

# Display graph coloring results
if coloring_solutions:
    print("Graph Coloring Solutions:")
    for solution in coloring_solutions:
        print(solution)
else:
    print("No valid graph coloring found.")

# Display seating arrangement results
if seating_solutions:
    print("\nSeating Arrangement:")
    for solution in seating_solutions:
        for roll_number, seat in solution:
            print(f"Bench {seat}, Seat {seat % 2 + 1}: {roll_number}")
else:
    print("No valid seating arrangement found.")
