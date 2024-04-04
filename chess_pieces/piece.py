

class Piece():

    def __init__(self, team):
        self.team = team
        self.takeable = False
        self.moved = False
        self.index = ()
        self.moves = []
        self.empty = False


    def __repr__(self):
        return self.team + self.piece
 

    def movement(self, board):
        raise NotImplementedError('subclasses must override movement()')
    

    def getMoves(self, board):
        self.movement(board)
        haveMoves = False
        for pos in self.moves:
            if self.checksSelf(board, pos) == False:
                haveMoves = True
                board.index[pos[0]][pos[1]].takeable = True
        return haveMoves
    

    def checksSelf(self, board, index):
        from Chess_Pieces.Empty import Empty

        global blackInCheck, whiteInCheck
        row, col = self.index
        newRow, newCol = index
        temp = board.index[newRow][newCol]
        
        board.index[newRow][newCol] = board.index[row][col]
        board.index[row][col] = Empty(' ')

        ret = board.checkForCheck()

        board.index[row][col] = board.index[newRow][newCol]
        board.index[newRow][newCol] = temp

       
        if ret and board.index[row][col].team == 'W':
            return True
        elif ret and board.index[row][col].team == 'B':
            return True

        return False