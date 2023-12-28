import numpy as np
import xml.etree.ElementTree as ET
import random
import datetime
import networkx
import matplotlib.pyplot as plt

# Parameters
ALPHA = 0.5
BETA = 10
NUM_ANTS = 50
ITERATIONS = 10000
RHO_EVAPORATION = 0.1
Q_PARAMETER = 1

# Parse XML file and find all distances between cities
def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    distances = []

    # For each city (vertex), create list of edges to other cities with associated costs
    for city_id, vertex in enumerate(root.findall('.//vertex')):

        edge_costs = [float(edge.attrib['cost']) for edge in vertex.findall('edge[@cost]')]
        edge_costs.insert(city_id, 0)  # Add 0 distance entry for current city
        distances.append(edge_costs)

    return np.array(distances)  # Return distance matrix

# Ant Colony Optimization algorithm
def ant_colony_optimization(distances, num_ants, num_iterations, rho, alpha, beta):
    num_cities = len(distances)

    # Pheromone matrix with random initial values
    # tau_{ij} at t=0
    T = [[ random.random() for j in range(num_cities)] for i in range(num_cities)]

    # Number of fitness evaluations
    fitness_evaluations = 0

    # Repeat through algorithm 'num_iterations' times
    for t in range(num_iterations):

        current_cities = []  # current_city[k] is the city that ant k is currently in
        paths = []  # List of solutions generated by ants
        best_path = []
        best_distance = None
    
        for k in range(num_ants):
            current_cities.append(0)  # Each ant starts in city 0
            paths.append([0])  # Each path will start from city 0
    
        # For each ant, build a solution
        for k in range(num_ants):

            # Heuristic matrix
            # eta_{ij} = 1/d_{ij}
            H = [[ 1/distances[i][j] if i != j else 0 for j in range(num_cities)] for i in range(num_cities)]
                    
            # Repeat until an ant has visited all cities
            while( len( paths[k]) < num_cities ):

                # Set column for current city ant is in to 0 to exclude city
                for row in H:
                    row[ current_cities[k] ] = 0

                # Obtain probabilities for ant traversing each edge from the current city
                probabilities = calculate_probability(T, H, current_cities[k], alpha, beta)

                # Calculate next city ant goes to
                next_city = find_next_city(probabilities)
                paths[k].append(next_city)
                current_cities[k] = next_city

            # Return to start city
            paths[k].append(0)

        # Update pheromones and best path based on ant paths
        T, best_path, best_distance = update_pheromones(T, best_path, best_distance, rho, distances, paths)
        fitness_evaluations += num_ants  # One fitness evaluation is made per ant

        # Check if the desired number of fitness evaluations is reached
        if fitness_evaluations >= 10000:
            print('Fitness evaluations limit reached:', fitness_evaluations)
            return best_path, best_distance  # Terminate the algorithm

    return best_path, best_distance  # Return best path found and its total distance

# Calculate probability of ant traversing each edge from a city
def calculate_probability(T, H, current_city, alpha, beta):
    num_cities = len(T)

    # Calculate numerators in probability matrix
    probabilities = [ (T[current_city][i] ** alpha) * (H[current_city][i] ** beta) for i in range(num_cities) ]

    # Divide each entry by total sum to get probabilities
    total = sum(probabilities)
    for i in range(len(probabilities)):
        probabilities[i] /= total if total != 0 else 1.0

    return probabilities  # Return probabilities

# Find next city an ant goes to from a probability matrix
def find_next_city(probabilities):
    num_cities = len(probabilities)

    # Calculate next city
    rand = random.random()
    cumulative_prob = 0
    for city in range(num_cities):

        # Cumulative probability of ant going from current city to each possible next city
        cumulative_prob += probabilities[city]
        if cumulative_prob >= rand:
            return city  # Return first city that passes probability threshold

# Update pheromone matrix with decay and deposits, and update best path found
def update_pheromones(T, best_path, best_distance, rho, distance_matrix, paths):
    num_cities = len(T)
    new_best_distance = best_distance
    new_best_path = best_path

    # Pheromone decay
    T = [[ (1-rho) * T[i][j] for j in range(num_cities)] for i in range(num_cities)]

    # Pheromone deposits
    for path in paths:
        length = 0
        for i in range(1, num_cities):
            length += distance_matrix[ path[i-1] ][ path[i] ]  # Combine cost of each step in path
        for i in range(1, num_cities):
            T[ path[i-1] ][ path[i] ] += Q_PARAMETER / length

        # Check if path is better than current best
        if best_distance == None or length < new_best_distance:
            new_best_path = path
            new_best_distance = length

    return T, new_best_path, new_best_distance  # Return updated pheromone matrix

# Visualisation of a distance matrix as a graph
def visualise_graph(distances):
    d = np.array(distances)
    graph = networkx.from_numpy_array(d)
    networkx.draw(graph, with_labels=True)
    plt.show()

if __name__ == '__main__':

    # Load distance matrices from XML files
    burmese_distances = parse_xml('burma14.xml')
    brazilian_distances = parse_xml('brazil58.xml')

    # Visualise graph of nodes and edges between cities
    #visualise_graph(burmese_distances)
    #visualise_graph(brazilian_distances)

    # Apply ACO algorithm to Burmese data
    start = datetime.datetime.now()
    burmese_best_route, burmese_distance = ant_colony_optimization(burmese_distances, NUM_ANTS, ITERATIONS, RHO_EVAPORATION, ALPHA, BETA)
    end = datetime.datetime.now()

    print('Burmese execution time', end - start)
    print("Burmese Best Route:", burmese_best_route)
    print("Burmese Total Cost:", burmese_distance)

    # Apply ACO algorithm to Brazilian data
    start = datetime.datetime.now()
    brazilian_best_route, brazilian_distance = ant_colony_optimization(brazilian_distances, NUM_ANTS, ITERATIONS, RHO_EVAPORATION, ALPHA, BETA)
    end = datetime.datetime.now()

    print('Brazilian execution time', end - start)
    print("Brazilian Best Route:", brazilian_best_route)
    print("Brazilian Total Cost:", brazilian_distance)