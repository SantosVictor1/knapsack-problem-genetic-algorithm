import random
import re
import time

POPULATION_SIZE = 150
GENERATIONS = 400
MUTATION_RATE = 0.01

def fitness(chromosome, items, max_weight):
    total_value = 0
    total_weight = 0

    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            total_value += items[i][1]
            total_weight += items[i][2]

    if total_weight > max_weight:
        return 0
    
    return total_value

def generate_population(size, num_items):
    population = []

    for _ in range(size):
        chromosome = [0] * num_items

        num_ones = num_items // 64
        indices_to_flip = random.sample(range(num_items), num_ones)
        for index in indices_to_flip:
            chromosome[index] = 1

        population.append(chromosome)

    return population

def select_parents(population, num_parents, items, max_weight):
    parents = []

    for _ in range(num_parents):
        parents.append(max(population, key=lambda chromosome: fitness(chromosome, items, max_weight)))
        population.remove(parents[-1])
    return parents

def crossover(parent_a, parent_b):
    crossover_point = random.randint(0, len(parent_a) - 1)

    offspring_a = parent_a[:crossover_point] + parent_b[crossover_point:]
    offspring_b = parent_b[:crossover_point] + parent_a[crossover_point:]

    return offspring_a, offspring_b

def mutate(offspring):
    for i in range(len(offspring)):
        if MUTATION_RATE > random.random():
            offspring[i] = 1 - offspring[i]

    return offspring

def genetic_algorithm(population, items, max_weight, num_parents):
    old_fitness = 0

    for generation in range(GENERATIONS):
        parents = select_parents(population, num_parents, items, max_weight)
        offspring = []
        if (num_parents % 2) != 0:
            num_parents -= 1

        for i in range(0, num_parents, 2):
            parent_a = parents[i]
            parent_b = parents[i + 1]
            offspring_a, offspring_b = crossover(parent_a, parent_b)
            offspring_a = mutate(offspring_a)
            offspring_b = mutate(offspring_b)
            offspring.extend([offspring_a, offspring_b])

        population = parents + offspring

        best_solution = max(population, key=lambda chromosome: fitness(chromosome, items, max_weight))
        best_fitness = fitness(best_solution, items, max_weight)

        if best_fitness != old_fitness:
            old_fitness = best_fitness
            print(f"Generation {generation + 1}: Best Fitness = {best_fitness}")

    best_solution = max(population, key=lambda chromosome: fitness(chromosome, items, max_weight))
    best_fitness = fitness(best_solution, items, max_weight)
    
    return best_solution, best_fitness

def main():
    for instance in range(1, 17):
        items = list()
        input_file_path = f"input/input{instance}.in"
        
        with open(input_file_path, "r") as file:
            lines = file.readlines()
        
        max_weight = int(lines[-1].strip())

        for line in lines[1:-1]:
            values = re.findall(r"[0-9]+", line)
            items.append(list(map(int, values)))

        print(f"\nArquivo {instance}")

        population = generate_population(POPULATION_SIZE, len(items))

        best_solution, best_fitness = genetic_algorithm(population, items, max_weight, int(POPULATION_SIZE / 2))

        if best_fitness > 0:
            print("\nMelhor solução encontrada:")
            print("Itens selecionados:")
            for i, bit in enumerate(best_solution):
                if bit == 1:
                    print(f"Item {items[i][0]}: Peso = {items[i][2]}, Valor = {items[i][1]}")
            print(f"Valor Total = {best_fitness}")
        else:
            print("\nNão foi possível encontrar o melhor resultado")
        
        with open("output/genetic.out", "a") as output_file:
            output_file.write(f"Instancia {instance} : {best_fitness}\n")

if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    print(f"Execution time: {execution_time} seconds")