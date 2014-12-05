__author__ = 'luvsandondov'


class Flow:
    '''
    This class will find max-flow across the network to schedule the airfare
    '''
    def __init__(self, g):
        '''

        :param g: Graph of to find the optimal schedule
        :return:
        '''
        self.g = g
    def find_residual_path(self, src, dest, path):
        '''
        Do a BFS on finding path from src to dest
        :param src: source vertex
        :param dest: destination vertex
        :param path: path from src to dest
        :return: found path
        '''
        if src == dest:
            return path
        src_vertex = self.g.getVertexByCode(src)
        for vertex_code in src_vertex.getAdjacency():
            residual = src_vertex.getCapacity(vertex_code) - src_vertex.getFlow(vertex_code)
            if residual > 0 and [src,vertex_code] not in path:
                result = self.find_residual_path(vertex_code, dest, path + [[src,vertex_code]])
                if result != None:
                    return result
    def max_flow(self, src, dest):
        '''
        Function to find max-flow in a graph
        :param src: source vertex code
        :param dest: distance vertex code
        :return: maximal flow in current network
        '''
        path = self.find_residual_path(src, dest, [])
        while path != None:
            residuals = []
            for pair in path:
                u = self.g.getVertexByCode(pair[0])
                # add residual to the list
                residuals.append(u.getCapacity(pair[1]) - u.getFlow(pair[1]))
            min_residual = min(residuals)
            # subtract the value from all in path
            for pair in path:
                u = self.g.getVertexByCode(pair[0])
                v = self.g.getVertexByCode(pair[1])
                # add flow in u to v direction
                u.addFlow(pair[1], min_residual)
                # subtract this flow in reverse direction
                v.addFlow(pair[0], -min_residual)
            # recurse
            path = self.find_residual_path(src, dest, [])
        # here we have successfully found the max-flow, we find the amount by adding all values going out of source
        src_vertex = self.g.getVertexByCode(src)
        max_flow = 0
        for neighbor_code in src_vertex.getAdjacency():
            max_flow += src_vertex.getFlow(neighbor_code)
        # return the value
        return max_flow
    def min_cut(self, src, dest):
        '''
        Find the minimal cut to isolate source from dest
        :param src: source vertex_code
        :param dest: destination vertex_code
        :return: number of pilots to destroy
        '''
        max_flow = self.max_flow(src,dest)
        return "You will be required to execute at least " + str(max_flow) + \
               " pilots to stop Agent 007, LJ to get from " +  self.g.getVertexByCode(src).name + " to " \
               + self.g.getVertexByCode(dest).name
