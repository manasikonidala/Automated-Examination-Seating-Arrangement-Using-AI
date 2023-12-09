from constraint import Problem, AllDifferentConstraint

def graph_coloring():
    # Create a CSP problem instance
    problem = Problem()

    # Define the domains for student roll numbers (1 to 30) and colors (blue, red, green)
    roll_numbers = list(range(1, 31))
    colors = ['blue', 'red', 'green']

    # Add variables for each student roll number and their corresponding department color
    for roll_number in roll_numbers:
        problem.addVariable(roll_number, colors)

    # Add constraints to enforce that students from the same department have different colors
    for i in range(1, 31):
        for j in range(i + 1, 31):
            problem.addConstraint(AllDifferentConstraint(), (i, j))

    # Add specific constraints for each department
    for roll_number in range(1, 31):
        if roll_number <= 10:
            problem.addConstraint(lambda color: color == 'blue', (roll_number,))
        elif 11 <= roll_number <= 20:
            problem.addConstraint(lambda color: color == 'red', (roll_number,))
        else:
            problem.addConstraint(lambda color: color == 'green', (roll_number,))

    # Solve the CSP problem
    solutions = problem.getSolutions()

    # Display the results in a grid format
    if not solutions:
        print("No solution found.")
    else:
        print("Graph Coloring Results:")
        for i, solution in enumerate(solutions):
            if i % 10 == 0 and i != 0:
                print("\n")
            roll_number, color = solution.popitem()
            print(f"Roll {roll_number}: {color}", end="\t")

# Run the graph coloring function
graph_coloring()
