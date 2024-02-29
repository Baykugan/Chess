import pygame

from chess_pieces.piece import Piece


class Bishop(Piece):

    def __init__(self, team):
        super().__init__(team)
        self.piece = 'B'
        self.img = pygame.image.load(f'Chess_Images/{self.team}B.png')

    def movement(self, board):
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