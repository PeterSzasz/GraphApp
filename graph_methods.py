# graph related algorithms

from core.graph import Graph, Node, Edge
from graph_visualisation import VisGraph

def breadth_first(graph: Graph, start_node: Node) -> tuple:
    '''
    A breadth first graph traversal
    makes one traversal from start_node.
    
    Args:
        graph (Graph): full graph
        start_node (Node): starting node

    Returns:
        tuple: two list, traversed nodes and traversed edges
    '''
    
    nodes = [start_node]
    discovered_nodes = nodes[:]
    discovered_edges = []
    i = 0
    while nodes:
        i += 1
        if i >= 300:
            # failsafe, TODO:replace or delete
            return discovered_nodes, discovered_edges
        node = nodes.pop(0)
        for edge in node.nextEdge():
            new_node = edge.n1() if edge.n1() != node else edge.n2()
            if new_node not in discovered_nodes:
                discovered_nodes.append(new_node)
                discovered_edges.append(edge)
                nodes.append(new_node)
            
    return discovered_nodes, discovered_edges

def depth_first(graph: Graph, start_node: Node) -> list:
    '''
    A depth first graph traversal
    makes one traversal from start_node.
    
    Args:
        graph (Graph): full graph
        start_node (Node): starting node

    Returns:
        list: traversed nodes
    '''
    pass

def highlightComponents(graph: VisGraph) -> None:
    '''
    Finds separate components in graph, starts in node[0] 
    and marks the nodes with appropriate component number.

    Args:
        graph (VisGraph): full graph

    Returns:
        None
    '''
    componentNo = 1
    nodeNo = 1
    graph.highlighted_node, _ = breadth_first(graph, graph.nodes[0])
    for node in graph.highlighted_node:
        node.data = {'component': componentNo, 'number': nodeNo}
        nodeNo += 1

    for node in graph.nextNode():
        nodeNo = 1
        if node not in graph.highlighted_node:
            componentNo += 1
            new_component, _ = breadth_first(graph, node)
            for node in new_component:
                node.data = {'component': componentNo, 'number': nodeNo}
                nodeNo += 1
            graph.highlighted_node.extend(new_component)

def highlightSpanningTree(graph: VisGraph) -> None:
    '''
    Finds separate components in graph, starts in node[0]
    and highlights the nodes and edges that represents a spanning tree.

    Args:
        graph (VisGraph): full graph

    Returns:
        None
    '''
    componentNo = 1
    nodeNo = 1
    graph.highlighted_node, graph.highlighted_edge = breadth_first(graph, graph.nodes[0])
    for node in graph.highlighted_node:
        node.data = {'component': componentNo, 'number': nodeNo}
        nodeNo += 1

    for node in graph.nextNode():
        nodeNo = 1
        if node not in graph.highlighted_node:
            componentNo += 1
            new_component, graph.highlighted_edge = breadth_first(graph, node)
            for node in new_component:
                node.data = {'component': componentNo, 'number': nodeNo}
                nodeNo += 1
            graph.highlighted_node.extend(new_component)