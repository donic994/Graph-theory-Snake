from collections import deque, namedtuple

inf = float('inf') #We'll use infinity as a default distance to nodes.
Edge = namedtuple('Edge', 'start, end, cost')


def make_edge(start, end, cost=1):
  return Edge(start, end, cost)


class Graph:
    def __init__(self, edges):
        #Checks that the data is right
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))

        self.edges = [make_edge(*edge) for edge in edges]


    """
    In the original implementation the vertices are defined in the _ _ init _ _,
    but we'll need them to update when edges change,
    so we'll make them a property, they'll be recounted each time we address the property.
    We think this is the problem with our calculation speed, 
    because when tested on a much smaller graph it was really fast.
    But since we are removing and adding edges after every move, it takes time to recount all vertices 
    """
    @property
    def vertices(self):
        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    """
    Returns egdes that are pairs 
    """
    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    """
    Removes edge from the graph
    """
    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)
   
    """
    Adds edge to the graph
    """
    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=str(n1), end=str(n2), cost=cost))
        if both_ends:
            self.edges.append(Edge(start=str(n2), end=str(n1), cost=cost))


    """
    Neighbors for every node
    """
    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Such source node doesn\'t exist'
        """
        Mark all nodes unvisited and store them.
        Set the distance to zero for our initial node and to infinity for other nodes.
        """
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            """
            Select the unvisited node with the smallest distance, it's current node now.
            """
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)

            """
            If the smallest distance among unvisited nodes in infinity STOP
            """
            if distances[current_vertex] == inf:
                break
            """
            Find unvisited neighbors for the current node and calculate their distances through the current node.
            """
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                """
                Compare the newly calculated distance to the assigned and save the smaller one.
                """
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return path
