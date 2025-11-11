
# useful constants to avoid typos
WHITE = "white"
BLACK = "black"



# conversion functions

def _n2c(notation): # notation to coords
    # converts chess notation to row and column indices
    # e.g. 'a1' -> (0,0), 'a2' -> (1,0), 'e4' -> (3,4), 'h8' -> (7,7)
    return int(notation[1]) - 1, ord(notation[0]) - ord('a')

def _c2n(row, col): # coords to notation
    # converts row and column indices to chess notation
    # e.g. (0,0) -> 'a1', (1,0) -> 'a2', (3,4) -> 'e4', (7,7) -> 'h8'
    return chr(col + ord('a')) + str(row + 1)



# Board class that represents the chess board as a 2D array of either Piece objects or None
class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
    
    def setup_board(self):
        # set up the board with the starting pieces
        piece_order = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        # black pieces on rank 7 and 8
        for i, piece_type in enumerate(piece_order):
            self.board[7][i] = Piece(BLACK, piece_type)
            self.board[6][i] = Piece(BLACK, "pawn")
        # white pieces on rank 1 and 2
        for i, piece_type in enumerate(piece_order):
            self.board[0][i] = Piece(WHITE, piece_type)
            self.board[1][i] = Piece(WHITE, "pawn")

    def display(self):
        # display the board with pieces
        for i in range(7, -1, -1):
            for j in range(8):
                if self.board[i][j] is None:
                    print(".", end=" ")
                else:
                    print(self.board[i][j], end=" ")
            print()
        print()
    
    def move_piece(self, start_pos, end_pos):
        # check that indices are valid
        if start_pos[0] < 0 or start_pos[0] > 7 or start_pos[1] < 0 or start_pos[1] > 7:
            raise ValueError("Invalid start position")
        if end_pos[0] < 0 or end_pos[0] > 7 or end_pos[1] < 0 or end_pos[1] > 7:
            raise ValueError("Invalid end position")
        # make the move
        piece = self.board[start_pos[0]][start_pos[1]]
        self.board[start_pos[0]][start_pos[1]] = None
        self.board[end_pos[0]][end_pos[1]] = piece



# Piece class that represents a chess piece
class Piece:

    UNICODE_PIECES = {
        "white": {"rook": "♖", "knight": "♘", "bishop": "♗", "queen": "♕", "king": "♔", "pawn": "♙"},
        "black": {"rook": "♜", "knight": "♞", "bishop": "♝", "queen": "♛", "king": "♚", "pawn": "♟"}
    }

    def __init__(self, color, type):
        # initialize the piece by color and type, e.g. Piece(WHITE, "rook")
        self.color = color
        self.type = type
    
    def __str__(self):
        # overwrite __str__ to use Unicode chess characters to display the pieces
        return self.UNICODE_PIECES[self.color][self.type]



# Game class to represent a chess game
class Game:

    def __init__(self):
        # initialize the board and the game
        self.board = Board()
        self.board.setup_board()
        self.current_player = WHITE


    def play(self):
        # main game loop
        while True:
            # display the board
            self.board.display()
            print(f"{self.current_player}'s turn")
            try:
                # get the user's move
                move = input("Enter your move: ")
                if len(move) != 4:
                    raise ValueError("Invalid input. Please use valid algebraic notation (e.g., 'e2e4').")
                if move.lower() == 'exit': # quit
                    break
                # make the move
                start_pos = _n2c(move[:2])
                end_pos = _n2c(move[2:])
                self.board.move_piece(start_pos, end_pos)
                # switch players if the move was successful
                self.current_player = BLACK if self.current_player == WHITE else WHITE
            except (ValueError, IndexError):
                print("Invalid input. Please use valid algebraic notation (e.g., 'e2e4').")



# test
g = Game()
g.play()


