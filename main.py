
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

    # initialize the piece by color and type, e.g. Piece(WHITE, "rook")
    def __init__(self, color, type):
        self.color = color
        self.type = type
    
    # overwrite __str__ to use Unicode chess characters to display the pieces
    def __str__(self):
        return self.UNICODE_PIECES[self.color][self.type]
    
    # check if the move is valid for the piece
    def is_valid_move(self, start_pos, end_pos):
        # null moves are illegal
        if start_pos == end_pos:
            return False
        # compute deltas
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        d_row = abs(end_row - start_row)
        d_col = abs(end_col - start_col)
        # check if piece can make the move
        if self.type == "king":
            return (d_row <= 1 and d_col <= 1)
        elif self.type == "rook":
            return (d_row == 0 or d_col == 0)
        elif self.type == "bishop":
            return (d_row == d_col)
        elif self.type == "queen":
            return (d_row == 0 or d_col == 0) or (d_row == d_col)
        elif self.type == "knight":
            return (d_row == 2 and d_col == 1) or (d_row == 1 and d_col == 2)
        # pawn is a bit trickier
        elif self.type == "pawn":
            if self.color == "white":
                if d_row == 1 and d_col == 0:
                    return True
                if start_row == 1 and d_row == 2 and d_col == 0:
                    return True
            elif self.color == "black":
                if d_row == 1 and d_col == 0:
                    return True
                if start_row == 6 and d_row == 2 and d_col == 0:
                    return True
        # conclude if-elif block
        return False



# Game class to represent a chess game
class Game:

    # initialize the board and the game
    def __init__(self):
        self.board = Board()
        self.board.setup_board()
        self.current_player = WHITE

    # main game loop
    def play(self):
        while True:
            # display the board
            self.board.display()
            print(f"{self.current_player}'s turn")
            try:
                # get the user's move
                move = input("Enter your move: ")
                if len(move) != 4:
                    errmsg = "Invalid input. Please use valid algebraic notation (e.g., 'e2e4')."
                    raise ValueError
                if move.lower() == 'exit': # quit
                    break
                # select the moving piece and check move validity
                start_pos = _n2c(move[:2])
                end_pos = _n2c(move[2:])
                piece = self.board.board[start_pos[0]][start_pos[1]]
                if piece is None or piece.color != self.current_player:
                    errmsg = "Invalid input. Please select a valid move."
                    raise ValueError
                if not piece.is_valid_move(start_pos, end_pos):
                    errmsg = f"Invalid input. Please select a valid move for your {piece.type}."
                    raise ValueError
                # make the move
                self.board.move_piece(start_pos, end_pos)
                # switch players if the move was successful
                self.current_player = BLACK if self.current_player == WHITE else WHITE
            except (ValueError, IndexError):
                print(errmsg)



# test
g = Game()
g.play()


