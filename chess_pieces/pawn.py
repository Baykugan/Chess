import pygame

from chess_pieces.piece import Piece
from chess_pieces.empty import Empty
from chess_pieces.rook import Rook
from chess_pieces.bishop import Bishop
from chess_pieces.queen import Queen
from chess_pieces.knight import Knight


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
    
    def movement(self, board):
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
    

    def promote(self, board, SCREEN, SIZE):
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

                    # if printToTerminal:
                    #     print(board)


                    exit = True

            if exit:
                break

    def enPassant(self, board):
        row, col = self.index
        row -= self.dir
        board.index[row][col] = Empty(' ')