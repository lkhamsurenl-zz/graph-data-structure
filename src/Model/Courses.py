import json
from src.Model import Graph

__author__ = 'luvsandondov'

import urllib2
import requests
from bs4 import BeautifulSoup

class Courses:
    '''
    Class to initialize all CS classes, and build graph
    '''
    def __init__(self):
        # NOTE: Use following 3 line only once to build json_file and not to load it every time I open the app
        #list = self.__load_classes__()
        #self.__build_JSON__(list)
        # Initialize the graph
        self.graph = Graph.Graph(["../../resources/data/classes.json"])
        # NOTE: Use following code only once
        # get Dr.Everitt Neighborhood description
        #self.__getDesc__()

    def __load_classes__(self):
        #url = "http://www.cs.illinois.edu/courses/profile/CS173"
        list_of_classes = {}
        list_of_class_names = {}
        # Holds all classes as a dictionary
        soup = BeautifulSoup(urllib2.urlopen("https://courses.cites.illinois.edu/schedule/2015/spring/CS"))
        for classes in soup.find_all("table", id = "default-dt"):
            for links in  classes.find_all("a"):
                # For each class, create list of neighbors
                list_of_classes[links['href'][25:]] = []

        # For each class above, we get all prerequisites:
        for class_code in list_of_classes.keys():
            soup = BeautifulSoup(urllib2.urlopen("https://courses.cites.illinois.edu/schedule/2015/spring/CS/{}".format(class_code)))
            # Get course prereqs
            for class_name in soup.find_all("div", id = "app-course-info"):
                para =  class_name.find_all("p")[2]
                for req in  para.find_all("a"):
                    # NOTE: Ignoring non-cs requirements. Can extend it as requested
                    #print req.text[3:]
                    if req.text[:3] == "CS " and class_code != req.text[3:]:
                        list_of_classes[class_code].append(req.text[3:])
            # Get course name:
            for class_title in soup.find_all("span", {"class":"app-label app-text-engage"}):
                list_of_class_names[class_code] = class_title.text
        return [list_of_classes, list_of_class_names]

    def __build_JSON__(self, list):
        '''
        Get JSON file based on list_of_classes
        :return:
        '''
        list_of_classes = list[0]
        list_of_class_names = list[1]
        data = {"metros": [], "routes" : []}
        for vertex in list_of_classes:
            for neighbor_code in list_of_classes[vertex]:
                ports = [vertex, neighbor_code]
                new_route = {"ports": ports, "distance": 1}
                curr = data.get("routes")
                curr.append(new_route)
                data["routes"] = curr
            # We add this vertex
            new_node = {"code": vertex, "name": list_of_class_names[vertex], "country": None, "continent": None
                , "timezone": None, "coordinates": None, "population": None,
                        "region": None}
            curr_metros = data.get("metros")
            curr_metros.append(new_node)
            data["metros"] = curr_metros
        with open('../../resources/data/classes.json', 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)

        # Get all course names

    def __getDesc__(self):
        '''
        Scrap Everitt website, and stores JSON data
        :return:
        '''
        data = {"metros": []}
        # For each class above, we get all prerequisites:
        for vertex in self.graph.vertices:
            class_code = vertex.code
            # Access Dr.Everitt's Neighborhood
            try:
                soup = BeautifulSoup(urllib2.urlopen("https://wiki.cites.illinois.edu/wiki/display/HKNDEN/CS+{}+-+{}"
                                                     .format(class_code, vertex.name.replace(" ", "+"))))
                list = soup.find_all("p")
                # BUild JSON file from above data
                new_node = {"code": class_code, "work": list[len(list) -2 ].text,
                        "lifeAfter": list[len(list) -1].text}
                curr_metros = data.get("metros")
                curr_metros.append(new_node)
                data["metros"] = curr_metros
                print list[len(list) -2 ].text
                print list[len(list) -1].text
            except:
                pass         # There is no such website exist to open
        # Dump into JSON file:
        with open('../../resources/data/classes_content.json', 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)


Courses()


