from Tkconstants import NW, FLAT, BOTTOM, HORIZONTAL, X, VERTICAL, RIGHT, Y, LEFT, BOTH, CENTER, W, END
import json
import tkMessageBox

__author__ = 'luvsandondov'

import Tkinter as tk
from src.Model import Courses

class GUI_Courses(tk.Frame):
    '''
    Class to build GUI of the course network
    '''
    def __init__(self, master=None):
        self.root = master
        self.canvas = tk.Canvas(self.root, width = 1000, height = 700)
        self.canvas.pack()
        #self.canvas.create_rectangle(50, 25, 150, 75, fill="blue")
        # Controller:
        self.courses = Courses.Courses()
        # Keep track of all buttons
        self.buttons = {}
#for vertex in self.courses.graph.vertices:
#    print "{} : {}".format(vertex.code, vertex.getAdjacency())
        # Build the buttons for each class
        self.createCourseButtons()
        sorted_names = sorted(self.courses.graph.getVerticesCodes())
        #create buttons
        curr_x =30
        curr_y =30
        for i in range(0, len(sorted_names)):
            course_code = sorted_names[i]
            # If it's new hundred level class or current column is full, then increment
            if (i != 0 and sorted_names[i][0] != sorted_names[i-1][0]) or curr_y > 700:
#print "{} and {}".format(sorted_names[i-1], sorted_names[i])
                curr_x = curr_x + 150
                curr_y = 30
            # Create actual button
            #self.buttons[course_code].grid(row =course_code[0], column = curr_col, pady = 10)
            button_window = self.canvas.create_window(curr_x, curr_y, window = self.buttons[course_code][0])
            # Store actual location for each button
            # x location
            self.buttons[course_code].append(curr_x)
            # y location
            self.buttons[course_code].append(curr_y)
            # Increment row
            curr_y = curr_y + 50
        # Draw connections between them
        self.drawEdges()

    def createCourseButtons(self):
        '''
        Method to create all buttons for each classes
        :return:
        '''
        for course_code in self.courses.graph.getVerticesCodes():
            # NOTE: Usage of j is required here because i is shared across all buttons and will be used only for last i
            button = tk.Button(self.root, text="CS " + course_code, command=lambda j = course_code: self.buttonClick(j))
            button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            # buttons dictionary include button itself, and its x,y location on canvas as a list
            self.buttons[course_code] = []
            self.buttons[course_code].append(button)

    def drawEdges(self):
        '''
        Creates lines between buttons depending on the graph and buttons locations
        :return:
        '''
        for vertex in self.courses.graph.vertices:
            for neighbor_code in vertex.getAdjacency():
                #Create line from vertex to neighbor based on location saved on buttons
                self.canvas.create_line(self.buttons[vertex.code][1],self.buttons[vertex.code][2],
                                        self.buttons[neighbor_code][1], self.buttons[neighbor_code][2] )
                #pass

    def buttonClick(self, course_code):
        '''
        Function is called when the button is clicked
        :param course_code: course code
        :return:
        '''
        vertex = self.courses.graph.getVertexByCode(course_code)
        # Get all classes can take after this class:
        list_of_classes = self.getAdjacentClasses(vertex)
        # GET the content from JSON
        json_data = open("../../resources/data/classes_content.json")
        data = json.load(json_data)
        # Add all vertices first
        work = ""
        for city in data["metros"]:
            if city["code"] == course_code:
                work = city["work"]
                lifeAfter = city["lifeAfter"]
        if work == "":
            work = "Nothing has been posted"
            lifeAfter = "Nothing has been posted"
        # Display the content
        root = tk.Toplevel()
        S = tk.Scrollbar(root)
        T = tk.Text(root, height=10, width=100)
        S.pack(side=RIGHT, fill=Y)
        T.pack(side=LEFT, fill=Y)
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
        T.insert(END, "CS {}\n{} \n\n Work: \n{} \n\n LifeAfter:\n {} \n\n Classes You Can Take: \n{}"
                 .format(vertex.code, vertex.name, work, lifeAfter, list_of_classes))
        #tkMessageBox.showinfo('Course Information', "CS {} \n {}\n       Work       \n {} \n LifeAfter {}"
               # .format(vertex.code, vertex.name, work, lifeAfter))

    def getAdjacentClasses(self, vertex):
        '''
        Return all classes can take after this class in correct format
        :param vertex: vertex
        :return:
        '''
        list_of_classes = ""
        # Class code, followed by its name
        for neighbor_code in vertex.getAdjacency():
            neighbor = self.courses.graph.getVertexByCode(neighbor_code)
            list_of_classes += "CS {} - {}, ".format(neighbor_code, neighbor.name)
        # Strip out last ", " from actual string
        return list_of_classes[:len(list_of_classes)-2]

def main():

    root = tk.Tk()
    app = GUI_Courses(root)
    root.title("CSAir")
    root.mainloop()

if __name__ == '__main__':
    main()