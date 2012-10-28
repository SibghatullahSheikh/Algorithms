from algorithms.clusters.hierarchical import Item, find_clusters


def test_3D_hierarchical_clusters():
    # Simple three dimensional test
    cluster_1 = ('c1',  0,  0,  0)
    cluster_2 = ('c2', 10, 10, 10)
    
    # Create a set of 54 3D items positioned in two separate clusters
    SCATTER = (-1, 0, 1)
    items = []
    for i in SCATTER:
        for j in SCATTER:
            for k in SCATTER:
                for c_name, c_x, c_y, c_z in (cluster_1, cluster_2):
                    name = '%s_(%d,%d,%d)' % (c_name, i, j, k)
                    x, y, z = (c_x + i), (c_y + j), (c_z + k)
                    items.append(Item(name, (x, y, z)))
    
    n_items = len(items)
    clusters = find_clusters(items, ("c1", "c2"))
    
    # We did not loose, or add any item
    c_items = sum(map(len, [c.items for c in clusters]))
    assert n_items == c_items, "Error n items: %d" % (n_items - c_items)
    
    # Items belongs to the correct cluster
    for c in clusters:
        name = c.items[0].name[:2]
        for i in c.items:
            assert i.name.startswith(name), 'Error: "%s" != "%s"' % (i.name[:2], name) 


LANGUAGES_POPULARITY = (
    ("C", 100.00),
    ("JavaScript", 99.99),
    ("Java", 99.28),
    ("C++", 86.06),
    ("Python", 67.50),
    ("PHP", 52.69),
    ("Perl", 35.29),
    ("Ruby", 35.20),
    ("C#", 32.71),
    ("Objective-C", 11.63),
    ("Lisp", 11.10),
    ("Modula", 9.42),
    ("ActionScript", 8.20),
    ("Basic", 5.84),
    ("Lua", 5.39),
    ("Pascal", 3.86),
    ("D", 3.75),
    ("Groovy", 3.35),
    ("Fortran", 3.25),
    ("Tcl", 3.16),
    ("Haskell", 2.87),
    ("Scala", 2.34),
    ("Erlang", 1.74),
    ("Objective Caml", 1.56),
    ("CoffeeScript", 1.33),
    ("Ada", 0.83),
    ("Go", 0.70),
    ("Vala", 0.69),
    ("F#", 0.63),
    ("Eiffel", 0.47),
    ("HaXe", 0.45),
)

EXPECTED_CLUSTERS = (
    ('Ubiquitous'  , ['C', 'JavaScript', 'Java', 'C++']),
    ('Very Popular', ['Python', 'PHP']),
    ('Popular'     , ['Perl', 'Ruby', 'C#']),
    ('Niche'       , ['Objective-C', 'Lisp', 'Modula', 'ActionScript', 'Basic', 'Lua', 'Pascal', 'D', 'Groovy', 'Fortran', 'Tcl', 'Haskell', 'Scala', 'Erlang', 'Objective Caml', 'CoffeeScript', 'Ada', 'Go', 'Vala', 'F#', 'Eiffel', 'HaXe']),
)

def test_langpop_hierarchical_clusters():
    clusters = find_clusters([Item(lang, n) for lang, n in LANGUAGES_POPULARITY],
                             ('Ubiquitous', 'Very Popular', 'Popular', 'Niche'))
    
    for cluster, (expected_label, expected_list) in zip(clusters, EXPECTED_CLUSTERS):
        assert cluster.name == expected_label
        
        cluster.items.sort(reverse=True)
        assert [item.name for item in cluster.items] == expected_list


if __name__ == '__main__':
    test_3D_hierarchical_clusters()
    test_langpop_hierarchical_clusters()


