from collections import defaultdict
from copy import deepcopy
from heapq import heappush, heappop


class Graph:
    def __init__(self, edges=None):
        self.node_edges = defaultdict(dict)
        if edges is not None:
            self.add_edges(edges)
    
    def add_edge(self, edge):
        if len(edge) == 3:
            first, second, cost = edge
        elif len(edge) == 2:
            first, second = edge
            cost = 1
        self.node_edges[first][second] = cost
        self.node_edges[second][first] = cost
    
    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(edge)
    
    def add_node(self, node):
        if node not in self.node_edges:
            self.node_edges[node] = {}
    
    def nodes(self):
        return self.node_edges.keys()
    
    def edges(self, node):
        return self.node_edges[node].items()


class Path:
    def __init__(self, start):
        self.nodes = [start]
        self.cost = 0
        
        # processing cost to find this solution
        self.iterations = 0
    
    def add(self, step):
        node, cost = step
        self.nodes.append(node)
        self.cost += cost
    
    @property
    def end(self):
        return self.nodes[-1]
    
    @property
    def length(self):
        return len(self.nodes)
    
    def __str__(self):
        return ' -> '.join(self.nodes)  + " (cost:%d, length:%d)" % (self.cost, self.length)


class GraphSearcher:
    def _add_frontier(self, path):
        self.frontier[path.end] = path
        self._add_path(path)
    
    def _add_path(self, path):
        self.paths.append(path)
    
    def _already_in_frontier(self, new_path, adjacent):
        pass
    
    def _get_path(self):
        raise Exception("GraphSearcher is an abstract class, use one of its implementations instead")
    
    def search(self, graph, start, goal, heuristic=None, debug=False):
        self.goal = goal
        self.heuristic = heuristic
        
        self.paths = []
        self.frontier = {}
        self._add_frontier(Path(start))
        
        explored = set([])
        iterations = 0
        while True:
            iterations += 1
            path = self._get_path()
            if path is None: return None
            if debug: print path
            
            s = path.end
            explored.add(s)
            del self.frontier[s]
            if s == goal:
                path.iterations = iterations
                return path
            
            for edge in graph.edges(s):
                new_node = edge[0]
                if new_node in explored: continue
                
                new_path = deepcopy(path)
                new_path.add(edge)
                
                if new_node in self.frontier:
                    self._already_in_frontier(new_path, new_node)
                else:
                    self._add_frontier(new_path)


class BreadthFirstSearcher(GraphSearcher):
    def _get_path(self):
        return self.paths.pop(0)


class DepthFirstSearcher(GraphSearcher):
    def _get_path(self):
        return self.paths.pop()


class UniformCostSearcher(GraphSearcher):
    def _add_path(self, path):
        heappush(self.paths, (self._path_cost(path), path))
    
    def _get_path(self):
        return heappop(self.paths)[1] # (0:cost, 1:path)
    
    def _path_cost(self, path):
        return path.cost
    
    def _already_in_frontier(self, new_path, adjacent):
        if self._path_cost(new_path) < self._path_cost(self.frontier[adjacent]):
            del self.frontier[adjacent]
            self._add_frontier(new_path)


class AStarSearcher(UniformCostSearcher):
    def _path_cost(self, path):
        return path.cost + self.heuristic(path.end, self.goal)


def breadth_first_search(graph, start, end):
    return BreadthFirstSearcher().search(graph, start, end)


def depth_first_search(graph, start, end):
    return DepthFirstSearcher().search(graph, start, end)


def uniform_cost_search(graph, start, end):
    return UniformCostSearcher().search(graph, start, end)


def a_star_search(graph, start, end, heuristic):
    return AStarSearcher().search(graph, start, end, heuristic)

