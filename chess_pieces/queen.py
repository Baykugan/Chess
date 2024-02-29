import pygame

from chess_pieces.piece import Piece
from chess_pieces.rook import Rook
from chess_pieces.bishop import Bishop


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