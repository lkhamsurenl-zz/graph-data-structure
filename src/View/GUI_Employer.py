import copy
from src.Controller.RandomizedMinCut import RandomizedMinCut

__author__ = 'luvsandondov'

from src.Controller import Flow
from src.Model import Graph
from src.View import GUI_TicTacToe, GUI

from PIL import Image, ImageTk
from Tkconstants import BOTH, END, BROWSE, ANCHOR
import tkMessageBox
import tkSimpleDialog
import Tkinter as tk
import urllib


class GUI_Employer(tk.Frame):
    '''
    This class will construct all necessary GUI parts for the two softwares
    '''
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        json_data_list = []
        json_data_list.append('../../resources/data/data.json')
        json_data_list.append('../../resources/data/additional_data.json')
        # Pass the list of the json_data
        self.g = Graph.Graph(json_data_list)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        '''
        Display contents of the user options
        :return:
        '''
        # list of cities
        self.list = tk.Listbox(self, selectmode=BROWSE)
        for vertex in self.g.vertices:
            self.list.insert(END, vertex.name)
        self.list.pack(fill=BOTH, expand=1)
        self.list.config(height = 31)
        self.list.bind("<Double-Button-1>", self.poll)
        self.removeCityButton = tk.Button(self, text="Remove City",
          command=self.removeCity)
        # Get image
        self.photo = ImageTk.PhotoImage(file= "../../resources/icon/net.gif")
        self.imageButton = tk.Button(self, image = self.photo)
        self.createSecretInfoButtons()
        # Update network part
        self.createUpdateNetworkButtons()
        # Display all buttons
        self.displayWidgets()
#######################################################################################################################
# Set up the buttons
#######################################################################################################################
    def createSecretInfoButtons(self):
        self.gameButton = tk.Button(self, text="Back To Work", command=self.playGame)
        self.getScheduleButton = tk.Button(self, text='Schedule Information', command=self.getSchedule)
        self.getRandMinCutButton = tk.Button(self, text='008 Chris', command=self.getRandMinCut)
        self.getnetworkImageButton = tk.Button(self, text='Get network image', command=lambda: GUI.getNetworkPicture(self))
        self.getShortestPathButton = tk.Button(self, text='Get Shortest Path', command=lambda: GUI.getShortestDistance(self))
        self.getRouteInfoButton = tk.Button(self, text='Get Route Information', command=lambda :GUI.getRouteInfo(self))

    def createUpdateNetworkButtons(self):
        '''
        Helper function to create buttons for updating network
        :return:
        '''
        # Edit network
        self.removeRouteButton = tk.Button(self, text= 'Remove Route', command = self.removeRoute)
        self.addCityButton = tk.Button(self, text= 'Add City', command = self.addCity)
        self.addRouteButton = tk.Button(self, text= 'Add Route', command = self.addRoute)
        self.editCityButton = tk.Button(self, text= 'Edit City', command = self.editCity)
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.getJSONButton = tk.Button(self, text= 'Get Json', command = self.getJSON)

    def displayWidgets(self):
        # display the widgets
        self.list.grid(row = 0, column = 3, rowspan = 6)
        self.imageButton.grid(row = 0, column = 0, columnspan = 3)
        self.getScheduleButton.grid(row = 1, column = 1)
        self.getRandMinCutButton.grid(row = 1, column = 2)

        self.addCityButton.grid(row =2, column = 0)
        self.addRouteButton.grid(row =2, column = 1)
        self.editCityButton.grid(row =2, column = 2)

        self.removeCityButton.grid(row =3, column = 0)
        self.removeRouteButton.grid(row =3, column = 1)
        self.getJSONButton.grid(row = 3, column = 2)

        self.getnetworkImageButton.grid(row = 4, column = 0)
        self.getShortestPathButton.grid(row =4, column = 1)
        self.getRouteInfoButton.grid(row=4, column = 2)

        self.quitButton.grid(row =5, column = 1)
        self.gameButton.grid(row =5, column = 0)
#######################################################################################################################
    # Helper functions for GUI
#######################################################################################################################
    def getRandMinCut(self):
        '''
        Computes Min Cut in the graph with high probability
        :return: value of the min cut
        '''
        # Make a copy of the original graph, because randomized min cut algorithm will modify the current network
        graph = copy.deepcopy(self.g)
        minCut = RandomizedMinCut(graph)
        # Run randomized min cut algorithm 10 times and get minimal value from all runs (Amplification)
        tkMessageBox.showinfo('Destroy CSAir', minCut.ComputeRandomMinCutRepeatedly(graph, 10))
        #tkMessageBox.showinfo('Destroy CSAir', minCut.ComputeRandomizedMinCut(graph))

    def getJSON(self):
        '''
        Helper function to get JSON file from current network, by asking user name of the file
        :return:
        '''
        name = tkSimpleDialog.askstring("File Name" ,"Please enter file name")
        self.g.getJSON(name)

    def playGame(self):
        # Create a instance if TicTacToe game
        gameGUI = GUI_TicTacToe.GUI_TicTacToe()
        #game = TicTacToe.TicTacToe()

    def addCity(self):
        # Display dialog to get user input
        # Code
        code = tkSimpleDialog.askstring("City code" ,"Please enter city code")
        if code is None or len(code) is not 3 or self.g.getVertexByCode(code) is not None:
            if code is not None: tkMessageBox.showwarning("Code invalid", "City code is not valid")
            return
        # Name
        name = tkSimpleDialog.askstring("City name", "Please enter city name:")
        if name is None or self.g.getVertexByName(name) is not None:
            if name is not None: tkMessageBox.showwarning("Name invalid", "City name is not valid")
            return
        # Country
        country = tkSimpleDialog.askstring("City country" , "Please enter country where the city is located:")
        if country is None: return
        # Country
        continent = tkSimpleDialog.askstring("City continent" ,"Please enter continent where the city is located:")
        if continent is None or (continent not in ["Asia", "Europe", "North America", "South America", "Australia", "Africa"]):
            if continent is not None: tkMessageBox.showwarning("Continent invalid", "Continent name is not valid")
            return
        # Timezone
        timezone = tkSimpleDialog.askstring("City timezone" ,"Please enter the timezone:")
        if timezone is None: return
        # Coordinates
        coordinates = tkSimpleDialog.askstring("City coordinates" ,"Please enter coordinates where the city is located:")
        if coordinates is None: return
        # Population
        population = tkSimpleDialog.askstring("City population" ,"Please enter city population:")
        if population is None or population < 0:
            if population is not None: tkMessageBox.showwarning("Population invalid", "Population is not valid")
            return
        # Region
        region = tkSimpleDialog.askstring("City region" ,"Please enter the region:")
        if coordinates is None: return
        self.g.addVertex(code, name , country, continent, timezone, coordinates, population, region)
        # Add city to the list
        self.list.insert(END, name)

    def addRoute(self):
        '''
        Adds a route between two cities, with option to go both directions
        :return:
        '''
        # Source city
        source_name = tkSimpleDialog.askstring("Source name" ,"Please enter the source city")
        if source_name is None or self.g.getVertexByName(source_name) is None:
            if source_name is not None: tkMessageBox.showwarning("Name invalid", "City is not in current Network")
            return
        # Destination city
        dest_name = tkSimpleDialog.askstring("Destination name" ,"Please enter the destination city")
        if dest_name is None or self.g.getVertexByName(dest_name) is None:
            if source_name is not None: tkMessageBox.showwarning("Name invalid", "City is not in current Network")
            return
        # Distance
        distance = tkSimpleDialog.askstring("Distance" ,"Please enter distance")
        if distance is None or distance < 0:
            if distance  < 0: tkMessageBox.showwarning("Distance invalid", "Distance cannot be negative")
            return
        # Add reverse direction only if user says yes to both direction
        if tkMessageBox.askyesno("Both ways", "Do you want to add this route both ways?"):
            self.g.getVertexByName(dest_name).addEdge(self.g.getVertexByName(source_name).code, float(distance))
        self.g.getVertexByName(source_name).addEdge(self.g.getVertexByName(dest_name).code, float(distance))
    def removeCity(self):
        '''
        Remove currently selected vertex
        :return:
        '''
        current_sel  = self.list.curselection()
        if current_sel != ():
            city_name = self.list.get(current_sel)
            vertex = self.g.getVertexByName(city_name)
            self.g.removeVertex(vertex.code)
            self.list.delete(ANCHOR)
        else:
            tkMessageBox.showwarning("City invalid", "Please select a city from list to remove")
    def removeRoute(self):
        '''
        Removes a route between two cities, with option to remove both directions
        :return:
        '''
        # Source vertex
        source_name = tkSimpleDialog.askstring("Source name" ,"Please enter the source city")
        if source_name is None or self.g.getVertexByName(source_name) is None:
            if source_name is not None: tkMessageBox.showwarning("Name invalid", "City is not in current Network")
            return
        # Destination city
        dest_name = tkSimpleDialog.askstring("Destination name" ,"Please enter the destination city")
        if source_name is None or self.g.getVertexByName(source_name) is None:
            if source_name is not None: tkMessageBox.showwarning("Name invalid", "City is not in current Network")
            return
        # Add reverse direction only if user says yes to both direction
        if tkMessageBox.askyesno("Both ways", "Do you want to remove this route both ways?"):
            self.g.getVertexByName(dest_name).removeEdge(self.g.getVertexByName(source_name).code)
        self.g.getVertexByName(source_name).removeEdge(self.g.getVertexByName(dest_name).code)
    def editCity(self):
        '''
        Edit currently existing city information
        :return:
        '''
        current_sel  = self.list.curselection()
        if current_sel == ():
            tkMessageBox.showwarning("Select city", "Please select a city from a list to edit")
        else:
            city_name = self.list.get(current_sel)
            vertex = self.g.getVertexByName(city_name)
            # Name
            name = tkSimpleDialog.askstring("City name", "Please enter city name, or click cancel to not update")
            if name is None or self.g.getVertexByName(name) is not None:
                if name is not None: tkMessageBox.showwarning("Name invalid", "City name is not valid")
                name = vertex.name
            else:
                # We update the display name for this city
                self.list.delete(ANCHOR)
                self.list.insert(END, name)
            # Country
            country = tkSimpleDialog.askstring("City country" , "Please enter country where the city is located, or click cancel to not update")
            if country is None:
                country = vertex.country
            continent = tkSimpleDialog.askstring("City continent" ,"Please enter continent where the city is located, or click cancel to not update")
            if continent is None or (continent not in ["Asia", "Europe", "North America", "South America", "Australia", "Africa"]):
                if continent is not None: tkMessageBox.showwarning("Continent invalid", "Continent name is not valid")
                continent = vertex.continent
            # Timezone
            timezone = tkSimpleDialog.askstring("City timezone" ,"Please enter the timezone, or click cancel to not update")
            if timezone is None: timezone = vertex.timezone
            # Coordinates
            coordinates = tkSimpleDialog.askstring("City coordinates" ,"Please enter coordinates where the city is located, or click cancel to not update")
            if coordinates is None: coordinates = vertex.coordinates
            # Population
            population = tkSimpleDialog.askstring("City population" ,"Please enter city population, or click cancel to not update")
            if population is None or population < 0:
                if population is not None: tkMessageBox.showwarning("Population invalid", "Population is not valid")
                population = vertex.population
            # Region
            region = tkSimpleDialog.askstring("City region" ,"Please enter the region, or click cancel to not update")
            if region is None: region = vertex.region
            # Then update vertex info with new information
            self.g.updateVertex(vertex.code, name, country, continent, timezone, coordinates, population, region)

    def getSchedule(self):
        '''
        Dialog to display continental information
        :return:
        '''
        source_name = tkSimpleDialog.askstring("City name", "Please enter source city name")
        if source_name is None or self.g.getVertexByName(source_name) is None:
            if source_name is not None: tkMessageBox.showwarning("Name invalid", "City name is not valid")
            return
        dest_name = tkSimpleDialog.askstring("City name", "Please enter destination city name")
        if dest_name is None or self.g.getVertexByName(dest_name) is None:
            if dest_name is not None: tkMessageBox.showwarning("Name invalid", "City name is not valid")
            return
        source_code = self.g.getVertexByName(source_name).code
        dest_code = self.g.getVertexByName(dest_name).code
        flow = Flow.Flow(self.g)
        tkMessageBox.showinfo('Schedule Information', flow.min_cut(source_code, dest_code))

    def poll(self, event):
        '''
        Act on the current selection of city
        '''
        current_sel  = self.list.curselection()
        if current_sel != ():
            city_name = self.list.get(current_sel)
            self.option_selected(city_name)

    def option_selected(self, city_name):
        '''
        Helper function to get selected city_name
        :param city_name:
        :return:
        '''
        vertex = self.g.getVertexByName(city_name)
        # create new widget
        GUI.createCityInfo(self, vertex)


def main():

    root = tk.Tk()
    root.title("Internal CSAir")
    #app = GUI_Employer.GUI_Employer(root)
    # NOTE: Comment it out and replace with above line when using released version
    app = GUI_Employer(root)
    root.mainloop()

if __name__ == '__main__':
    main()
