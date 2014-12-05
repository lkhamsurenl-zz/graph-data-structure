from Queue import PriorityQueue
import tkMessageBox

from src.Model import Vertex
from src.Model.DisjointSet import DisjointSet


__author__ = 'Luvsandondov Lkhamsuren'
import json
########################################################################################################################
# Helper functions
########################################################################################################################
def findVertex(self, vertex_code):
    '''
    # Find vertex given code
    :param vertex_code: given vertex code
    :return:
    '''
    for vertex in self.vertices:
        if vertex.code == vertex_code:
            return vertex

def init_class_graph(self, class_dict):
    '''
    Initialize the graph with all the class names,
    :param class_dict: dictionary including all class names as a adjacency list
    :return:
    '''
    for key in class_dict.keys():
        vertex = Vertex.Vertex(key, key)
        self.vertices.append(vertex)
    # Add edges between all vertex in the graph
    for key in class_dict.keys():
        for neighbor_name in class_dict[key]:
            neighbor = self.getVertexByName(neighbor_name)
            # If neighbor exists in current CS class list, then connect them
            if neighbor is not None:
                # Edge will be directed away from neighbor to current city since neighbor is prereq
                # For now, weight is just 1
                neighbor.addEdge(key, 1)

def init_graph(self, json_data_list):
    '''
    # initialize the given graph based on the data
    :param json_data_list: list of json data
    :return:
    '''
    # First load the data
    for json_data_name in json_data_list:
        json_data = open(json_data_name)
        data = json.load(json_data)
        # Add all vertices first
        for city in data["metros"]:
            vertex = Vertex.Vertex(city["code"], city["name"], city["country"], city["continent"], city["timezone"],
                            city["coordinates"], city["population"], city["region"])
            self.vertices.append(vertex)
    for json_data_name in json_data_list:
        json_data = open(json_data_name)
        data = json.load(json_data)
        # Add the routes between them
        for route in data["routes"]:
            # Destination vertex
            vertex_code1 = route["ports"][0]
            # Source vertex
            vertex_code2 = route["ports"][1]
            vertex1 = findVertex(self, vertex_code1)
            vertex2 = findVertex(self, vertex_code2)
            # Add the edge only if both vertices exist in the network
            if vertex2 is not None:
                vertex2.addEdge(vertex_code1, route["distance"])
                # return edge will be added only when we are not loading classes.json
                if json_data_name != "../../resources/data/classes.json":
                    vertex1.addEdge(vertex_code2, route["distance"])

def runBellmanFord(self, root):
    '''
    # Bellman-Ford on finding SSSP given root
    # NOTE: Running time would be O(mn), n - number of vertices , m -number of edges
    :param root:
    :return:
    '''
    root.distance = 0
    root.pred = None
    # Initialize the all other vertices by setting distance to be infinity and pred None
    for vertex in self.vertices:
        if vertex is not root:
            vertex.distance = float("Inf")
            vertex.pred = None
    # Iterate
    for vertex1 in self.vertices:
        for vertex in self.vertices:
            for neighbor_code in vertex.getAdjacency():
                neighbor = self.getVertexByCode(neighbor_code)
                if neighbor.distance > vertex.distance + vertex.getDistance(neighbor_code):
                    neighbor.distance = vertex.distance + vertex.getDistance(neighbor_code)
                    neighbor.pred = vertex

def runDijkstra(self, root):
    '''
    Function to find SSSP rooted at root, using Dikjstra's algorithm
    # NOTE: Priority Queue get method does not remove the min element
    :param root:
    :return:
    '''
    root.distance = 0
    root.pred = None
    size = len(self.vertices)
    for vertex in self.vertices:
        if vertex is not root:
            vertex.distance = float("Inf")
            vertex.pred = None
    queue = PriorityQueue()
    queue.put((root.distance, root))
    while not queue.empty():
        #min = queue.get()
        min = queue.delMin()
        vertex = min[1]
        for neighbor_code in vertex.getAdjacency():
            neighbor = self.getVertexByCode(neighbor_code)
            if(neighbor.distance > vertex.distance + vertex.getDistance(neighbor_code)):
                neighbor.distance = vertex.distance + vertex.getDistance(neighbor_code)
                neighbor.pred = vertex
                # Add the neighbor into the queue
                queue.put((vertex.distance, vertex))

########################################################################################################################
# Class definition
########################################################################################################################
class Graph:
    def __init__(self, json_data):
        '''
        Constructors
        :param json_data:
        :return:
        '''
        self.vertices = []
        self.correction_list = {'Bogota':'Colombia', 'Kinshasa':'Congo', 'Khartoum':'Sudan', 'Algiers':'ALgeria',
                                'Essen':'Denmark', 'Bagdad':'Iraq', 'Tehrah':'Iran', 'Riyadh':'Saudi Arabia',
                                'Karachi':'Pakistan', 'Mumbai':'Indonesia', 'Chennai':'India', 'Calcutta':'India',
                                'Washington':'Washington DC','St. Petersburg':"St Petersburg", 'Champaign':'Chicago'}
        init_graph(self, json_data)

    def getVerticesNames(self):
        '''
        # List of Cities in the system
        :return: all cities in the network as a list
        '''
        listOfCities = []
        for vertex in self.vertices:
            listOfCities.append(vertex.name)
        return listOfCities

    def getVerticesCodes(self):
        listOfVertices = []
        for vertex in self.vertices:
            listOfVertices.append(vertex.code)
        return listOfVertices

    def getVertexByName(self, vertex_name):
        '''
        Given a name of the String find if vertex exist or not
        :param vertex_name: name of the vertex
        :return:
        '''
        for v in self.vertices:
            if v.name == vertex_name:
                return v
        return None

    def getVertexByCode(self, vertex_code):
        '''
        Given a name of the String find if vertex exist or not
        :param vertex_code:
        :return:
        '''
        for v in self.vertices:
            if v.code == vertex_code:
                return v
        return None

    def getLongestEdge(self):
        '''
        Get the longest distance in the graph as a list:
        :return: source, destination, and distance as a list
        '''
        longest_distance = [None] * 3
        for u in self.vertices:
            for v_code in u.getAdjacency():
                if longest_distance[2] < u.getDistance(v_code):
                    longest_distance[2] = u.getDistance(v_code)
                    longest_distance[0] = u.name
                    v = self.getVertexByCode(v_code)
                    longest_distance[1] = v.name
        return longest_distance

    def getShortestEdge(self):
        '''
        Shortest distance in the graph
        :return: source, destination, and distance
        '''
        shortest_distance = [None] * 3
        shortest_distance[2] = float("inf")
        for u in self.vertices:
            for v_code in u.getAdjacency():
                if shortest_distance[2] > u.getDistance(v_code):
                    shortest_distance[2] = u.getDistance(v_code)
                    shortest_distance[0] = u.name
                    v = self.getVertexByCode(v_code)
                    shortest_distance[1] = v.name
        return shortest_distance

    def getAverageEdgeLength(self):
        '''
        Get the Average path
        NOTE: Each edge will be exactly added twice, but we increment edge counter as well
        :return: average length in integer
        '''
        totalLength = 0;
        totalNumEdges = 0;
        for u in self.vertices:
            for v_code in u.getAdjacency():
                totalNumEdges = totalNumEdges + 1
                totalLength = totalLength + u.getDistance(v_code)
        return totalLength / totalNumEdges

    def getBiggestCityPopulation(self):
        '''
        Find biggest city by the population
        :return: Name of the biggest city
        '''
        biggestCity = None
        for u in self.vertices:
            if biggestCity is not None:
                if u.population > biggestCity.population:
                    biggestCity = u
            else:
                biggestCity = u
        return biggestCity

    def getSmallestCity(self):
        '''
        Find Smallest city
        :return: Name of the smallest city
        '''
        smallestCity = None
        for u in self.vertices:
            if smallestCity is None:
                smallestCity = u
            elif u.population < smallestCity.population:
                smallestCity = u
        return smallestCity

    def findAverageSize(self):
        '''
        Find average size of the cities
        :return: average size of all cities in int
        '''
        totalNumCities = len(self.vertices)
        totalPopulation = 0
        for u in self.vertices:
            totalPopulation += u.population
        return totalPopulation / totalNumCities

    def getListContinents(self):
        '''
        get the list of continents
        :return: get list of continents such that each continent has all its cities
        '''
        continents = {}
        for u in self.vertices:
            if u.continent not in continents:
                continents[u.continent] = ""
            continents[u.continent] += ", " + u.name
        return continents

    def getHubCities(self):
        '''
        # Get hub cities, which have most number of direct flights from
        # NOTE: First pass through to find max connections
        :return: list of all cities with maximum connections
        '''
        hubCitiesNames = []
        maxHubCityConnections = 0
        for u in self.vertices:
            if len(u.getAdjacency()) > maxHubCityConnections:
                maxHubCityConnections = len(u.getAdjacency())
        # Second pass
        for u in self.vertices:
            if len(u.getAdjacency()) == maxHubCityConnections:
                hubCitiesNames.append(u.name)                               # add this city to the list
        return [hubCitiesNames, maxHubCityConnections]

########################################################################################################################
# Updating current information
########################################################################################################################
    def removeVertex(self, vertex_code):
        '''
        # Remove specified vertex
        # NOTE: function takes vertex_code as an argument, not the actual vertex
        :param vertex_code: Code of the vertex to be removed
        :return:
        '''
        if self.getVertexByCode(vertex_code) is not None:
            current_vertex = self.getVertexByCode(vertex_code)
            # Remove all outgoing edges
            for dest_code in current_vertex.getAdjacency():
                dest = self.getVertexByCode(dest_code)
                # Remove dest to curr_edge edge
                current_vertex.removeEdge(dest_code)
            # remove all incoming edges
            for source in self.vertices:
                source.removeEdge(vertex_code)
            #Now remove the vertex from the graph
            self.vertices.remove(current_vertex)
        else:
            print "There is no such city: " + vertex_code

    def addVertex(self, code, name = None, country = None, continent = None, timezone = None, coordinates = None,
                  population = float("Inf"), region = None):
        '''
        NOTE: update the population?????
        Add a given city
        :return:
        '''
        if self.getVertexByCode(code) is None and population > 0:
            vertex = Vertex.Vertex(code, name, country, continent, timezone, coordinates, population, region)
            self.vertices.append(vertex)
        elif population < 0:
            print "You cannot pass negative population"
        else:
            print name + " city already exist!"

    def updateVertex(self, code, name, country, continent, timezone, coordinates, population, region):
        if self.getVertexByCode(code) is not None and population > 0:
            # I assumed you cannot change the vertex code, since it is the only unique thing
            vertex = self.getVertexByCode(code)
            vertex.updateVertexInfo(code, name, country, continent, timezone, coordinates, population, region)
        elif population < 0:
            print "You cannot pass negative population"
        else:
            print name + " does not exist in the current network!"

    def findSSSP(self, root):
        '''
        Find the SSSP rooted at given vertex, using Dikstra and Bellman-Ford
        :param root: source vertex
        :return:
        '''
        if root not in self.vertices:
            print "Root cannot be located in the tree"
            return
        else:
            #runDijkstra(self, root)
            runBellmanFord(self, root)
#######################################################################################################################
# Additional methods
#######################################################################################################################

    def visualizeNetwork(self):
        '''
        #Helper function to get all cities, connections, and direct to browser
        :param g: Graph
        :return: return the URL of the picture of the current network
        '''
        new = 2  # open in a new tab, if possible
        URL = "http://www.gcmap.com/map?P="
        for u in self.vertices:
            for vertex_code in u.getAdjacency():
                URL = URL + '+' + u.code + '-' + vertex_code + ','
        # We have extra + very first ,and extra , at the very end
        correctURL = URL[:27] + URL[28:len(URL) - 1]
        correctURL += '&MS=wls&MR=1800&MX=720x360&PM=%2a'
        # For picturing the graph on the browser
        #webbrowser.open(correctURL, new=new)
        return correctURL
    def getRouteInformation(self):
        '''
        # Helper function to getting route names
        :param g: Graph
        :return:
        '''
        print("Please enter the route cities in start to end order, separated by ', ' ")
        input = raw_input().split(", ")
        self.getRouteInfoFromList(self, input)

    def getRouteInfoFromList(self, input):
        '''
        # Helper function to get route information
        :param g: Graph
        :param input: user input list
        :return:
        '''
        # Necessary information:
        totalDistance = 0
        totalCost = 0
        totalTime = 0
        # Current cost per kilometer
        currentCost = 0.35
        i = 0
        route = ""
        try:
            while i is not len(input) - 1:
                current = self.getVertexByName(input[i])
                next = self.getVertexByName(input[i + 1])
                if next is not None and next.code in current.getAdjacency():
                    totalDistance += current.getDistance(next.code)
                    totalCost += current.getTravelCost(next, currentCost)[0]
                    currentCost = current.getTravelCost(next, currentCost)[1]
                    totalTime += current.getTravelTime(next)
                    route += input[i] + "->"
                    i = i + 1;
                elif (next.code not in current.getAdjacency):
                    message = "There is no such route from {} to {}".format(current, next)
                    tkMessageBox.showerror("No Route", message)
                    return
                else:
                    break
            route += input[i]
            tkMessageBox.showinfo("Route Info", route + '\nTotal Distance: ' + str(totalDistance) + 'kms\n'
                  'Total Cost: '+ str(totalCost) +  '$\n'
                  'Total Time: ' + str( int(totalTime / 60) )+ ' hours, ' + str( totalTime % 60  )+ ' minutes\n')
        except:
            tkMessageBox.showerror("No Route", "There is no such route")
    def getJSON(self, name):
        '''
        Get JSON file based on current network
        :param g: Graph
        :return:
        '''
        data = {"metros": [], "routes": []}
        for vertex in self.vertices:
            for neighbor_code in vertex.getAdjacency():
                ports = [vertex.code, neighbor_code]
                distance = vertex.getDistance(neighbor_code)
                new_route = {"ports": ports, "distance": distance}
                curr = data.get("routes")
                curr.append(new_route)
                data["routes"] = curr
            # We add this vertex
            new_node = {"code": vertex.code, "name": vertex.name, "country": vertex.country, "continent": vertex.continent
                , "timezone": vertex.timezone, "coordinates": vertex.coordinates, "population": vertex.population,
                        "region": vertex.region}
            curr_metros = data.get("metros")
            curr_metros.append(new_node)
            data["metros"] = curr_metros
        with open('../../resources/data/{}.json'.format(name), 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)

    def getCitiesWithMostConnections(self):
        list = self.getHubCities();
        value = ""
        for city_name in list[0]:
            value += city_name + ", "
        value += " have " + str(list[1]) + " connections"
        return value
    def getContinentalInformation(self):
        listOfContinents = self.getListContinents()
        collector = ""
        for continent in listOfContinents:
                collector += continent + ": " + listOfContinents[continent][2:] + "\n\n"
        return 'a list of the continents served by CSAir: \n\n {}'.format(collector)
    def parseInput(input, self):
        '''
        # Parse initial input
        :param input: user input
        :param g: Graph
        :return:
        '''
        if input == 1:
            string = "\n"
            # Counter for the list labeling
            count = 1;
            for city_name in self.getVerticesNames():
                string += str(count) + ". " + city_name + "\n"
                count = count + 1
            print 'Cities: {}'.format(string)
        elif input == 2:
            self.getCityInformation()
        elif input == 3:
            self.getStatisticalInformation()
        elif input == 4:
            listOfContinents = self.getListContinents()
            collector = ""
            for continent in listOfContinents:
                collector += continent + ": " + listOfContinents[continent][2:] + "\n"
            print 'a list of the continents served by CSAir: \n{}'.format(collector)
        elif input == 5:
            self.getCitiesWithMostConnections();
        elif input == 6:
            self.visualizeNetwork()
        elif input == 7:
            self.updateNetworkInfo()
        elif input == 8:
            self.getJSON()
        elif input == 9:
            self.getRouteInformation()
        elif input == 10:
            return
            #getShortestDistance(g)
        else:
            print "Your input is not valid. Please enter correct number between '1 - 10'"
    def getStatisticalInformation(self):
        '''
        # Parses user input from statistical option section
        :param g: Graph
        :return:
        '''
        value = ''
        list = []
        list = self.getLongestEdge()
        value += 'A longest single flight is: from {} to {}, within distance of {} kms\n\n'.format(list[0], list[1],
                                                                                            list[2])
        list = self.getShortestEdge()
        value += 'A shortest single flight is: from {} to {}, within distance of {} kms\n\n'.format(list[0], list[1],
                                                                                             list[2])
        value += 'The average distance of all flight is: {}\n\n'.format(self.getAverageEdgeLength())
        value += 'The biggest city (by population) served by CSAir: {} , Population: {}\n\n'.format(
                self.getBiggestCityPopulation().name, self.getBiggestCityPopulation().population)
        value += 'The smallest city (by population) served by CSAir: {} , Population: {}\n\n'.format(
                self.getSmallestCity().name, self.getSmallestCity().population)
        value += ('The average size (by population) of all the cities served by CSAir: {}\n\n').format(
                self.findAverageSize())
        return value
    def getClosestNameForTravelInfo(self, vertex_name):
        '''
        Given a vertex name, figure out the closest name, or country name
        :return:
        '''
        # Compile a list of names for correction, manually checked
        if vertex_name in self.correction_list:
            correct_name = self.correction_list[vertex_name]
        else:
            correct_name = vertex_name
        # return teh correct name in lower case with space replaced by -
        return correct_name.lower().replace(" ", "-")
    def getCityInformation(self, vertex):
        '''
        # If user wants to know more information about specific city, this functions will be called
        # It will repeatedly ask correct input
        :param g: Graph
        :return:
        '''
        isFinished = False
        while isFinished is not True:
            #print('Please enter the name of the city:')
            if vertex is not None:
                string = vertex.getVertexInformation()
                for city_code in vertex.getAdjacency():
                    if city_code is not None:
                        city_name = self.getVertexByCode(city_code).name
                        string += "Name: " + city_name + ", Distance: " + str(vertex.getDistance(city_code)) + "\n"
                    else:
                        break
                return string
                break
            else:
                return ('It is not a valid city. Please enter a valid city name')
######################################################################################################################
# All Pair Shortest Paths using DP and its applications
######################################################################################################################
    def allPairShortestPaths(self):
        '''
        Algorithm will find all pair shortest paths in current network using Dynamic Programming
        :return: 2D array of all possible shortest paths
        '''
        # Initialize all the distances
        dist = {}
        for vertex_outer in self.vertices:
            dist[vertex_outer.code] = {}
            for vertex_inner in self.vertices:
                dist[vertex_outer.code][vertex_inner.code] = {}
                if vertex_inner.code == vertex_outer.code:
                    for k in range(0, len(self.vertices)):
                        dist[vertex_outer.code][vertex_inner.code][k] = 0
                else:
                    dist[vertex_outer.code][vertex_inner.code][0] = float('Inf')
        # Find all possible distances with at most k edges
        for k in range(1, len(self.vertices)):
            for vertex_outer in self.vertices:
                for vertex_inner in self.vertices:
                    if vertex_outer.code != vertex_inner.code:
                        dist[vertex_outer.code][vertex_inner.code][k] = float('Inf')
                    for neighbor_code in vertex_outer.getAdjacency():
                        # IF the edge is tense, then relax
                        if dist[vertex_outer.code][vertex_inner.code][k] > vertex_outer.getDistance(neighbor_code) + dist[neighbor_code][vertex_inner.code][k-1]:
                            dist[vertex_outer.code][vertex_inner.code][k] = vertex_outer.getDistance(neighbor_code) + dist[neighbor_code][vertex_inner.code][k-1]
        # Need only the minimal distance using at most V-1 edges
        distances = {}
        for vertex_outer in self.vertices:
            distances[vertex_outer.code] = {}
            for vertex_inner in self.vertices:
                distances[vertex_outer.code][vertex_inner.code] = dist[vertex_outer.code][vertex_inner.code][len(self.vertices) -1]
                #print "{} to {}, distance: {}".format(vertex_outer.code, vertex_inner.code, distances[vertex_outer.code][vertex_inner.code])
        # return the distances
        return distances
    def travelAround7Wonders(self, startCity_code):
        '''
        Find shortest route to travel from startCity through 7 wonders
        :param startCity_code:
        :return: list in order of which to travel and distances for each route
        '''
        # Find all possible shortest paths
        distances = self.allPairShortestPaths()
        # Generate list of 7 cities, where 7 wonders are located
        list = ['SAO', 'LIM', 'MEX', 'MIL', 'CAI', 'DEL','PEK']
        # order is order on how to go from start to finish
        order = []
        while len(list) != 0:
            closestCity_code = self.findClosestFromList(startCity_code, list, distances)
            # push the current distance
            order.append([startCity_code, closestCity_code, distances[startCity_code][closestCity_code]])
            # remove the closestCity
            list.remove(closestCity_code)
            # now the closest city is starting point
            startCity_code = closestCity_code
        return order

    def findClosestFromList(self, startCity_code, list, distances):
        '''
        Helper function to find closest city to startCity from the given list of cities
        :param startCity_code:
        :param list:
        :return:
        '''
        min_distance = float('Inf')
        closest_vertex_code = None
        for vertex_code in list:
            if self.getVertexByCode(vertex_code) is not None:
                if distances[startCity_code][vertex_code] < min_distance:
                    min_distance = distances[startCity_code][vertex_code]
                    closest_vertex_code = vertex_code
            else:
                print "Currently there is no such city {} in the system".format(vertex_code)
        # At this point, I have found my closest distance
        return closest_vertex_code
    def getRouteImageURL(self, list):
        '''
        Given a list of cities, get the image and return it
        :param list: [[vertex1, vertex2], [vertex2, vertex3], ... ]
        :return: return the image URL
        '''
        URL = "http://www.gcmap.com/map?P="
        for route in list:
            URL = URL + '+' + route[0] + '-' + route[1] + ','
        # We have extra + very first ,and extra , at the very end
        correctURL = URL[:27] + URL[28:len(URL) - 1]
        correctURL += '&MS=wls&MR=1800&MX=720x360&PM=%2a'
        # For picturing the graph on the browser
        #webbrowser.open(correctURL, new=new)
        return correctURL
#######################################################################################################################
# Minimal spanning tree
#######################################################################################################################
    def Kruskal(self):
        '''
        Computes minimal spanning tree of the current graph using Kruskal algorithm
        :return:
        '''
        # set of minimim spanning tree
        set = []
        # Disjoint set
        disjointSet = DisjointSet.DisjointSet()
        for vertex in self.vertices:
             disjointSet.makeSet(vertex)
        # Get all edges in increasing order
        ordered_edges = self.getOrderedEdges()
        for edge in ordered_edges:
            source = edge[0]
            destination = edge[1]
            # If they are not in same set, merge
            if disjointSet.find(source) != disjointSet.find(destination):
                set = set.append(edge)
                disjointSet.union(source, destination)
        # Return the set of edges
        return set

    def getOrderedEdges(self):
        '''
        Get ordered list of edges from given graph
        :return:
        '''

