__author__ = 'luvsandondov'

import urllib2
import requests
from bs4 import BeautifulSoup
import tkSimpleDialog
import webbrowser
from PIL import ImageTk
import Image
from Tkconstants import BOTH, END, BROWSE, ANCHOR
import tkMessageBox
import Tkinter as tk
import urllib
# Some shared code resides here
def click_link(event, link):
    # open a link in new tab
    webbrowser.open(link, new=2)


def createCityInfo(self, vertex):
    '''
    Create a dialog with city information
    :param self: GUI_Employer or GUI_Customer
    :param vertex: Selected vertex
    :return:
    '''
    root = tk.Toplevel()
    # tkMessageBox.showinfo('City Information', self.g.getCityInformation(vertex))
    # Modify the current message box to be a dialog so that I can bind the city to the more info on the website
    modified_name = self.g.getClosestNameForTravelInfo(vertex.name)
    city_name = tk.Label(root, text="{}\n".format(vertex.name), foreground="#0000ff", font="-weight bold")
    city_name.bind("<1>", lambda event, text="More on city": \
        click_link(event, "http://www.worldtravelguide.net/{}".format(modified_name)))
    city_name.grid(row=0, column=0)
    # Show the city information
    city_info = tk.Label(root, text=self.g.getCityInformation(vertex))
    city_info.grid(row=1, column=0)

def getRouteInfo(self):
    '''
    Shows specific route information
    :return:
    '''
    list = tkSimpleDialog.askstring("Route cities", "Please enter list of cities in the route, separated by ', '")
    list = list.split(", ")
    self.getRouteInfoFromList(self.g, list)


def getShortestDistance(self):
    '''
    # Function to get call SSSP after asking user for source and destination cities
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

    source = self.g.getVertexByName(source_name)
    dest = self.g.getVertexByName(dest_name)

    self.g.findSSSP(source)
    list = []
    current_vertex = dest
    while current_vertex is not source:
        list.append(current_vertex.name)
        current_vertex = current_vertex.pred
    list.append(current_vertex.name)
    # then we reverse the list
    list.reverse()
    # DEGGING
    print list
    # DEBUGGING
    self.g.getRouteInfoFromList(list)


def getNetworkPicture(self):
    '''
    Display network route
    NOTE: not dynamic picture for now
    :return:
    '''
    # Get the top level
    root = tk.Toplevel()
    # Based on the current network, get the image
    URL = self.g.visualizeNetwork()
    urllib.urlretrieve(URL, "network.gif")
    # Display it
    image = Image.open("../../resources/icon/map.gif")
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=photo)
    label.image = photo  # keep a reference!
    label.pack()
    root.mainloop()



