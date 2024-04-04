import pygame

from Chess_Pieces.Piece import Piece
from Chess_Pieces.Rook import Rook
from Chess_Pieces.Bishop import Bishop


class Queen(Piece):

    def __init__(self, team):
        super().__init__(team)
        self.piece = 'Q'
        self.img = pygame.image.load(f'Chess_Images/{self.team}Q.png')

    def movement(self, board):
        self.moves = []
        moveset = []

        moveset.append(Rook.movement(self, board))
        moveset.append(Bishop.movement(self, board))
        self.moves = [pos for sub in moveset for pos in sub]
        return self.moves