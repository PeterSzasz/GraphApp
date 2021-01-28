# graph related algorithms

from core.graph import Graph, Node, Edge

def breadth_first(graph: Graph) -> list:
    '''
    a breadth first graph traversal
    makes one traversal from node[0]
    
    Args:
        graph (Graph): full graph

    Returns:
        list: traversed nodes
    '''
    
    nodes = []
    nodes.append(graph.nodes[0])
    discovered = nodes[:]
    i = 0
    while nodes:
        print("start while:")
        i += 1
        if i >= 500:
            return discovered
        for node in nodes:
            print(f"checked node: {node}")
            for edge in node.nextEdge():
                new_node = edge.n1() if edge.n1() != node else edge.n2()
                if new_node not in discovered:
                    print(f"new node: {new_node}")
                    discovered.append(new_node)
                    nodes.append(new_node)
            nodes.remove(node)
    return discovered