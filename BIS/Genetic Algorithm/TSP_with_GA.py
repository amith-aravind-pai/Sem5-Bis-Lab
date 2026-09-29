import random
import math
from collections import deque

POPULATION_SIZE = 100
MUTATION_RATE = 0.05
GENERATIONS = 500
TOURNAMENT_SIZE = 4

def generate_random_cities(num_cities):
    city_coords = []
    for i in range(num_cities):
        city_coords.append((random.randint(0,100),random.randint(0,100)))
    return city_coords

def build_distance_matrix(cities):
    dis_matrix = []
    total_distance = 0 
    for i in range(len(cities)):
        temp = []
        for j in range(len(cities)):
            temp.append(0);
        dis_matrix.append(temp)

    for i in range(len(cities)):
        for j in range(len(cities)):
            dis = abs(math.dist(cities[i],cities[j]))
            dis_matrix[i][j] = dis

    return dis_matrix
        
def calculate_route_distance(route, dist_matrix):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += dist_matrix[route[i]][route[i+1]]
    total_distance += dist_matrix[route[-1]][route[0]]
    return total_distance

def create_initial_population(num_cities, pop_size):
    base_cities = [i for i in range(num_cities)]
    initial_pop = []
    for i in range(pop_size):
        initial_pop.append(random.sample(base_cities,num_cities))
    return initial_pop  


def tournament_selection(population, dist_matrix):
    selected_routes = random.sample(population,TOURNAMENT_SIZE)
    min_route = None
    min_route_dist = 0

    for i in range(TOURNAMENT_SIZE):
        dist = calculate_route_distance(selected_routes[i], dist_matrix)
        if min_route is None or dist < min_route_dist:
            min_route_dist = dist 
            min_route = selected_routes[i]

    return min_route

def ordered_crossover(parent1, parent2):
    child = [-1 for i in range(len(parent1))]
    start = random.randint(0,len(child)-1)
    end = random.randint(0,len(child)-1)
    if start > end : start,end = end,start
    p1_cross = parent1[start:end]
    child[start:end] = p1_cross

    p2_cross = deque()
    p1_set = set(p1_cross)

    for i in range(len(parent2)):
        if parent2[i] not in p1_set:
            p2_cross.append(parent2[i])

    for i in range(len(child)):
        if child[i] == -1:
            child[i] = p2_cross.popleft()

    return child


def mutate(route):
    for i in range(len(route)):
        if random.random() < MUTATION_RATE:
            swap_ind = random.randint(0,len(route) - 1)
            route[swap_ind], route[i] = route[i] , route[swap_ind] 

def run_evolution(cities):
    dist_matrix = build_distance_matrix(cities)
    num_cities = len(cities)
    
    population = create_initial_population(num_cities, POPULATION_SIZE)
    
    best_overall_route = None
    best_overall_distance = float('inf')

    for _ in range(GENERATIONS):
        new_population = []
        
        while len(new_population) < POPULATION_SIZE:
            parent1 = tournament_selection(population, dist_matrix)
            parent2 = tournament_selection(population, dist_matrix)
            
            child = ordered_crossover(parent1, parent2)
            mutate(child)
            
            new_population.append(child)
            
        population = new_population
        
        for route in population:
            dist = calculate_route_distance(route,dist_matrix)
            if best_overall_route is None or best_overall_distance > dist:
                best_overall_distance = dist
                best_overall_route = route.copy()
        
    return best_overall_route, best_overall_distance

if __name__ == "__main__":
    city_coordinates = generate_random_cities(20)
    
    best_route, shortest_distance = run_evolution(city_coordinates)
    
    print(f"Shortest Distance Found: {shortest_distance}")
    print(f"Optimal Route: {best_route}")