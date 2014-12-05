__author__ = 'luvsandondov'
class DisjointSet:
    '''
    Disjoint set of objects data structure
    '''

    def makeSet(self, vertex):
        '''
        Given a object, builds new set
        :param vertex:
        :return:
        '''
        vertex.parent = vertex
        vertex.rank = 0

    def union(self, vertex_1, vertex_2):
        '''
        Merge two given sets containing object_1 and object_2
        :param vertex_1:
        :param vertex_2:
        :return:
        '''
        root_1 = self.find(vertex_1)
        root_2 = self.find(vertex_2)

        # Elements can be in same set
        if root_1 == root_2:
            return
        else:
            # root_2 has higher rank, so it should be new root
            if root_1.rank < root_2.rank:
                root_1.parent = root_2
            # root_1 has higher rank
            elif root_1.rank > root_2.rank:
                root_2.parent = root_1
            else:
                # if there is a tie, make root_1 root and increment its rank
                root_2.parent = root_1
                root_1.rank += 1

    def find(self, vertex):
        '''
        Find the root of the set containing object
        :param vertex:
        :return:
        '''
        # If current element is not root, then compress the path by letting root to be parent of current element
        if vertex.parent != vertex:
            vertex.parent = self.find(vertex.parent)
        return vertex.parent