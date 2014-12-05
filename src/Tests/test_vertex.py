from unittest import TestCase

from src.Model import Vertex

__author__ = 'Luvsandondov Lkhamsuren'


class TestVertex(TestCase):
    '''
    Test class for Vertex
    '''
    distance = 100
    vertex1 = Vertex.Vertex("SCL", "Santiago", "CL", "South America", -4 , {"S" : 33, "W" : 71}, 6000000, 1)
    vertex2 = Vertex.Vertex("MIA", "MIAMI", "US", "North America", -4 , {"S" : 30, "W" : 70}, 60000, 12)
    vertex3 = Vertex.Vertex("ULA", "Ulaanbaatar", "MN", "Asia", -8 , {"E" : 47, "N" : 106}, 1000000, 1)

    def test_addEdge(self):
        '''
        1. Ensure cannot add negative distance
        2. Make sure the distance is updated afterwards
        '''
        self.vertex1.addEdge(self.vertex2.code, self.distance)
        self.assertIsNotNone(self.vertex1.getAdjacency())

    def test_isNeighbor(self):
        '''
        1. Ensure exactly the ones I add are actually neighbors
        2. Ensure not neighbors are correctly recognized
        '''
        self.vertex1.addEdge(self.vertex2.code, self.distance)
        self.assertIsNotNone(self.vertex1.isNeighbor(self.vertex2.code))
        # Assert ULA is not a neighbor
        self.assertFalse(self.vertex1.isNeighbor(self.vertex3))

    def test_getDistance(self):
        '''
        1. Ensure correct distance is returned
        2. Ensure no negative distance
        '''
        self.vertex1.addEdge(self.vertex2.code, self.distance)
        self.assertEqual( self.vertex1.getDistance(self.vertex2.code), self.distance )

    def test_getVertexInformation(self):
        self.assertEqual(self.vertex1.code, "SCL")
        self.assertEqual(self.vertex1.name, "Santiago")
        self.assertEqual(self.vertex1.country, "CL")
        self.assertEqual(self.vertex1.continent, "South America")
        self.assertEqual(self.vertex1.timezone, -4)

    def test_removeEdge(self):
        self.vertex1.addEdge(self.vertex2.code, self.distance)
        self.vertex2.addEdge(self.vertex1.code, self.distance)
        self.vertex1.removeEdge(self.vertex2.code)
        self.assertEqual(len(self.vertex1.getAdjacency()), 0)
        # Ensure reverse edge has not been deleted
        self.assertNotEqual(len(self.vertex2.getAdjacency()), 0)
        print(self.vertex2.getAdjacency())

    def test_getTravelCost(self):
        '''
        # 1. travel cost cannot be negative
        '''
        self.vertex1.addEdge(self.vertex2.code, 400)
        self.vertex2.addEdge(self.vertex3.code, 500)
        #Cost should be decreased
        self.assertEqual([0.35*(400), 0.3], self.vertex1.getTravelCost(self.vertex2, 0.35))
        #Cannot be negative
        self.assertEqual([0*(500), 0], self.vertex1.getTravelCost(self.vertex2, 0))

    def test_getTravelTime(self):
        '''
        1. Ensure the time includes the delay
        2. Ensure travel time has different method for computing when less than 400
        '''
        self.vertex1.addEdge(self.vertex2.code, 400)
        self.vertex2.addEdge(self.vertex3.code, 500)
        #Cost should be decreased
        self.assertEqual( (0.0 + 800)*60/(0.0 + 750) + (0.0 +120 - 10*1), self.vertex1.getTravelTime(self.vertex2) )
        self.assertEqual( (0.0 + 800)*60/(0.0 + 750) + (0.0 + 100)*60/(0.0 + 750) + (0.0 +120 - 10*1), self.vertex2.getTravelTime(self.vertex3) )
