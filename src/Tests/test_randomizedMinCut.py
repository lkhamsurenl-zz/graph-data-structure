from unittest import TestCase
from src.Controller.RandomizedMinCut import RandomizedMinCut
from src.Model import Graph

__author__ = 'luvsandondov'


class TestRandomizedMinCut(TestCase):

    def test_GetRandomEdge(self):
        graph = Graph.Graph(['test.json'])
        MCUT = RandomizedMinCut(graph)
        edge = MCUT.GetRandomEdge(graph)
        source = graph.getVertexByCode(edge[0])
        destination = graph.getVertexByCode(edge[1])
        print "{} to {}".format(source.name, destination.name)

    def test_ComputeRandomizedMinCut(self):
        # Set up the graph
        graph = Graph.Graph(['test.json'])
        MCUT = RandomizedMinCut(graph)
        LIM = MCUT.graph.getVertexByCode("LIM")
        SCL = MCUT.graph.getVertexByCode("SCL")
        # Add new edge to make it interesting
        LIM.addEdge("ERD", 2000)
        source = MCUT.graph.getVertexByCode("ERD")
        destination = MCUT.graph.getVertexByCode("MEX")
        # Compute Randomized Min-Cut
        print MCUT.ComputeRandomizedMinCut(graph)

    def test_RemoveEdge(self):
        # Set up the graph
        graph = Graph.Graph(['test.json'])
        MCUT = RandomizedMinCut(graph)
        LIM = MCUT.graph.getVertexByCode("LIM")
        SCL = MCUT.graph.getVertexByCode("SCL")
        # Add new edge to make it interesting
        LIM.addEdge("ERD", 2000)
        source = MCUT.graph.getVertexByCode("ERD")
        destination = MCUT.graph.getVertexByCode("MEX")
        # remove edge
        graph = MCUT.removeEdge(graph, [source.code, destination.code])
        # CHeck there are exactly 3 vertices
        self.assertEqual(len(graph.vertices), 3)
        # Make sure the edges have correct edge distances
        newVertex = graph.getVertexByCode("ERD, MEX")
        self.assertEqual(LIM.getDistance(newVertex.code), 6231)
        self.assertEqual(SCL.getDistance(newVertex.code), 2454)

    def test_addNewVertex(self):
        # Set up the graph
        graph = Graph.Graph(['test.json'])
        MCUT = RandomizedMinCut(graph)
        LIM = MCUT.graph.getVertexByCode("LIM")
        SCL = MCUT.graph.getVertexByCode("SCL")
        # Add new edge to make it interesting
        LIM.addEdge("ERD", 2000)
        source = MCUT.graph.getVertexByCode("ERD")
        destination = MCUT.graph.getVertexByCode("MEX")
        # Add new vertex
        MCUT.addNewVertex(graph, [source.code, destination.code])
        # Check if the city actually created
        self.assertIsNotNone(MCUT.graph.getVertexByCode("ERD, MEX"))
        newVertex = MCUT.graph.getVertexByCode("ERD, MEX")
        # Make sure the edges are correctly added

        self.assertTrue(LIM.isNeighbor(newVertex.code))
        self.assertTrue(LIM.isNeighbor(newVertex.code))
        # Make sure distance is correctly add up
        self.assertEqual(LIM.getDistance(newVertex.code), 6231)
        self.assertEqual(SCL.getDistance(newVertex.code), 2454)
        # Ensure reverse edges are there
        self.assertTrue(newVertex.isNeighbor(LIM.code))
        self.assertTrue(newVertex.isNeighbor(SCL.code))