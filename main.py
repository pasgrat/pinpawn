
# useful constants to avoid typos
WHITE = "white"
BLACK = "black"


# useful conversion functions

def n2c(notation): # notation to coords
    # converts chess notation to row and column indices
    # e.g. 'a1' -> (0, 0), 'a2' -> (0, 1), 'h8' -> (7, 7)
    return ord(notation[0]) - ord('a'), int(notation[1]) - 1

def c2n(row, col): # coords to notation
    # converts row and column indices to chess notation
    # e.g. (0, 0) -> 'a1', (0, 1) -> 'a2', (7, 7) -> 'h8'
    return chr(ord('a') + row) + str(col + 1)



# Board class that represents the chess board as a 2D array of either Piece objects or None
class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
    
    # set up the board with the starting pieces
    def setup_board(self):
        piece_order = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        # black pieces on the 8 rank
        for i in range(8):
            self.board[7][i] = Piece(BLACK, piece_order[i])
        # black pawns on the 7 rank
        for i in range(8):
            self.board[6][i] = Piece(BLACK, "pawn")
        # white pieces on the 1 rank
        for i in range(8):
            self.board[0][i] = Piece(WHITE, piece_order[i])
        # white pawns on the 2 rank
        for i in range(8):
            self.board[1][i] = Piece(WHITE, "pawn")

    # display the board with pieces
    def display(self):
        for i in range(7, -1, -1):
            for j in range(8):
                if self.board[i][j] is None:
                    print(".", end=" ")
                else:
                    print(self.board[i][j], end=" ")
            print()
        print()



# Piece class that represents a chess piece
class Piece:

    UNICODE_PIECES = {
        "white": {"rook": "♖", "knight": "♘", "bishop": "♗", "queen": "♕", "king": "♔", "pawn": "♙"},
        "black": {"rook": "♜", "knight": "♞", "bishop": "♝", "queen": "♛", "king": "♚", "pawn": "♟"}
    }

    # initialize the piece by color and type, e.g. Piece(WHITE, "rook")
    def __init__(self, color, type):
        self.color = color
        self.type = type
    
    # overwrite __str__ function to use Unicode chess characters to display the pieces
    def __str__(self):
        return self.UNICODE_PIECES[self.color][self.type]



# test
board = Board()
board.setup_board()
board.display()

print(n2c("a1"))
print(n2c("a2"))
print(n2c("h8"))

print(c2n(0, 0))
print(c2n(0, 1))
print(c2n(7, 7))
