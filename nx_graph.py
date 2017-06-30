import networkx as nx


# key: bus line, value: list of stop IDs
bus_lines = {
    '46': [1, 2, 3, 4, 5, 6],
    '46.5': [1, 2, 3, 4, 5, 6],
    '47': [5, 6, 7, 8, 9],
    '48': [9, 10, 11],
    '49': [4, 10, 12],
    '50': [3, 12]
}

# A multigraph allows multiple edges between the same nodes (we will label each
# edge with it's lineId to distinguish between them)
MG = nx.MultiGraph()

for line, stops in bus_lines.items():
    # Draw an edge between every stop for each line,
    # so number of nodes in shortest path = number of changes needed + 2 (the
    # origin and the destination)
    for stop in stops:

        for s in stops:

            # check whether an edge between these nodes has already been added
            # for this line, and don't create an edge to itself
            if str(line) not in MG.get_edge_data(stop, s, default={}).values()\
                    and s != stop:
                MG.add_edge(stop, s, line=line)

        # all edges for this stop have now been added, so we can remove it from the list
        stops.remove(stop)


def parse_journey(graph, changes):
    """takes the graph and a list of nodes, yields a tuple of a node, and the
    edges that link it to the next node in the list"""
    changes = iter(changes)
    prev_stop = next(changes)
    for next_stop in changes:
        yield prev_stop, graph[prev_stop][next_stop]
        prev_stop = next_stop


origin, destination = 1, 12
changes = nx.dijkstra_path(MG, origin, destination)


print('Origin, changes, and destination: {}'.format(changes))
for stop, options in parse_journey(MG, changes):
    print('Stop: {}'.format(stop), end=' :: ')
    print('Options: {}'.format(options))
