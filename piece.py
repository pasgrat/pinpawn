
# useful constants to avoid typos
WHITE = "white"
BLACK = "black"


# Piece class that represents a chess piece

class Piece:

    UNICODE_PIECES = {
        WHITE: {"rook": "♖", "knight": "♘", "bishop": "♗", "queen": "♕", "king": "♔", "pawn": "♙"},
        BLACK: {"rook": "♜", "knight": "♞", "bishop": "♝", "queen": "♛", "king": "♚", "pawn": "♟"}
    }

    # initialize the piece by color and type, e.g. Piece(WHITE, "rook")
    def __init__(self, color, type):
        self.color = color
        self.type = type
    
    # overwrite __str__ to use Unicode chess characters to display the pieces
    def __str__(self):
        return self.UNICODE_PIECES[self.color][self.type]
