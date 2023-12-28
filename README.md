# Ant Colony Optimization

This program uses an ant colony optimization algorithm to optimize solutions to the Traveling Salesman Problem. The algorithm is applied to two data samples contained within the `brazil58.xml` and `burma14.xml` files. These files consist of 58 cities in Brazil and 14 cities in Burma, respectively, and the travel costs between them.

    python3 aco.py

Run the `aco.py` file with the command above to execute the algorithm which upon completion will print: the resulting time of execution, the solution path found between the cities and the total travel cost of the solution. This is done for both the Brazilian and Burmese data samples. This algorithm is initialized with randomized levels of pheromones between cities and updates pheromones once all ants have completed their tours. The algorithm continues until 10000 fitness evaluations have been made or until the `ITERATIONS` parameter has been reached, whichever occurs first.

## Configuration of Parameters

Parameters for the algorithm can be modified at the top of the `aco.py` file, listed as:

    - ALPHA: Trade-off importance of global information (pheromones)
    - BETA: Trade-off importance of local information (heuristics)
    - NUM_ANTS: The total number of ants in the colony
    - ITERATIONS: The total number of iterations permitted
        (the program is however also limited to 10000 fitness evaluations)
    - RHO_EVAPORATION: The evaporation rate of pheromones
    - Q_PARAMETER: The importance of pheromones deposited by ants on their paths

These can be modified here to allow experimentation with different values for each of the parameters.

## Prerequisite packages

The program was written using Python version 3.9.13 and also makes use of the following python packages:

    - numpy
    - networkx
    - matplotlib

Please ensure these packages are installed with the python interpreter used when running the program. This can be done by installing the packages listed in the `requirements.txt` file using:

    pip3 install -r requirements.txt

This program was written by: Johan Schoultz at University of Exeter.
