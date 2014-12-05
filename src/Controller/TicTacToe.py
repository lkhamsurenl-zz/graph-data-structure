__author__ = 'luvsandondov'

class TicTacToe:
    '''
    Controller of the Tic Tac Toe game
    '''
    # In order to generalize the game, only need to change following numbers:
    def col_size(self):
        return 9
    def board_size(self):
        return self.col_size() * self.col_size()
    def row_size(self):
        return self.col_size()

    def __init__(self):
        self.board = [] # Represent the board
        for i in range(0,self.board_size()):
            self.board.append(-1)
        # Represent the cell numbers which can be winning streak
        self.possibleWinCells = self.getPossibleWinCells()

    def move(self, cell, turn):
        self.board[cell] = turn
        return self.isFinished(cell)

    def isFinished(self, cell):
        '''
        Check if the game is finished, given the last movement was cell
        :return: -1 if no winner, else return the winner side's turn
        '''
        for possibleWinCell in self.possibleWinCells:
            if cell in possibleWinCell and self.allSameColors(possibleWinCell):
                return self.board[possibleWinCell[0]]
        # There could be no more movement, return 1
        if -1 not in self.board:
            return 1
        #Otherwise there is no winner
        return -1

    def getPossibleWinCells(self):
        '''
        Creates all possible ways to win the game
        :return:
        '''
        lists = []
        for i in range(0, self.row_size()):
            col_list = []
            for j in range(0, self.col_size()):
                col_list.append(i+j)
            # add this col way to win into lists
            lists.append(col_list)
        for j in range(0, self.col_size()):
            row_list = []
            for i in range(0, self.row_size()):
                row_list.append(i*self.col_size() + j)
            # add this col way to win into lists
            lists.append(row_list)
        # Then also there is diagonal ways to win
        ascend_diagonal = []
        for i in range(1, self.col_size()+1):
            ascend_diagonal.append((self.row_size() -1 ) * i)
        lists.append(ascend_diagonal)
        # Descend
        descend_diagonal = []
        for i in range(0, self.col_size()):
            descend_diagonal.append(i* (self.col_size() + 1))
        lists.append(descend_diagonal)
        return lists

    def allSameColors(self, possibleWinCell):
        '''
        Returns true if all letters in possibleWinCell are same
        :param possibleWinCell:
        :return:
        '''
        color = self.board[possibleWinCell[0]] # They all should be same as color
        for i in possibleWinCell:
            if self.board[i] != color:
                return False
        return True



