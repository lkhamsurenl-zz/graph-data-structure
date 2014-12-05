from Tkinter import Label, Entry
import Tkinter as tk
import tkMessageBox
from src.View import GUI_Employer

__author__ = 'luvsandondov'
import tkSimpleDialog

class Login(tkSimpleDialog.Dialog):

    def body(self, master):
        Label(master, text="Username:").grid(row=0)
        Label(master, text="Password:").grid(row=1)

        self.e1 = Entry(master)
        self.e2 = Entry(master, show="*")

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus

    def apply(self):
        username = self.e1.get()
        password = self.e2.get()
        if "csair.com" in username and "mr.yang" in password:
            root = tk.Toplevel()
            GUI_Employer.GUI_Employer(root)
        else:
            tkMessageBox.showwarning("Not Authorized", "You do not have a permission")

