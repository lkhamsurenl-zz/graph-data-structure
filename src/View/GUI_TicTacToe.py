import tkMessageBox
import tkFont
from src.Controller import TicTacToe


__author__ = 'luvsandondov'
import Tkinter as tk

class GUI_TicTacToe():
    '''
    Class represent GUI of the game
    '''

    def __init__(self):
        # Current window
        self.root = tk.Toplevel()
        self.root.title("Tic Tac Toe")
        # Initialize the Controller side
        self.board = TicTacToe.TicTacToe()
        # All 9 buttons
        self.buttons = []
        # create all buttons, and bind it with callback with its cell number as argument
        self.createButtons()
        # Keep track of whose turn
        self.turn = 0

        # Place the buttons
        for i in range(0,self.board.board_size()):
            self.buttons[i].grid(row = i/self.board.row_size(), column = i%self.board.col_size())

    def createButtons(self):
        for i in range(0, self.board.board_size()):
            # Used j here, otherwise lambda will only pick up last value of i, which is 8
            button = tk.Button(self.root, text=" ", command=lambda j = i: self.buttonClick(j), height = 3, width =3)
            self.buttons.append(button)

    def buttonClick(self, i):
        '''
        Change GUI and Contoller upon button click
        :param i: cell number
        :return:
        '''
        # Check if the cell was taken
        if self.buttons[i]['text'] != " ":
            tkMessageBox.showwarning("Move Invalid", "Not Valid Movement")
            return
        # otherwise make the turn
        if self.turn == 0:
            self.buttons[i]['text'] = "X"
            self.buttons[i]['bg'] = 'red'
            # change the turn
            self.turn = 1
            # Change the board
            winner = self.board.move(i, 'X')
        elif self.turn == 1:
            self.buttons[i]['text'] = "O"
            self.buttons[i]['bg'] = 'blue'
            # Change the turn
            self.turn = 2
            # Change the board
            winner = self.board.move(i, 'O')
        else:
            self.buttons[i]['text'] = "Y"
            self.buttons[i]['bg'] = 'green'
            # Change the turn
            self.turn = 0
            # Change the board
            winner = self.board.move(i, 'Y')

        # Finish game if it's is done
        if winner != -1:
            self.finishGame(winner)

    def finishGame(self, winner):
        '''
        Show the winner if there is one, and destroy the current window
        :param winner: winner side. 1 if there is no more movement
        :return:
        '''
        if winner ==1:
            tkMessageBox.showwarning("Draw", "No more possible movements")
        else:
            tkMessageBox.showwarning("Winner", "Hooray! {} has won".format(winner))
        # Close the current window
        self.root.destroy()



