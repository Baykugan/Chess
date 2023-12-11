import pygame

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
    

    def getMoves(self):
        self.movement()
        haveMoves = False
        for pos in self.moves:
            if self.checksSelf(pos) == False:
                haveMoves = True
                board.index[pos[0]][pos[1]].takeable = True
        return haveMoves
    

    def checksSelf(self, index):
        global blackInCheck, whiteInCheck
        row, col = self.index
        newRow, newCol = index
        temp = board.index[newRow][newCol]
        
        board.index[newRow][newCol] = board.index[row][col]
        board.index[row][col] = Empty(' ')

        ret = checkForCheck()

        board.index[row][col] = board.index[newRow][newCol]
        board.index[newRow][newCol] = temp

       
        if ret and board.index[row][col].team == 'W':
            return True
        elif ret and board.index[row][col].team == 'B':
            return True

        return False
    

class Empty(Piece):

    def __init__(self, team):
        super().__init__(team)
        self.piece = ' '
        self.img = pygame.image.load('Chess_Images/Empty.png')
        self.empty = True
        self.enPassant = False

    def movement(self):
        return self.moves


class Pawn(Piece):

    def __init__(self, team):
        super().__init__(team)
        self.piece = 'P'
        self.doublemove = True
        self.img = pygame.image.load(f'Chess_Images/{self.team}P.png')
        if self.team == 'W':
            self.dir = -1
        else:
            self.dir = 1
    
    def movement(self):
        self.moves = []
        row, col = self.index



        if self.doublemove:
            if board.index[row + self.dir][col].empty:
                if board.index[row + self.dir * 2][col].empty:
                    self.moves.append((row + self.dir * 2, col))

        forward = [(row + self.dir, col + i) for i in range(-1, 2)]

        for pos in forward:
            if board.onBoard(pos):
                if forward.index(pos) % 2 == 0:
                    if not board.index[pos[0]][pos[1]].empty:
                        if self.team != board.index[pos[0]][pos[1]].team:
                            self.moves.append(pos)
                    try:
                        if board.index[pos[0]][pos[1]].enPassant and board.index[pos[0]][pos[1]].empty:
                            self.moves.append(pos)
                    except:
                        pass
                elif board.index[pos[0]][pos[1]].empty:
                    self.moves.append(pos)
        return self.moves
    

    def promote(self, SCREEN, SIZE):
        global running

        exit = False
        bImages = ['Chess_Images/BQ.png', 'Chess_Images/BR.png', 'Chess_Images/BN.png', 'Chess_Images/BB.png']
        wImages = ['Chess_Images/WQ.png', 'Chess_Images/WR.png', 'Chess_Images/WN.png', 'Chess_Images/WB.png']

        BLACK = (0, 0, 0)
        GREY = (75, 75, 75)
        WHITE = (255, 255, 255)
        QUARTER = int(SIZE / 2)

        if self.team == 'W':
            images = wImages
        else:
            images = bImages

        for i in range(0, SIZE, QUARTER):
            for j in range(0, SIZE, QUARTER):
                rect = pygame.Rect(i, j, QUARTER, QUARTER)
                if i % SIZE == j % SIZE:
                    pygame.draw.rect(SCREEN, WHITE, rect)
                else:
                    pygame.draw.rect(SCREEN, GREY, rect)
                pygame.draw.rect(SCREEN, BLACK, rect, 1)

        for i in range(4):
            image = pygame.image.load(images[i])
            image = pygame.transform.scale(image, (QUARTER / 2, QUARTER / 2))
            SCREEN.blit(image, (i // 2 * QUARTER + (QUARTER / 4 ) , i % 2 * QUARTER + (QUARTER / 4 )))


        pygame.display.flip()

        while True:
            for event in pygame.event.get():     
                if event.type == pygame.QUIT: 
                    running = False
                    exit = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    col, row = pos
                    row = row // QUARTER
                    col = col // QUARTER
                    team = self.team

                    pos = board.index[self.index[0]][self.index[1]]

                    if row == 0 and col == 0:
                        pos = Queen(team)
                    elif row == 0 and col == 1:
                        pos = Knight(team)
                    elif row == 1 and col == 0:
                        pos = Rook(team)
                    elif row == 1 and col == 1:
                        pos = Bishop(team)

                    print(board.index[self.index[0]][self.index[1]])
                    print(board)


                    exit = True

            if exit:
                break

    def enPassant(self):
        row, col = self.index
        row -= self.dir
        board.index[row][col] = Empty(' ')


class King(Piece):

    def __init__(self, team):
        super().__init__(team)
        self.piece = 'K'
        self.castleAble = True
        self.img = pygame.image.load(f'Chess_Images/{self.team}K.png')

    def movement(self):
        self.moves = []
        row, col = self.index

        for i in range(-1, 2):
            for j in range(-1, 2):
                if board.onBoard((row + i, col + j)):
                    if self.team != board.index[row + i][col + j].team:
                        self.moves.append((row + i, col + j))


        if self.castleAble == True :
            directions = [[[row, col + i] for i in range(1, board.size - col)],
                          [[row, col - i] for i in range(1, col + 1)]]
            
            for direction in directions: 
                for pos in direction:
                    piece = board.index[pos[0]][pos[1]]
                    if not piece.empty and (piece.piece != 'R' or not piece.castleAble or self.team != piece.team):
                        break
                    if piece.piece == 'R':
                        self.moves.append(direction[1])
                        break
                                
        return self.moves

    
    def cast(self, rookPos):
        print(rookPos)
        row, col = self.index
        rookPos  = int(rookPos)
        if rookPos < 0:
            if board.index[row][board.size - 1].piece == 'R':
                board.index[row][col + rookPos] = board.index[row][board.size - 1]
                board.index[row][board.size - 1] = Empty(' ')
        else:
            if board.index[row][0].piece == 'R':
                board.index[row][col + rookPos] = board.index[row][0]
                board.index[row][0] = Empty(' ')


        board.index[row][col + rookPos].moved = True

                    
class Rook(Piece):

    def __init__(self, team):
        super().__init__(team)
        self.piece = 'R'
        self.castleAble = True
        self.img = pygame.image.load(f'Chess_Images/{self.team}R.png')

    def movement(self):
        self.moves = []
        row, col = self.index
        directions = [[[row + i, col] for i in range(1, board.size - row)],
                      [[row - i, col] for i in range(1, row + 1)],
                      [[row, col + i] for i in range(1, board.size - col)],
                      [[row, col - i] for i in range(1, col + 1)]]
        

        for direction in directions:
            
            for pos in direction:
                piece = board.index[pos[0]][pos[1]]
                if not piece.empty:
                    if self.team != piece.team:
                        self.moves.append(pos)
                        break
                    elif self.team == piece.team:
                        break
                else:
                    self.moves.append(pos)
        # updateIndex()
        # ^Bane of my existence, 4 tima wasta her
        return self.moves


class Bishop(Piece):

    def __init__(self, team):
        super().__init__(team)
        self.piece = 'B'
        self.img = pygame.image.load(f'Chess_Images/{self.team}B.png')

    def movement(self):
        self.moves = []
        row, col = self.index

        directions = [[[row + i, col + i] for i in range(1, board.size)],
                      [[row + i, col - i] for i in range(1, board.size)],
                      [[row - i, col + i] for i in range(1, board.size)],
                      [[row - i, col - i] for i in range(1, board.size)]]

        for direction in directions:
            for pos in direction:
                if board.onBoard(pos):

                    piece = board.index[pos[0]][pos[1]]
                    if not piece.empty:
                        if self.team != piece.team:
                            self.moves.append(pos)
                            break
                        elif self.team == piece.team:
                            break
                    else:
                        self.moves.append(pos)
        return self.moves


class Queen(Piece):

    def __init__(self, team):
        super().__init__(team)
        self.piece = 'Q'
        self.img = pygame.image.load(f'Chess_Images/{self.team}Q.png')

    def movement(self):
        self.moves = []
        moveset = []

        moveset.append(Rook.movement(self))
        moveset.append(Bishop.movement(self))
        self.moves = [pos for sub in moveset for pos in sub]
        return self.moves


class Knight(Piece):

    def __init__(self, team):
        super().__init__(team)
        self.piece = 'N'
        self.img = pygame.image.load(f'Chess_Images/{self.team}N.png')

    def movement(self):
        self.moves = []
        row, col = self.index

        for i in range(-2, 3):
            for j in range(-2, 3):
                if board.onBoard((row + i, col + j)):
                    if i**2 + j**2 == 5:
                        if self.team != board.index[row + i][col + j].team:
                            self.moves.append((row + i, col + j))
        return self.moves


class Board():

    def __init__(self):
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
        for row in range(board.size):
            for col in range(board.size):
                board.index[row][col].takeable = False
                board.index[row][col].moved = False




def checkForCheck():
    global whiteInCheck, blackInCheck
    global turn
    whiteInCheck = False
    blackInCheck = False
     
    allMoves = []
    for row in range(board.size):
        for col in range(board.size):
            piece = board.index[row][col]
            allMoves.append(piece.movement())

    allMoves = [pos for sub in allMoves for pos in sub]

    for pos in allMoves:
        if board.index[pos[0]][pos[1]].piece == 'K':
            if turn % 2 == 1 and board.index[pos[0]][pos[1]].team == 'W':
                whiteInCheck = True
                return True
            elif turn % 2 == 0 and board.index[pos[0]][pos[1]].team == 'B':
                blackInCheck = True
                return True
    return False


def checkForMate():
    checkMate = True
    for row in board.index:
        for pos in row:
            if not pos.empty:
                if pos.team == 'W' and turn % 2 == 1:
                    haveMoves = pos.getMoves()
                elif pos.team == 'B' and turn % 2 == 0:
                    haveMoves = pos.getMoves()
                else:
                    haveMoves = False
                if haveMoves:
                    checkMate = False
    return checkMate



def checkTurn(index):
    global turn
    row, col = index
    if turn % 2:
        if board.index[row][col].team == 'W':
            return True
    else:
        if board.index[row][col].team == 'B':
            return True


def updateIndex():
    for i in range(board.size):
        for j in range(board.size):
            board.index[i][j].index = (i, j)


def DRAW_BOARD(SCREEN, SIZE, TILE_SIZE):
    BLACK = (0, 0, 0)
    GREY = (75, 75, 75)
    WHITE = (255, 255, 255) 
    RED = (200, 0, 0)
    BLUE = (0, 0, 200)

    for i in range(0, SIZE, TILE_SIZE):
        for j in range(0, SIZE, TILE_SIZE):
            rect = pygame.Rect(i, j, TILE_SIZE, TILE_SIZE)
            if i % (TILE_SIZE * 2) == j % (TILE_SIZE * 2):
                pygame.draw.rect(SCREEN, WHITE, rect)
            else:
                pygame.draw.rect(SCREEN, GREY, rect)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)

    for i in range(board.size):
        for j in range(board.size):
            rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if board.index[i][j].takeable:
                pygame.draw.rect(SCREEN, RED, rect)
                pygame.draw.rect(SCREEN, BLACK, rect, 1)
                if board.index[i][j].empty and not board.index[i][j].enPassant:
                    pygame.draw.rect(SCREEN, BLUE, rect)
                    pygame.draw.rect(SCREEN, BLACK, rect, 1)





def DRAW_PIECES(SCREEN, TILE_SIZE):
    for row in range(board.size):
        for col in range(board.size):
            image = board.index[row][col].img
            image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            SCREEN.blit(image, (col * TILE_SIZE, row * TILE_SIZE))



def DRAW_MOVES(row, col):
    row = int(row)
    col = int(col)
    if not board.index[row][col].empty:
        board.index[row][col].getMoves()


def main():
    global board
    global blackInCheck, whiteInCheck
    global turn
    global running

    board = Board()
    turn = 1
    show = False
    blackInCheck = False
    whiteInCheck = False
    prevRow = -1
    prevCol = -1


    updateIndex()

    windowIcon = pygame.image.load('Chess_Images/Thumbnail.png')
    pygame.display.set_icon(windowIcon)
    pygame.display.set_caption('Turn 1 \ White\'s turn')
    SIZE = 480   
    TILE_SIZE = int(SIZE / board.size)
    SIZE = TILE_SIZE * board.size
    SCREEN = pygame.display.set_mode((SIZE, SIZE)) 



    
    running = True
    while running:  
        DRAW_BOARD(SCREEN, SIZE, TILE_SIZE)
        DRAW_PIECES(SCREEN, TILE_SIZE)
        pygame.display.flip() 

        while True:
            event = pygame.event.wait()
            if event.type != pygame.MOUSEMOTION:
                break

        if event.type == pygame.QUIT: 
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:

            pos = pygame.mouse.get_pos()
            col, row = pos
            row = int(row // TILE_SIZE)
            col = int(col // TILE_SIZE)
            clear = False
            doEnPassant = False

            
            try:
                if row == prevRow and col == prevCol and not show:
                    clear = True
                    show = True
                else:
                    show = False
            except:
                pass
                
 
           
            
            if board.index[row][col].takeable:
                if checkTurn((prevRow, prevCol)):
                    
                    if board.index[row][col].empty and board.index[row][col].enPassant:
                        doEnPassant = True
                    board.index[row][col] = board.index[prevRow][prevCol]
                    board.index[prevRow][prevCol] = Empty(' ')
                    board.index[row][col].moved = True
                    turn += 1
                    clear = True
                    show = True


                    try:
                        board.index[row][col].castleAble = False
                    except:
                        pass

                    try:
                        board.index[row][col].doublemove = False
                    except:
                        pass

                    for tempRow in range(board.size):
                        for tempCol in range(board.size):
                            if board.index[tempRow][tempCol].empty:
                                board.index[tempRow][tempCol].enPassant = False

                else:
                    print(f'It is not you turn')

            
            DRAW_PIECES(SCREEN, TILE_SIZE)
            updateIndex()

            if doEnPassant:
                board.index[row][col].enPassant()


            if board.index[row][col].piece == 'K' and board.index[row][col].moved and abs(prevCol - col) == 2:

                rookPos = int((prevCol - col) / 2)
                board.index[row][col].cast(rookPos)


            if board.index[row][col].piece == 'P' and board.index[row][col].moved and abs(prevRow - row) == 2:
                tempRow = row + int((prevRow - row) / 2)
                board.index[tempRow][col].enPassant = True
                


            
            for rows in board.index:
                for pos in rows:
                    if pos.piece == 'P':
                        if pos.index[0] == 0 or pos.index[0] == board.size - 1:
                                pos.promote(SCREEN, SIZE)

            updateIndex()



            windowTitle = f'Turn {turn}'

            if turn % 2 == 1:
                windowTitle += ' \ White\'s turn'
            else:
                windowTitle += ' \ Black\'s turn'
            
            checkForCheck()
            if whiteInCheck:
                if checkForMate():
                    windowTitle += ' \ White is in mate'
                else:
                    windowTitle += ' \ White is in check'
            elif blackInCheck:
                if checkForMate():
                    windowTitle += ' \ Black is in mate'
                else:
                    windowTitle += ' \ Black is in check'
            pygame.display.set_caption(windowTitle)

            

            prevRow = row
            prevCol = col
            board.clearBoard()
            DRAW_MOVES(row, col)
                        


            if clear:
                board.clearBoard()
            print(board)   




main()


'''
TO-DO:
Update checkForCheck() and checForMate() to work with enPassant
'''