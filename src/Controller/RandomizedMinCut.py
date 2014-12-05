import math
import datetime
import random
from src.Controller.Flow import Flow
__author__ = 'luvsandondov'
class RandomizedMinCut:
    '''
    Computes randomized min-cut of the given graph
    '''
    def __init__(self, graph):
        self.graph = graph

    def ComputeRandomMinCutRepeatedly(self, graph, repetition):
        '''
        Use amplification to get correct Randomized min-cut
        :param repetition -- Number of times to repeat the randomized min cut algorithm
        :return:
        '''
        # Initialize the min cut
        MinCut = float('Inf')
        # Repeat to get the best result
        for i in range(0, repetition):
            curr_MinCut = self.ComputeRandomizedMinCut(graph)
            # Minimum of current, and global minimum
            MinCut = min(curr_MinCut, MinCut)
        return MinCut

    def ComputeRandomizedMinCut(self, graph):
        '''
        Compute Random Min Cut in the graph
        :return: Value of the Min cut in the graph
        '''
        if len(graph.vertices) > 3:
            # Recursively call the function and get the minimal cut
            graph_1 = self.Contract(graph, int(len(graph.vertices)/math.sqrt(2) + 1))
            minCut_1 = self.ComputeRandomizedMinCut(graph_1)
            graph_2 = self.Contract(graph, int(len(graph.vertices)/math.sqrt(2) + 1))
            minCut_2 = self.ComputeRandomizedMinCut(graph_2)
            # Get the min of the two
            return min(minCut_1, minCut_2)
        else:
            return self.ComputeMinCutDirectly(graph)

    def ComputeMinCutDirectly(self, graph):
        '''
        Computes min cut in the graph directly, because the graph is small with at most 3 vertices
        :return: value of the actual min cut
        '''
        # Min cut has to isolate one vertex, since graph has either 2 or 3 vertices
        # So that vertex can be source or destination
        minCut = float("Inf")
        for source in graph.vertices:
            curr_MinCut = 0
            # Iterate through all the neighbors and add all capacities, since that is exactly the min cut for that vertex
            for neighbor_code in source.getAdjacency():
                curr_MinCut += source.getCapacity(neighbor_code)
            minCut = min(minCut, curr_MinCut)
        # One special vertex can be destination:
        for destination in graph.vertices:
            curr_MinCut = 0
            for vertex in graph.vertices:
                if vertex.isNeighbor(destination.code):
                    curr_MinCut += vertex.getCapacity(destination.code)
            minCut = min(minCut, curr_MinCut)
        return minCut


    def Contract(self, graph,  numOfVertexBound):
        '''
        Contract the given graph, given edge
        :param numOfVertexBound -- Number of vertex should leave after contraction
        :return:
        '''
        for i in range(len(graph.vertices), numOfVertexBound, -1):
            edge = self.GetRandomEdge(graph)
            graph = self.removeEdge(graph, edge)
        return graph

    def GetRandomEdge(self, graph):
        '''
        Get random edge in the given graph
        :return:
        '''
        # Get random vertex
        randVertex = random.choice(graph.vertices)
        # Get random adjacent edge
        try:
            randNeighborKey = random.choice(randVertex.getAdjacency())
            randNeighbor = graph.getVertexByCode(randNeighborKey)
            return [randVertex.code, randNeighbor.code]
        except:
            # IT is possible that random chosen vertex has no outgoing edge, so we have to do the process again
            self.GetRandomEdge(graph)

    def removeEdge(self, graph, edge):
        '''
        Removes given edge
        :param edge: list of two vertices
        :return:
        '''
        # Add new vertex, with all correct edges set up
        graph = self.addNewVertex(graph, edge)
        # Remove both vertices
        source_code = edge[0]
        destination_code = edge[1]
        graph.removeVertex(source_code)
        graph.removeVertex(destination_code)
        return graph

    def addNewVertex(self,graph, edge):
        '''
        Add new Vertex with all correct edges, combined the two vertices of edge
        :param edge: [source, destination] two vertices codes
        :return:
        '''
        # Initialize source and distance
        source = graph.getVertexByCode(edge[0])
        destination = graph.getVertexByCode(edge[1])
        # Add new vertex
        graph.addVertex("{}, {}".format(source.code, destination.code), "{}, {}".format(source.name, destination.name))
        newVertex = graph.getVertexByCode("{}, {}".format(source.code, destination.code))
        # Add all edges from all other vertices to source and distance to new vertex
        for vertex in graph.vertices:
            if vertex.code != source.code and vertex.code != destination.code and vertex.code != newVertex.code:
                if vertex.isNeighbor(source.code) and vertex.isNeighbor(destination.code):
                    vertex.addEdge(newVertex.code, vertex.getDistance(source.code) + vertex.getDistance(destination.code))
                elif vertex.isNeighbor(source.code):
                    vertex.addEdge(newVertex.code, vertex.getDistance(source.code))
                elif vertex.isNeighbor(destination.code):
                    vertex.addEdge(newVertex.code, vertex.getDistance(destination.code))
                    #there is no edge adding
                # Consider reverse direction
                if source.isNeighbor(vertex.code) and destination.isNeighbor(vertex.code):
                    newVertex.addEdge(vertex.code, source.getDistance(vertex.code) + destination.getDistance(vertex.code))
                elif source.isNeighbor(vertex.code):
                    newVertex.addEdge(vertex.code, source.getDistance(vertex.code))
                elif destination.isNeighbor(vertex.code):
                    newVertex.addEdge(vertex.code, destination.getDistance(vertex.code))
                    #there is no edge to add
                # They are the merging vertices, so do nothing
        return graph
