
from piece import Piece, WHITE, BLACK


# Board class that represents the chess board as a 2D array of either Piece objects or None

class Board:

    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
    
    # set up the board with the starting pieces
    def setup_board(self):
        piece_order = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        # black pieces on rank 7 and 8
        for i, piece_type in enumerate(piece_order):
            self.board[7][i] = Piece(BLACK, piece_type)
            self.board[6][i] = Piece(BLACK, "pawn")
        # white pieces on rank 1 and 2
        for i, piece_type in enumerate(piece_order):
            self.board[0][i] = Piece(WHITE, piece_type)
            self.board[1][i] = Piece(WHITE, "pawn")

    # display the board with pieces
    def display(self):
        print()
        for i in range(7, -1, -1):
            for j in range(8):
                if self.board[i][j] is None:
                    print(".", end=" ")
                else:
                    print(self.board[i][j], end=" ")
            print()
        print()
    
    # check that the straight path between two squares is clear for a move
    def is_path_clear(self, start_pos, end_pos):
        # compute deltas
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        d_row = end_row - start_row
        d_col = end_col - start_col
        # horizontal movement
        if d_row == 0:
            for col in range(min(start_col, end_col) + 1, max(start_col, end_col)):
                if self.board[start_row][col] is not None:
                    return False
            return True
        # vertical movement
        elif d_col == 0:
            for row in range(min(start_row, end_row) + 1, max(start_row, end_row)):
                if self.board[row][start_col] is not None:
                    return False
            return True
        # diagonal movement
        elif abs(d_row) == abs(d_col):
            for i in range(1, abs(d_row)):
                if self.board[start_row + d_row // abs(d_row) * i][start_col + d_col // abs(d_col) * i] is not None:
                    return False
            return True
        # invalid path
        return False


    # perform a move on the board
    def move_piece(self, start_pos, end_pos):
        # check that indices are valid
        if start_pos[0] < 0 or start_pos[0] > 7 or start_pos[1] < 0 or start_pos[1] > 7:
            raise ValueError("Invalid start position.")
        if end_pos[0] < 0 or end_pos[0] > 7 or end_pos[1] < 0 or end_pos[1] > 7:
            raise ValueError("Invalid end position.")
        # make the move
        piece = self.board[start_pos[0]][start_pos[1]]
        self.board[start_pos[0]][start_pos[1]] = None
        self.board[end_pos[0]][end_pos[1]] = piece


    # find the king of the specified color in the board
    def find_king(self, color):
        for r in range(8):
            for c in range(8):
                if self.board[r][c] and self.board[r][c].type == "king" and self.board[r][c].color == color:
                    return (r, c) # found the king
        return None # something went wrong

