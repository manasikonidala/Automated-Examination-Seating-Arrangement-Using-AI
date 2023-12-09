from constraint import Problem, AllDifferentConstraint

def load_classroom_details(classroom_id):
    # Fetch classroom details from the database based on classroom_id
    # Replace this with your actual database query
    # For example:
    # cursor.execute("SELECT BENCH_COUNT, CLASSROOM_CAPACITY FROM CLASSROOM WHERE CLASSROOM_ID = ?;", (classroom_id,))
    # bench_count, classroom_capacity = cursor.fetchone()
    # return bench_count, classroom_capacity
    return 20, 40  # Replace with the actual values fetched from the database

def classroom_constraint(*students):
    # Constraint: No two students from the same department should sit in the same bench
    departments = [student[1][:4] for student in students]
    for i in range(len(students) - 1):
        if departments[i] == departments[i + 1]:
            return False

    # Constraint: If a student is allocated, the adjacent seat in the same bench
    # should not be allocated to a student from the same department.
    for i in range(len(students) - 1):
        if abs(students[i][0] - students[i + 1][0]) == 1 and departments[i] == departments[i + 1]:
            return False

    return True

def seating_arrangement_csp(roll_number_range_cse, roll_number_range_it, roll_number_range_ece, classroom_id):
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
    problem.addConstraint(AllDifferentConstraint(), roll_number_range_cse + roll_number_range_it + roll_number_range_ece)
    problem.addConstraint(classroom_constraint, roll_number_range_cse + roll_number_range_it + roll_number_range_ece)

    # Solve the CSP
    solutions = problem.getSolutions()

    # Fill remaining seats with one student from the ECE department in each bench
    remaining_students_ece = roll_number_range_ece[len(solutions):]
    for i, bench in enumerate(range(bench_count * 2 + 1, (bench_count + 1) * 2 + 1, 2)):
        if i < len(remaining_students_ece):
            solutions.append((remaining_students_ece[i], bench))
        else:
            break

    return solutions, bench_count, classroom_capacity

def display_seating_arrangement(solution, bench_count):
    # Display seating arrangement in a matrix format
    seating_matrix = [['Empty Seat'] * 2 for _ in range(bench_count)]

    for i, seating_info in enumerate(solution, start=1):
        if isinstance(seating_info, tuple) and len(seating_info) == 2:
            roll_number, seat = seating_info
            bench_number = (i - 1) // 2
            seat_index = (i - 1) % 2
            seating_matrix[bench_number][seat_index] = roll_number

    # Print the seating matrix
    print("Seating Arrangement:")
    for bench_number, seats in enumerate(seating_matrix, start=1):
        print(f"Bench {bench_number}: Seat 1: {seats[0]}, Seat 2: {seats[1]}")

# Example usage
roll_number_range_cse = [f"3122215001{i}" for i in range(101, 111)]  # Replace with your actual CSE department range
roll_number_range_it = [f"3122215002{i}" for i in range(50, 61)]  # Replace with your actual IT department range
roll_number_range_ece = [f"3122215003{i}" for i in range(30, 40)]  # Replace with your actual ECE department range
classroom_id = 'ITA'

solutions, bench_count, classroom_capacity = seating_arrangement_csp(roll_number_range_cse, roll_number_range_it, roll_number_range_ece, classroom_id)
if solutions:
    print("Seating Arrangement:")
    for solution in solutions:
        try:
            display_seating_arrangement(solution, bench_count)
        except ValueError as e:
            print(f"Error displaying seating arrangement: {e}")
    print(f"\nTotal Students Accommodated: {classroom_capacity}")
    empty_seats = bench_count * 2 - len(solutions)
    print(f"Total Empty Seats: {empty_seats}")
else:
    print("No valid seating arrangement found.")

# Display unallocated students
unallocated_students = roll_number_range_ece[len(solutions):]
print("\nUnallocated Students:")
for student in unallocated_students:
    print(student)
