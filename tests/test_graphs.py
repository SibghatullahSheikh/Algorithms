from algorithms.graphs import Graph, BreadthFirstSearch, DepthFirstSearch, UniformCostSearch, AStarSearch

ROMANIA_ROAD_MAP = [
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
]

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

class TestGraph:
    def __init__(self):
        self.graph = Graph(ROMANIA_ROAD_MAP)
    
    def test_BreadthFirstSearch(self):
        algorithm = BreadthFirstSearch(self.graph)
        path = algorithm.search("Arad", "Bucharest")
        assert path.nodes == ["Arad", "Sibiu", "Fagaras", "Bucharest"]
        assert algorithm.iterations == 10
    
    def test_DepthFirstSearch(self):
        algorithm = DepthFirstSearch(self.graph)
        path = algorithm.search("Arad", "Bucharest")
        assert path.nodes == ['Arad', 'Sibiu', 'Rimnicu Vilcea', 'Pitesti', 'Bucharest']
        assert algorithm.iterations == 5
    
    def test_UniformCostSearch(self):
        algorithm = UniformCostSearch(self.graph)
        path = algorithm.search("Arad", "Bucharest")
        assert path.nodes == ["Arad", "Sibiu", "Rimnicu Vilcea", "Pitesti", "Bucharest"]
        assert algorithm.iterations == 13
    
    def test_AStarSearch(self):
        algorithm = AStarSearch(self.graph, distance_heuristic)
        path = algorithm.search("Arad", "Bucharest")
        assert path.nodes == ["Arad", "Sibiu", "Rimnicu Vilcea", "Pitesti", "Bucharest"]
        assert algorithm.iterations == 6
