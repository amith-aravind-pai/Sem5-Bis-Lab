import random

class AntNetRouting:
    def __init__(self, nodes, edges, source, destination, num_ants=20, num_iterations=100, decay=0.1, alpha=1.0, beta=2.0):
        self.nodes = nodes
        self.edges = edges 
        self.adj_list = {node: [] for node in nodes}
        for (u, v), cost in edges.items():
            self.adj_list[u].append(v)
            self.adj_list[v].append(u)
            
        self.source = source
        self.destination = destination
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        
        self.pheromones = { (u, v): 1.0 for (u, v) in edges.keys() }
        for (u, v) in list(edges.keys()):
            self.pheromones[(v, u)] = 1.0
            
        self.get_cost = lambda u, v: self.edges.get((u, v)) or self.edges.get((v, u))

    def run(self):
        best_path = None
        best_cost = float('inf')

        for _ in range(self.num_iterations):
            all_paths = self._send_ants()
            self._update_pheromones(all_paths)
            
            for path, cost in all_paths:
                if cost < best_cost:
                    best_cost = cost
                    best_path = path
                    
        return best_path, best_cost

    def _send_ants(self):
        all_paths = []
        for _ in range(self.num_ants):
            path = self._route_single_ant()
            if path: 
                cost = self._calculate_path_cost(path)
                all_paths.append((path, cost))
        return all_paths

    def _route_single_ant(self):
        path = [self.source]
        visited = set([self.source])
        current_node = self.source
        
        while current_node != self.destination:
            next_hop = self._select_next_hop(current_node, visited)
            if not next_hop:
                return None 
            path.append(next_hop)
            visited.add(next_hop)
            current_node = next_hop
            
        return path

    def _select_next_hop(self, current_node, visited):
        neighbors = [n for n in self.adj_list[current_node] if n not in visited]
        if not neighbors:
            return None
            
        probabilities = []
        total_prob = 0.0
        
        for neighbor in neighbors:
            pheromone = self.pheromones[(current_node, neighbor)] ** self.alpha
            heuristic = (1.0 / self.get_cost(current_node, neighbor)) ** self.beta
            prob = pheromone * heuristic
            probabilities.append((neighbor, prob))
            total_prob += prob
            
        if total_prob == 0:
            return random.choice(neighbors)
            
        threshold = random.uniform(0, total_prob)
        cumulative_prob = 0.0
        for neighbor, prob in probabilities:
            cumulative_prob += prob
            if cumulative_prob >= threshold:
                return neighbor
                
        return probabilities[-1][0]

    def _update_pheromones(self, all_paths):
        for link in self.pheromones:
            self.pheromones[link] *= (1.0 - self.decay)
            self.pheromones[link] = max(0.0001, self.pheromones[link])
            
        for path, cost in all_paths:
            pheromone_contribution = 100.0 / cost
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                self.pheromones[(u, v)] += pheromone_contribution
                self.pheromones[(v, u)] += pheromone_contribution

    def _calculate_path_cost(self, path):
        return sum(self.get_cost(path[i], path[i+1]) for i in range(len(path) - 1))

if __name__ == "__main__":
    nodes = ['Router_A', 'Router_B', 'Router_C', 'Router_D', 'Router_E', 'Router_F', 'Router_G']
    edges = {
        ('Router_A', 'Router_B'): 10, ('Router_A', 'Router_C'): 15,
        ('Router_B', 'Router_D'): 12, ('Router_C', 'Router_D'): 5,
        ('Router_C', 'Router_E'): 20, ('Router_D', 'Router_F'): 10,
        ('Router_E', 'Router_G'): 8,  ('Router_F', 'Router_G'): 15,
        ('Router_B', 'Router_E'): 25
    }

    ant_net = AntNetRouting(nodes, edges, source='Router_A', destination='Router_G', num_ants=10, num_iterations=50)
    best_route, lowest_delay = ant_net.run()
    
    print(f"Optimal Routing Path: {' -> '.join(best_route)}")
    print(f"Total Network Delay: {lowest_delay} ms")