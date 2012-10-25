from numpy import array, mean
from numpy.linalg import norm


class Item:
    def __init__(self, name, values):
        self.name = name
        self.values = array(values)
    
    def distance(self, other):
        return norm(self.values - other.values)
    
    def __cmp__(self, other):
        return cmp(norm(self.values), norm(other.values))
    
    def __str__(self):
        return "(%s: %s)" % (self.name, self.values)


class Group(Item):
    def __init__(self, items):
        self.items = items
        self.values = mean(array([i.values for i in self.items]), axis=0)
        self.name = None
    
    def __str__(self):
        self.items.sort(reverse=True)
        name = "%s: " % self.name if self.name is not None else ''
        return "%s[%s]" % (name, ', '.join([i.name for i in self.items]))


def pop_items(l, indexes):
    indexes.sort(reverse=True)
    return [l.pop(index) for index in indexes]


def find_clusters(items, clusters_names):
    # Initially create a group for each item
    groups = [Group([item]) for item in items]
    
    # Iterate until the number of groups match the desired number of clusters
    num_clusters = len(clusters_names)
    while len(groups) > num_clusters:
        
        # Find the closest pair of groups
        closest_pair, shortest_distance = None, None
        for a in range(len(groups)):
            for b in range(a+1, len(groups)):
                
                # Calculate distance
                distance = groups[a].distance(groups[b])
                
                # Keep shortest distance
                if shortest_distance is None or distance < shortest_distance:
                    shortest_distance = distance
                    closest_pair = [a, b]
        
        # Merge the closest pair of groups
        a, b = pop_items(groups, closest_pair)
        groups.append(Group(a.items + b.items))
    
    groups.sort(reverse=True)
    for group, cluster_name in zip(groups, clusters_names):
        group.name = cluster_name
    
    return groups
