__author__ = 'Luvsandondov Lkhamsuren'
class Vertex:
    '''
    Class Vertex, implemented with adjacency list method
    '''
    def __init__(self, code, name = None, country = None, continent = None, timezone = None, coordinates = None,
                 population = None, region = None):
        self.code = code
        self.name = name
        self.country = country
        self.continent = continent
        self.timezone = timezone
        self.coordinates = coordinates
        self.population = population
        self.region = region
        # There are two more attributes used for finding shortest distance
        # DISTANCE FROM THE ROOT
        self.distance = float("Inf")
        # PREDECESSOR POINTER IN THE SSSP TREE
        self.pred = None
        # RANK AND PARENT for Disjoint set
        self.parent = self
        self.rank = 0
        # Adjacency list contains the codes of the neighbors, distance, capacity, and flow
        self.adjacencyList = {}

    def getAdjacency(self):
        '''
        #Get adjacency list for the vertex
        :return: Keys of all adjacent vertices
        '''
        return self.adjacencyList.keys()

    def addEdge(self, destination_code, distance):
        '''
        add neighbor with given distance
        :param destination_code: code name
        :param distance:  distance between
        :return:
        '''
        if distance > 0:
            # Edge capacity is 1 person per 1000km distance
            self.adjacencyList[destination_code] = {'distance':distance, 'capacity':distance/1000,'flow':0}
        else:
            print "You cannot pass non-positive distance between two cities"

    def isNeighbor(self, vertex_code):
        '''
        Check if the given vertex_code is neighbor
        :param vertex_code: code of the neighbor, if one exist
        :return: vertex
        '''
        return self.adjacencyList.get(vertex_code)

    def getDistance(self, neighbor_code):
        '''
        Get distance to the neighbor
        :param neighbor_code: code of the neighbor
        :return:
        '''
        return self.adjacencyList.get(neighbor_code)['distance']
    def getCapacity(self, neighbor_code):
        '''
        Get distance to the neighbor
        :param neighbor_code: code of the neighbor
        :return:
        '''
        return self.adjacencyList.get(neighbor_code)['capacity']
    def getFlow(self, neighbor_code):
        '''
        Get distance to the neighbor
        :param neighbor_code: code of the neighbor
        :return:
        '''
        return self.adjacencyList.get(neighbor_code)['flow']

    def getVertexInformation(self):
        '''
        Get vertex information:
        :return:
        '''
        string = None
        string = ('Code: {}\n'
              'Name: {}\n'
              'Country: {}\n'
              'Continent: {}\n'
              'TimeZone: {}\n'
              'Coordinates: {}\n'
              'Population: {}\n'
              'Region: {}\n'
              'Connected Cities:\n').format(
            self.code, self.name, self.country, self.continent, self.timezone,self.coordinates, self.population, self.region,
            )
        return string

    def removeEdge(self, destination_code):
        '''
        # Given destination vertex, remove the edge if exist:
        # NOTE: takes the destination code as an argument, not the name or actual vertex
        :param destination_code:
        :return:
        '''
        self.adjacencyList.pop(destination_code, None)

    def addFlow(self, destination_code, new_flow):
        self.adjacencyList.get(destination_code)['flow'] += new_flow

    def updateVertexInfo(self, code, name, country, continent, timezone, coordinates, population, region):
        '''
        # Update the vertex with given information
        :return:
        '''
        self.code = code
        self.name = name
        self.country = country
        self.continent = continent
        self.timezone = timezone
        self.coordinates = coordinates
        self.population =  population
        self.region = region

    def getTravelCost(self, next, currentCost):
        '''
        # Helper function to get travel time
        :param next: next vertex in the list (ideally the neighbor)
        :param currentCost: current cost per km
        :return:
        '''
        list = []
        # Here assume that travel cost is non-negative
        list.append(self.getDistance(next.code) * currentCost)
        list.append(max(currentCost - 0.05, 0))
        return list

    def getTravelTime(self, next):
        '''
        # Helper function to get travel time
        :param next: destination vertex
        :return: total time spend on travelling from this vertex to the neighbor
        '''
        distance = self.getDistance(next.code)
        # First get how long is the delay
        totalTime = 120 - len(self.getAdjacency())*10
        # If the distance is less than 400, I assume, the jet accelerates till 750, then decelerates
        if(distance >= 400):
            totalTime+= ((0.0 + 4 * 200)*60 /(0.0 + 750) + (0.0 + distance - 400)*60/(0.0 + 750))
        else:
            totalTime += (0.0 + 4*distance)/(0.0 + 750)
        return totalTime
    def get_edges(self):
        return
    ####################################################################################################################
    # Additional methods for final project
    ###################################################################################################################
    def getWonder(self):
        '''
        Helper function to figure out what wonder located nearby to this city
        '''
        if self.code == 'SAO':
            string = ['Christ The Redeemer', 'http://en.wikipedia.org/wiki/Christ_the_Redeemer_(statue)']
        elif self.code == 'LIM':
            string = ['Machu Picchu', 'http://en.wikipedia.org/wiki/Machu_Picchu']
        elif self.code == 'MEX':
            string = ['Chichen Itza','http://en.wikipedia.org/wiki/Chichen_Itza']
        elif self.code == 'MIL':
            string = ['Colosseum','http://en.wikipedia.org/wiki/Colosseum']
        elif self.code == 'CAI':
            string = ['Egyptian Pyramids','http://en.wikipedia.org/wiki/Egyptian_pyramids']
        elif self.code == 'DEL':
            string = ['Taj Mahal','http://en.wikipedia.org/wiki/Taj_Mahal']
        elif self.code == 'PEK':
            string = ['Great Wall of China','http://en.wikipedia.org/wiki/Great_Wall_of_China']
        else:
            string = ['Not a valid city: {}'.format(self.name)]
        return string
