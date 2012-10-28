# Examples taken from the course "Introduction to Artificial Intelligence", Sebastian Thrun and Peter Norvig:
#    https://www.ai-class.com
from algorithms.graphs import Graph, breadth_first_search, depth_first_search, uniform_cost_search, a_star_search

ROMANIA_GRAPH = Graph([
    ("Arad", "Sibiu", 140),
    ("Arad", "Zerind", 75),
    ("Arad", "Timisoara", 118),
    ("Sibiu", "Fagaras", 99),
    ("Sibiu", "Rimnicu Vilcea", 80),
    ("Rimnicu Vilcea", "Craiova", 146),
    ("Rimnicu Vilcea", "Pitesti", 97),
    ("Pitesti", "Bucharest", 101),
    ("Drobeta", "Craiova", 120),
    ("Zerind", "Oradea", 71),
    ("Oradea", "Sibiu", 151),
    ("Timisoara", "Lugoj", 111),
    ("Lugoj", "Mehadia", 70),
    ("Mehadia", "Drobeta", 75),
    ("Craiova", "Pitesti", 138),
    ("Fagaras", "Bucharest", 211),
    ("Bucharest", "Giurgiu", 90),
    ("Bucharest", "Urziceni", 85),
])

ROMANIA_DISTANCES_FROM_BUCHAREST = {
    "Arad": 336,
    "Bucharest": 0,
    "Craiova": 160,
    "Drobeta": 242,
    "Fagaras": 176,
    "Giurgiu": 77,
    "Lugoj": 244,
    "Mehadia": 241,
    "Oradea": 380,
    "Pitesti": 100,
    "Rimnicu Vilcea": 193,
    "Sibiu": 253,
    "Timisoara": 329,
    "Urziceni": 80,
    "Zerind": 374,
}

def distance_heuristic(start_node, end_node):
    assert end_node == "Bucharest"
    return ROMANIA_DISTANCES_FROM_BUCHAREST[start_node]


def test_breadth_first_search():
    path = breadth_first_search(ROMANIA_GRAPH, "Arad", "Bucharest")
    assert path.nodes == ["Arad", "Sibiu", "Fagaras", "Bucharest"]
    assert path.cost == 450
    assert path.iterations == 10
    print path

def test_depth_first_search():
    path = depth_first_search(ROMANIA_GRAPH, "Arad", "Bucharest")
    assert path.nodes == ['Arad', 'Sibiu', 'Rimnicu Vilcea', 'Pitesti', 'Bucharest']
    assert path.cost == 418
    assert path.iterations == 5
    print path

def test_uniform_cost_search():
    path = uniform_cost_search(ROMANIA_GRAPH, "Arad", "Bucharest")
    assert path.nodes == ["Arad", "Sibiu", "Rimnicu Vilcea", "Pitesti", "Bucharest"]
    assert path.cost == 418
    assert path.iterations == 13
    print path

def test_a_star_search():
    path = a_star_search(ROMANIA_GRAPH, "Arad", "Bucharest", distance_heuristic)
    assert path.nodes == ["Arad", "Sibiu", "Rimnicu Vilcea", "Pitesti", "Bucharest"]
    assert path.cost == 418
    assert path.iterations == 6
    print path


if __name__ == "__main__":
    test_breadth_first_search()
    test_depth_first_search()
    test_uniform_cost_search()
    test_a_star_search()
