from unittest import TestCase

from src.Controller import Flow
from src.Model import Graph

__author__ = 'luvsandondov'


class TestFlow(TestCase):
    '''
    Test class for Flow
    '''
    def test_find_residual_path(self):
        g = Graph.Graph(['test.json'])
        flow = Flow.Flow(g)
        flow1 =  flow.find_residual_path('SCL', 'MEX', [])
        # Ensure everything is in correct order
        self.assertEqual(flow1[0], ['SCL', 'ERD'])
        self.assertEqual(flow1[1], ['ERD', 'SCL'])
        self.assertEqual(flow1[2], ['SCL', 'LIM'])
        self.assertEqual(flow1[3], ['LIM', 'MEX'])
        v1 = g.getVertexByCode('SCL')
        v1.removeEdge('ERD')
        flow2 =  flow.find_residual_path('SCL', 'MEX', [])
        self.assertEqual(flow2[0], ['SCL', 'LIM'])
        self.assertEqual(flow2[1], ['LIM', 'MEX'])

    def test_max_flow(self):
        g = Graph.Graph(['test.json'])
        flow = Flow.Flow(g)
        # Ensure actual flows are computed correctly
        self.assertEqual(flow.max_flow('SCL', 'MEX'), 2 + 2)
        # Same should also hold for SCL - ERD as well
        self.assertEqual(flow.max_flow('SCL', 'ERD'), 4)

    def test_min_cut(self):
        g = Graph.Graph(['test.json'])
        flow = Flow.Flow(g)
        print flow.min_cut('SCL', 'ERD')