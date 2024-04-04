import pygame

from Chess_Pieces.Pieces import *
from Board import Board 


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
        board.index[row][col].getMoves(board)


def main():
    global board
    global blackInCheck, whiteInCheck
    global running
    global printToTerminal

    board = Board()
    show = False
    blackInCheck = False
    whiteInCheck = False
    prevRow = -1
    prevCol = -1
    printToTerminal = False
    # if input(f'Do you want the game printed to the terminal? (y/n)') == 'y':
    #     printToTerminal = True


    board.updateIndex()

    windowIcon = pygame.image.load('Chess_Images/Thumbnail.png')
    pygame.display.set_icon(windowIcon)
    pygame.display.set_caption('Turn 1 \\ White\'s turn')
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
                if board.checkTurn((prevRow, prevCol)):
                    
                    if board.index[row][col].empty and board.index[row][col].enPassant:
                        doEnPassant = True
                    board.index[row][col] = board.index[prevRow][prevCol]
                    board.index[prevRow][prevCol] = Empty(' ')
                    board.index[row][col].moved = True
                    board.turn += 1
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
                    if printToTerminal:
                        print(f'It is not you turn')

            
            DRAW_PIECES(SCREEN, TILE_SIZE)
            board.updateIndex()

            if doEnPassant:
                board.index[row][col].enPassant(board)


            if board.index[row][col].piece == 'K' and board.index[row][col].moved and abs(prevCol - col) == 2:

                rookPos = int((prevCol - col) / 2)
                board.index[row][col].castle(board, rookPos)


            if board.index[row][col].piece == 'P' and board.index[row][col].moved and abs(prevRow - row) == 2:
                tempRow = row + int((prevRow - row) / 2)
                board.index[tempRow][col].enPassant = True
                


            
            for rows in board.index:
                for pos in rows:
                    if pos.piece == 'P':
                        if pos.index[0] == 0 or pos.index[0] == board.size - 1:
                                pos.promote(SCREEN, SIZE)

            board.updateIndex()



            windowTitle = f'Turn {board.turn}'

            if board.turn % 2 == 1:
                windowTitle += ' \\ White\'s turn'
            else:
                windowTitle += ' \\ Black\'s turn'
            
            board.checkForCheck()
            if whiteInCheck:
                if board.checkForMate():
                    windowTitle += ' \\ White is in mate'
                else:
                    windowTitle += ' \\ White is in check'
            elif blackInCheck:
                if board.checkForMate():
                    windowTitle += ' \\ Black is in mate'
                else:
                    windowTitle += ' \\ Black is in check'
            pygame.display.set_caption(windowTitle)

            

            prevRow = row
            prevCol = col
            board.clearBoard()
            DRAW_MOVES(row, col)
                        


            if clear:
                board.clearBoard()
            if printToTerminal:
                print(board)   




main()


'''
TO-DO:
Update checkForCheck() and checForMate() to work with enPassant
'''