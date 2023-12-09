import random

# Define your seat data (you can customize this based on your venue)
seat_data = [
    {"seat_id": 1, "category": "A", "price": 100, "proximity": "near"},
    {"seat_id": 2, "category": "A", "price": 100, "proximity": "near"},
    {"seat_id": 3, "category": "B", "price": 80, "proximity": "near"},
    {"seat_id": 4, "category": "B", "price": 80, "proximity": "far"},
    # Add more seat information...
]

# Define user preferences (customize this based on user input)
user_preferences = [
    {"preference_type": "category", "preferred_categories": ["A"]},
    {"preference_type": "price", "max_price": 90},
    {"preference_type": "proximity", "preferred_proximity": "near"},
    # Add more user preferences...
]

# Define your seat representation (a chromosome)
def generate_random_seat_allocation(seat_data):
    return [random.choice(seat_data) for _ in range(len(seat_data))]

# Define the fitness function
def fitness(seat_allocation, user_preferences):
    # Calculate the fitness score based on how well the seat allocation matches user preferences
    score = 0
    for seat, preference in zip(seat_allocation, user_preferences):
        if seat == preference:
            score += 1
    return score

# Define tournament selection (updated to accept user_preferences)
def tournament_selection(population, fitness_func, tournament_size, user_preferences):
    tournament = random.sample(population, tournament_size)
    return max(tournament, key=lambda x: fitness_func(x, user_preferences))
# Define crossover (single-point crossover)
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2
# Define mutation
def mutate(seat_allocation, mutation_rate):
    mutated_allocation = seat_allocation.copy()
    for i in range(len(seat_allocation)):
        if random.random() < mutation_rate:
            mutated_allocation[i] = random.choice(seat_data)  # You should have seat_data defined in your code
    return mutated_allocation


# Genetic algorithm parameters
population_size = 100
num_generations = 100
mutation_rate = 0.1
tournament_size = 5

# Generate initial population
population = [generate_random_seat_allocation(seat_data) for _ in range(population_size)]

# Main loop
for generation in range(num_generations):
    # Evaluate the fitness of each seat allocation in the population
    fitness_scores = [fitness(seat_allocation, user_preferences) for seat_allocation in population]

    # Select parents for the next generation using tournament selection
    parents = [tournament_selection(population, fitness, tournament_size, user_preferences) for _ in range(population_size)]

    # Create a new population through crossover and mutation
    new_population = []
    for i in range(0, population_size, 2):
        parent1, parent2 = parents[i], parents[i + 1]
        child1, child2 = crossover(parent1, parent2)
        child1 = mutate(child1, mutation_rate)
        child2 = mutate(child2, mutation_rate)
        new_population.extend([child1, child2])

    # Replace the old population with the new population
    population = new_population

# Select the best seat allocation from the final population
best_seat_allocation = max(population, key=lambda x: fitness(x, user_preferences))

print("Best Seat Allocation:", best_seat_allocation)
