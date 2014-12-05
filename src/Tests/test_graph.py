from unittest import TestCase

from src.Model import Graph

__author__ = 'Luvsandondov Lkhamsuren'


class TestGraph(TestCase):
    '''
    Test class for Graph data structure
    '''
    def test_getVerticesNames(self):
        # pass loading data
        g = Graph.Graph(['test.json'])
        # Exactly 3 ciities should be added
        self.assertTrue("Santiago" in g.getVerticesNames())
        self.assertTrue("Lima" in g.getVerticesNames())
        self.assertTrue("Mexico City" in g.getVerticesNames())
        self.assertFalse("Miami" in g.getVerticesNames())

    def test_getVertexByName(self):
        '''
        # Gets the vertex, given the name of the vertex
        '''
        # pass loading data
        g = Graph.Graph(['test.json'])
        self.assertTrue("Santiago", g.getVertexByName("Santiago").name)
        self.assertIsNone(g.getVertexByName("Miami"))

    def test_getVertexByCode(self):
        '''
        # Gets the vertex by code
        '''
        # pass loading data
        g = Graph.Graph(['test.json'])
        self.assertTrue("Santiago", g.getVertexByCode("SCL").name)
        self.assertIsNone(g.getVertexByCode("MIA"))

    def test_getLongestEdge(self):
        '''
        # Test getting the longest edge in the network
        '''
        # pass loading data
        g = Graph.Graph(['test.json'])
        list = g.getLongestEdge()
        self.assertEqual("Mexico City", list[0])
        # Make sure they are in correct order
        self.assertEqual("Erdenet", list[1])
        self.assertEqual(4232, list[2])

    def test_getShortestEdge(self):
        '''
        # Test shortest edge
        '''
        # pass loading data
        g = Graph.Graph(['test.json'])
        list = g.getShortestEdge()
        self.assertEqual("Santiago", list[0])
        # Make sure they are in correct order
        self.assertNotEqual("Lima", list[0])
        self.assertEqual("Lima", list[1])
        self.assertEqual(2453, list[2])

    def test_getAverageEdgeLength(self):
        '''
        # Test average edge length in the network
        '''
        # pass loading data
        g = Graph.Graph(['test.json'])
        aver = g.getAverageEdgeLength()
        actual = (2453 + 4231)/2
        self.assertEqual(aver, actual)

    def test_getBiggestCityPopulation(self):
        '''
        # Test biggest city
        '''
        # pass loading data
        g = Graph.Graph(['test.json'])
        city =g.getBiggestCityPopulation()
        self.assertEqual(city.name, "Mexico City")
        self.assertEqual(city.code, "MEX")
        self.assertNotEqual(city.name, "Lima")

    def test_getSmallestCity(self):
        '''
        # Test smallest city
        '''
        # pass loading data
        g = Graph.Graph(['test.json'])
        city =g.getSmallestCity()
        self.assertEqual(city.name, "Erdenet")
        self.assertEqual(city.code, "ERD")
        self.assertNotEqual(city.name, "Lima")

    def test_getHubCities(self):
        '''
        # Test city with most connections
        '''
        # pass loading data
        g = Graph.Graph(['test.json'])
        list = g.getHubCities()
        #Make sure there are 4 hub cities
        self.assertEqual(2, len(list))
        self.assertEqual("Santiago", list[0][0])

    # Remove the certain vertex
    def test_removeVertex(self):
        '''
        # Test removing vertex from the network
        '''
        # pass loading data
        g = Graph.Graph(['test.json'])
        g.removeVertex("LIM")
        self.assertIsNone(g.getVertexByCode("LIM"))
        self.assertEqual(len(g.getVertexByCode("SCL").getAdjacency()), 1)
        self.assertEqual(len(g.getVertexByCode("MEX").getAdjacency()), 1)
        # MAke sure cannot remove non existent city
        g.removeVertex("LIM")
        g.removeVertex("SCL")
        g.removeVertex("MEX")
        # you can remove all the vertices
        print g.vertices
        self.assertEqual(len(g.vertices), 1)

    def test_addVertex(self):
        '''
        # Test adding vertex to the network
        '''
        # pass loading data
        g = Graph.Graph(['test.json'])
        g.addVertex("LIM", "Lima", "PE", "South America", -5, {"S" : 12, "W" : 77}, 9050000, 1)
        self.assertEqual(len(g.vertices), 4)
        g.addVertex("ULA", "Ulaanbaatar", "MN", "Asia", -8, {"S":67, "N":150}, 1600000, 1)
        self.assertEqual(len(g.vertices), 5)
        # Check cannot pass negative population
        g.addVertex("ONG", "Onga", "PE", "South America", -5, {"S" : 12, "W" : 77}, -5, 1)
        self.assertEqual(len(g.vertices), 5)

    def test_updateVertex(self):
        '''
        # Test updating vertex in the graph
        '''
        # pass loading data
        g = Graph.Graph(['test.json'])
        g.updateVertex("LIM", "Lima", "PE", "South America", -5, {"S" : 12, "W" : 77}, 9050000, 1)
        print g.getVertexByCode("LIM").getVertexInformation()
        g.updateVertex("LIM", "Lima", "PE", "South America", -5, {"S" : 12, "W" : 77}, -5, 1)
        print g.getVertexByCode("LIM").getVertexInformation()
        # Ensure information has been updated
        g.updateVertex("LIM", "Lima", "PE", "South America", -5, {"S" : 12, "W" : 77}, 9050001, 1)
        print g.getVertexByCode("LIM").getVertexInformation()
        # Cannot edit non-existing city
        g.updateVertex("ULA", "Ulaanbaatar", "MN", "Asia", -8, {"S":67, "N":150}, 1600000, 1)
        self.assertEqual(len(g.vertices), 4)

    def test_findSSSP(self):
        '''
        # Test Finding SSSP
        1. Correct implementation should find shortest path to any vertex from the root
        NOTE: Both Dikstra and Bellman-Ford should return same result here
        '''
        # pass loading data
        g = Graph.Graph(['test.json'])
        g.findSSSP(g.getVertexByCode("LIM"))
        self.assertEqual(g.getVertexByCode("SCL").pred, g.getVertexByCode("LIM"))
        self.assertEqual(g.getVertexByCode("MEX").pred, g.getVertexByCode("LIM"))
        # GEt another SSSP
        g.findSSSP(g.getVertexByCode("SCL"))
        self.assertEqual(g.getVertexByCode("MEX").pred, g.getVertexByCode("LIM"))
        self.assertEqual(g.getVertexByCode("LIM").pred, g.getVertexByCode("SCL"))
        # Another one
        g.findSSSP(g.getVertexByCode("ERD"))
        self.assertEqual(g.getVertexByCode("MEX").pred, g.getVertexByCode("ERD"))
        self.assertEqual(g.getVertexByCode("LIM").pred, g.getVertexByCode("SCL"))
        self.assertEqual(g.getVertexByCode("SCL").pred, g.getVertexByCode("ERD"))

    def test_AllPairShortestPath(self):
        '''
        Test on checking all pair shortest algorithm works
        :return:
        '''
        g = Graph.Graph(['test.json'])
        distances = g.allPairShortestPaths()
        # Ensure all connected nodes have minimal distances
        self.assertEqual(distances['SCL']['LIM'], 2453)
        self.assertEqual(distances['SCL']['ERD'], 2454)
        # ENsure distances away cities have correct minimal distance
        self.assertEqual(distances['SCL']['MEX'], 6684)
        self.assertEqual(distances['ERD']['LIM'], 4907)
        # Make some modifications
        graph_1 = Graph.Graph(['test.json'])
        lim = graph_1.getVertexByCode('LIM')
        lim.removeEdge('SCL')
        # No direct connection from LIM to SCL
        distances = graph_1.allPairShortestPaths()
        self.assertEqual(distances['LIM']['SCL'], 4231 + 4232 + 2454)
        # But other way around is direct
        self.assertEqual(distances['SCL']['LIM'], 2453)
        # Other distances are still valid
        self.assertEqual(distances['SCL']['ERD'], 2454)
        self.assertEqual(distances['SCL']['MEX'], 6684)
        self.assertEqual(distances['SCL']['LIM'], 2453)
        # It should take longer route to get LIM to ERD
        self.assertEqual(distances['LIM']['ERD'], 4231 + 4232)