def parse() -> list[tuple[str]]:
    return [(line.strip().split("-")[0], line.strip().split("-")[1]) for line in open("input.txt").readlines()]

def generate_graph(connections) -> dict:
    nodes = {}
    for connection in connections:
        if nodes.get(connection[0]) == None:
            nodes[connection[0]] = set()
        if nodes.get(connection[1]) == None:
            nodes[connection[1]] = set()
        nodes[connection[0]].add(connection[1])
        nodes[connection[1]].add(connection[0])
    return nodes

def part1():
    connections = parse()
    graph = generate_graph(connections)

    # Finds a three length loop with at least one containg t
    found = set()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            for neighbors_neighbor in graph[neighbor]:
                if node in graph[neighbors_neighbor]:
                    if node.startswith("t") or neighbor.startswith("t") or neighbors_neighbor.startswith("t"):
                        s = sorted([node, neighbor, neighbors_neighbor])
                        found.add(tuple(s))

    print(len(found))

def neighbors_all(node: str, graph: dict, subgraph: set) -> bool:
    for n in subgraph:
        if node not in graph[n]:
            return False
    return True

def part2():
    connections = parse()
    graph = generate_graph(connections)

    biggest_subgraph = set()
    for node, neighbors in graph.items():
        result = set()
        result.add(node)
        for neighbor in neighbors:
            if neighbors_all(neighbor, graph, result):
                result.add(neighbor)

        if len(result) > len(biggest_subgraph):
            biggest_subgraph = result

    in_order = sorted([x for x in biggest_subgraph])

    print(",".join(in_order))

part2()