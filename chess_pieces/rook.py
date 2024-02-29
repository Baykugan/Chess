import pygame

from chess_pieces.piece import Piece


class Rook(Piece):

    def __init__(self, team):
        super().__init__(team)
        self.piece = 'R'
        self.castleAble = True
        self.img = pygame.image.load(f'Chess_Images/{self.team}R.png')

    def movement(self, board):
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