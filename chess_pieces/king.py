import pygame

from chess_pieces.piece import Piece
from chess_pieces.empty import Empty


class King(Piece):

    def __init__(self, team):
        super().__init__(team)
        self.piece = 'K'
        self.castleAble = True
        self.img = pygame.image.load(f'Chess_Images/{self.team}K.png')

    def movement(self, board):
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

    
    def castle(self, board, rookPos):
        print(rookPos)
        row, col = self.index
        rookPos = int(rookPos)
        if rookPos < 0:
            if board.index[row][board.size - 1].piece == 'R':
                board.index[row][col + rookPos] = board.index[row][board.size - 1]
                board.index[row][board.size - 1] = Empty(' ')
        else:
            if board.index[row][0].piece == 'R':
                board.index[row][col + rookPos] = board.index[row][0]
                board.index[row][0] = Empty(' ')


        board.index[row][col + rookPos].moved = True