__author__ = 'luvsandondov'

from PIL import ImageTk
import Image
from Tkconstants import BOTH, END, BROWSE
import tkMessageBox
import Tkinter as tk
import urllib

from src.Model import Graph
from src.View import Login, GUI


class GUI_Customer(tk.Frame):
    '''
    This class will construct all necessary GUI parts for the two softwares
    '''
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        json_data_list = []
        json_data_list.append('../../resources/data/data.json')
        json_data_list.append('../../resources/data/additional_data.json')
        # For the test data purpose
        #json_data_list.append('output.json')
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
        self.list.config(height = 23)
        self.list.bind("<Double-Button-1>", self.poll)
        # Get image
        self.photoCS = ImageTk.PhotoImage(file= "../../resources/icon/CSAir.jpg")
        self.imageButton = tk.Button(self, image = self.photoCS, command = self.secret)
        self.createStatisticalInfoButtons()
        # Update network part
        self.createUpdateNetworkButtons()
        # Display all buttons
        self.displayWidgets()
#######################################################################################################################
# Set up the buttons
#######################################################################################################################
    def createStatisticalInfoButtons(self):
        # Get stats
        self.statsButton = tk.Button(self, text='Get statistical info', command=self.getStats)
        # get Continents
        self.continentsButton = tk.Button(self, text='Get continents info', command=self.getContinents)
        self.hubCitiesButton = tk.Button(self, text='Get hub city info', command=self.getHubCities)
        self.getnetworkImageButton = tk.Button(self, text='Get network image', command=lambda: GUI.getNetworkPicture(self))
        self.getShortestPathButton = tk.Button(self, text='Get Shortest Path', command=lambda: GUI.getShortestDistance(self))
        self.getRouteInfoButton = tk.Button(self, text='Get Route Information', command=lambda :GUI.getRouteInfo(self))

    def createUpdateNetworkButtons(self):
        '''
        Helper function to create buttons for updating network
        :return:
        '''
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.get7WondersButton = tk.Button(self, text='See 7 Wonders', command=self.get7WondersTravel)

    def displayWidgets(self):
        # display the widgets
        self.list.grid(row = 0, column = 3, rowspan = 6)
        self.imageButton.grid(row = 0, column = 0, columnspan = 3)

        self.statsButton.grid(row = 1, column = 0)
        self.continentsButton.grid(row = 1,  column = 1)
        self.hubCitiesButton.grid(row = 1, column = 2)

        self.getnetworkImageButton.grid(row = 2, column = 0)
        self.getShortestPathButton.grid(row =2, column = 1)
        self.getRouteInfoButton.grid(row=2, column = 2)

        self.quitButton.grid(row =3, column = 2)
        self.get7WondersButton.grid(row=3, column = 1)
#######################################################################################################################
    # Helper functions for GUI
#######################################################################################################################

    def __processOrder7Wonders__(self, vertex):
        # Get the order to travel around the world
        order = self.g.travelAround7Wonders(vertex.code)
        string = []
        names = []
        total_distance = 0
        for route in order:
            source_code = route[0]
            dest_code = route[1]
            distance = route[2]
            string.append("{} to {}, travel {} kms to see {}\n\n"
                          .format(self.g.getVertexByCode(source_code).name, self.g.getVertexByCode(dest_code).name,
                                  distance, self.g.getVertexByCode(dest_code).getWonder()[0]))
            names.append(self.g.getVertexByCode(dest_code).getWonder()[1])
            # add to the total distance
            total_distance += distance
        # Get the image URL representing this travel
        imageURL = self.g.getRouteImageURL(order)
        return [string, names, imageURL, total_distance]

    def get7WondersRouteImage(self, URL, root):
        '''
        Function generates the image represnting the route around 7 wonders of the world
        :param URL: URL of the image
        :param root: root of the Tkinter
        :return:
        '''
        # Show the title of the image as a label
        label_title = tk.Label(root, text="Travel Image", font=("Helvetica", 16))
        label_title.grid(row = 0, column = 1)
        # retrieve the image
        urllib.urlretrieve(URL, "../../resources/icon/7wonders.gif")
        image = Image.open("../../resources/icon/7wonders.gif")
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(root, image=photo)
        label.image = photo # keep a reference!
        label.grid(row = 1, column = 1, rowspan = 10)
        # Also include general description
        more_text = tk.Label(root, text="More on 7 wonders \n", foreground="#0000ff")
        more_text.bind("<1>", lambda event, text="More on 7 Wonders": \
                              GUI.click_link(event, "http://www.mapsofworld.com/world-seven-wonders.htm"))
        more_text.grid(row = 12, column = 1)

    def get7WondersTravel(self):
        '''
        Helper function to call all pair shotest path algorithm and find short way to travel around 7 wonders
        :return:
        '''
        # Ask user for the initial point to start
        current_sel  = self.list.curselection()
        if current_sel != ():
            city_name = self.list.get(current_sel)
            vertex = self.g.getVertexByName(city_name)
            # process it iwth creating a label
            level = tk.Toplevel()
            # Get all the city names and descriptions, and imageURL
            citiesAndDesc = self.__processOrder7Wonders__(vertex)
            # Codes of the cities of wonders in order
            city_codes = citiesAndDesc[1]
            # City descriptions with where to where and distance in order
            city_descs = citiesAndDesc[0]
            # URL of the image of travel
            imageURL = citiesAndDesc[2]
            # For each route, I bind information on where the user is going
            for i in range(len(city_codes)):
                city_code = city_codes[i]
                city_desc = city_descs[i]
                label = tk.Label(level, text="Click here to see more\n", foreground="#0000ff")
                label.bind("<1>", lambda event, text=city_code: \
                              GUI.click_link(event, text))
                text = tk.Label(level, text = city_desc)
                text.grid(row = 2*i, column = 0)
                label.grid(row = 2*i+1, column = 0)
            # Display the image as well as stats on travel
            self.get7WondersRouteImage(imageURL, level)
            # Distance of travel
            label_stats = tk.Label(level, text="Total distance of the travel: {} kms".format(citiesAndDesc[3]), font=("Helvetica", 14))
            label_stats.grid(row = 11, column = 1)
        else:
            tkMessageBox.showwarning("City invalid", "Please select a city from list to start your Journey")

    def secret(self):
        # secret way to enter the internal system
        root = tk.Toplevel()
        login = Login.Login(root)
        root.destroy()

    def getStats(self):
        '''
        Dialog to display statical information about the network
        :return:
        '''
        tkMessageBox.showinfo('Statistical Infomation', self.g.getStatisticalInformation())
    def getContinents(self):
        '''
        Dialog to display continental infotmation
        :return:
        '''
        tkMessageBox.showinfo('Continental Infomation', self.g.getContinentalInformation())
    def getHubCities(self):
        '''
        Dialog to display continental information
        :return:
        '''
        tkMessageBox.showinfo('Hub Cities Infomation', self.g.getCitiesWithMostConnections())

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
    app = GUI_Customer(root)
    root.title("CSAir")
    root.mainloop()

if __name__ == '__main__':
    main()