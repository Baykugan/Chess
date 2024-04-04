from Chess_Pieces.Pieces import *

class Board():

    def __init__(self):
        self.turn = 1
        self.size = 8
        self.index = [[Empty(' ') for j in range(self.size)] for i in range(self.size)]

        self.index[0] = [Rook('B'), Knight('B'), Bishop('B'), Queen('B'),
                         King('B'), Bishop('B'), Knight('B'), Rook('B')]

        self.index[7] = [Rook('W'), Knight('W'), Bishop('W'), Queen('W'),
                         King('W'), Bishop('W'), Knight('W'), Rook('W')] 

        self.index[1] = [Pawn('B') for i in range(8)]
        self.index[6] = [Pawn('W') for i in range(8)]


    def __repr__(self):
        ret = ''
        ret += f'╔════╤════╤════╤════╤════╤════╤════╤════╗\n'
        for i in range(8):
            ret += f'║'
            for j in range(8):
                if self.index[i][j].empty and self.index[i][j].enPassant:
                    ret += f' EE '
                elif self.index[i][j].empty and self.index[i][j].takeable:
                    ret += f' XX '
                else:
                    ret += f' {self.index[i][j]} '
                if j != 7:
                    ret += f'│'
            ret += '║\n'
            if i != 7:
                ret += '╟────┼────┼────┼────┼────┼────┼────┼────╢\n'
        ret += f'╚════╧════╧════╧════╧════╧════╧════╧════╝\n'
        return ret

    def onBoard(self, index):
        row, col = index
        if 0 <= row <= self.size -1 and 0 <= col <= self.size - 1:
            return True

    def clearBoard(self):
        for row in range(self.size):
            for col in range(self.size):
                self.index[row][col].takeable = False
                self.index[row][col].moved = False


    def checkForCheck(self):
        global whiteInCheck, blackInCheck

        whiteInCheck = False
        blackInCheck = False
        
        allMoves = []
        for row in range(self.size):
            for col in range(self.size):
                piece = self.index[row][col]
                allMoves.append(piece.movement(self))

        allMoves = [pos for sub in allMoves for pos in sub]

        for pos in allMoves:
            if self.index[pos[0]][pos[1]].piece == 'K':
                if self.turn % 2 == 1 and self.index[pos[0]][pos[1]].team == 'W':
                    whiteInCheck = True
                    return True
                elif self.turn % 2 == 0 and self.index[pos[0]][pos[1]].team == 'B':
                    blackInCheck = True
                    return True
        return False


    def checkForMate(self):
        checkMate = True
        for row in self.index:
            for pos in row:
                if not pos.empty:
                    if pos.team == 'W' and self.turn % 2 == 1:
                        haveMoves = pos.getMoves()
                    elif pos.team == 'B' and self.turn % 2 == 0:
                        haveMoves = pos.getMoves()
                    else:
                        haveMoves = False
                    if haveMoves:
                        checkMate = False
        return checkMate
    
    def checkTurn(self, index):

        row, col = index
        if self.turn % 2:
            if self.index[row][col].team == 'W':
                return True
        else:
            if self.index[row][col].team == 'B':
                return True


    def updateIndex(self):
        for i in range(self.size):
            for j in range(self.size):
                self.index[i][j].index = (i, j)