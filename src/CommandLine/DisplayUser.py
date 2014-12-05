__author__ = 'luvsandondov'

# #######################################################################################################################
# Helper functions to display options to user
########################################################################################################################
class DisplayUser:
    def askUser(self):
        '''
        Ask user repeatedly from the given options
        :return: String of all possible inputs
        '''
        return ('Please enter the input from following options: \n'
                '1. A list of all the cities that CSAir flies to \n'
                '2. A specific information about a specific city in the CSAir route network.\n'
                '3. Get statistical information about the CSAir route network. \n'
                '4. A list of the continents served by CSAir and which cities are in them \n'
                '5. Identifying CSAir"s hub cities the cities that have the most direct connections. \n'
                '6. Visualize CSAir"s network. \n'
                '7. Update the network. \n'
                '8. Get JSON format file from current network. \n'
                '9. Get the route information. \n'
                '10. Get the shortest path from source to destination. \n')

    def displayStatisticalOptions(self):
        '''
        # Display options for getting stats
        :return:
        '''
        print ( 'Please enter the number from following options:\n'
                '1. The longest single flight in the network \n'
                '2. The shortest single flight in the network \n'
                '3. The average distance of all the flights in the network \n'
                '4. The biggest city (by population) served by CSAir \n'
                '5. The smallest city (by population) served by CSAir \n'
                '6. The average size (by population) of all the cities served by CSAir \n')
    def displayUpdateNetworkList(self):
        '''
        # Display options for updating network
        :return:
        '''
        print ('Please enter the input from following options: \n'
               '1. Remove a city  \n'
               '2. Remove a route.\n'
               '3. Add a city, including all its necessary information \n'
               '4. Add a route, including all its necessary information \n'
               '5. Edit an existing city \n')


    def updateNetworkInfo(self, g):
        '''
        #Function to parse user input, when user chooses to update current network
        :param g: Graph of the network
        :return:
        '''
        self.displayUpdateNetworkList()
        input = int(raw_input())
        if input == 1:
            print "Please enter the city name: "
            city_name = raw_input()
            vertex = g.getVertexByName(city_name)
            g.removeVertex(vertex.code)
        elif input == 2:
            print "Please enter the two cities names to remove the route between in [source,, destination] form: "
            list = raw_input().split(",, ")
            src_name = list[0]
            dest_name = list[1]
            g.getVertexByName(src_name).removeEdge(g.getVertexByName(dest_name).code)
        elif input == 3:
            print "Please enter city information, separated by ',, '"
            list = raw_input().split(",, ")
            print list
            g.addVertex(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7])
        elif input == 4:
            print "Please enter the two cities names to add the route between in [source,, destination,, distance] form: "
            list = raw_input().split(",, ")
            src_name = list[0]
            dest_name = list[1]
            distance = list[2]
            g.getVertexByName(src_name).addEdge(g.getVertexByName(dest_name).code, float(distance))
        elif input == 5:
            print "Please enter city information editing, separated by ',, '"
            list = raw_input().split(",, ")
            g.updateVertex(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7])

