from collections import defaultdict
from copy import deepcopy
from heapq import heappush, heappop


class Path:
    def __init__(self, start):
        self.nodes = [start]
        self.cost = 0
        self.length = 0
    
    def add(self, step):
        node, cost = step
        self.nodes.append(node)
        self.cost += cost
        self.length += 1
    
    @property
    def end(self):
        return self.nodes[-1]
    
    def __str__(self):
        return ' -> '.join(self.nodes)  + " (cost:%d, length:%d)" % (self.cost, self.length)


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


class GraphSearch:
    def __init__(self, graph,  heuristic=None):
        self.graph = graph
        self.heuristic = heuristic
    
    def _add_frontier(self, path):
        self.frontier[path.end] = path
        self._add_path(path)
    
    def _add_path(self, path):
        self.paths.append(path)
    
    def _already_in_frontier(self, new_path, adjacent):
        pass
    
    def _get_path(self):
        raise Exception("GraphSearch is an abstract class, use one of its implementations instead")
    
    def search(self, start, goal, debug=False):
        self.paths = []
        self.frontier = {}
        self.goal = goal
        self._add_frontier(Path(start))
        
        explored = set([])
        self.iterations = 0
        while True:
            self.iterations += 1
            path = self._get_path()
            if path is None: return None
            if debug: print path
            
            s = path.end
            explored.add(s)
            del self.frontier[s]
            if s == goal:
                return path
            
            for edge in self.graph.edges(s):
                new_node = edge[0]
                if new_node in explored: continue
                
                new_path = deepcopy(path)
                new_path.add(edge)
                
                if new_node in self.frontier:
                    self._already_in_frontier(new_path, new_node)
                else:
                    self._add_frontier(new_path)


class BreadthFirstSearch(GraphSearch):
    def _get_path(self):
        return self.paths.pop(0)


class DepthFirstSearch(GraphSearch):
    def _get_path(self):
        return self.paths.pop()


class UniformCostSearch(GraphSearch):
    def _add_path(self, path):
        heappush(self.paths, (self._path_cost(path), path))
    
    def _get_path(self):
        return heappop(self.paths)[1]
    
    def _path_cost(self, path):
        return path.cost
    
    def _already_in_frontier(self, new_path, adjacent):
        if self._path_cost(new_path) < self._path_cost(self.frontier[adjacent]):
            del self.frontier[adjacent]
            self._add_frontier(new_path)


class AStarSearch(UniformCostSearch):
    def _path_cost(self, path):
        return path.cost + self.heuristic(path.end, self.goal)

