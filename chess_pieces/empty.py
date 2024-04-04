import pygame
from Chess_Pieces.Piece import Piece

class Empty(Piece):

    def __init__(self, team):
        super().__init__(team)
        self.piece = ' '
        self.img = pygame.image.load('Chess_Images/Empty.png')
        self.empty = True
        self.enPassant = False

    def movement(self, board):
        return self.moves
