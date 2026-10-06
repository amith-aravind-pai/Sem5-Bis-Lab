import random
import math 

N = 50
ITER = 500
W=0.5
C1 = 0.8
C2 = 0.9

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

def get_swap_sequence(source_route, target_route):
    temp_route = source_route.copy()
    swap_sequence = []

    for i in range(len(temp_route)):
        if temp_route[i] != target_route[i]:
            target_city = target_route[i]  
            j = temp_route.index(target_city)
            temp_route[i], temp_route[j] = temp_route[j], temp_route[i]
            swap_sequence.append((i, j))

    return swap_sequence

class Particle:
    def __init__(self, num_cities):
        base_cities = list(range(num_cities))
        self.route = random.sample(base_cities, num_cities)
        
        self.velocity = []
        self.pbest_route = self.route.copy()
        self.pbest_distance = float('inf')

    def update_velocity(self, gbest_route):
        new_velocity = []
        
        for swap in self.velocity:
            if random.random() < W:
                new_velocity.append(swap)
                
        pbest_swaps = get_swap_sequence(self.route, self.pbest_route)
        for swap in pbest_swaps:
            if random.random() < C1:
                new_velocity.append(swap)
                
        gbest_swaps = get_swap_sequence(self.route, gbest_route)
        for swap in gbest_swaps:
            if random.random() < C2:
                new_velocity.append(swap)
                
        self.velocity = new_velocity

    def apply_velocity(self):
        for i, j in self.velocity:
            self.route[i], self.route[j] = self.route[j], self.route[i]


def run_pso(cities):
    dist_matrix = build_distance_matrix(cities)
    num_cities = len(cities)
    
    swarm = [Particle(num_cities) for _ in range(N)]
    gbest_route = None
    gbest_distance = float('inf')

    for iteration in range(ITER):
        for particle in swarm:
            dist = calculate_route_distance(particle.route, dist_matrix)
            
            if dist < particle.pbest_distance:
                particle.pbest_distance = dist
                particle.pbest_route = particle.route.copy()
                
            if dist < gbest_distance:
                gbest_distance = dist
                gbest_route = particle.route.copy()
                
        for particle in swarm:
            particle.update_velocity(gbest_route)
            particle.apply_velocity()
            
    return gbest_route, gbest_distance



city_coordinates = generate_random_cities(20)
best_route, shortest_distance = run_pso(city_coordinates)

print(f"Shortest Distance Found: {shortest_distance}")
print(f"Optimal Route: {best_route}")