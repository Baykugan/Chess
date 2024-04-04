import pygame

from Chess_Pieces.Piece import Piece


class Knight(Piece):

    def __init__(self, team):
        super().__init__(team)
        self.piece = 'N'
        self.img = pygame.image.load(f'Chess_Images/{self.team}N.png')

    def movement(self, board):
        self.moves = []
        row, col = self.index

        for i in range(-2, 3):
            for j in range(-2, 3):
                if board.onBoard((row + i, col + j)):
                    if i**2 + j**2 == 5:
                        if self.team != board.index[row + i][col + j].team:
                            self.moves.append((row + i, col + j))
        return self.moves