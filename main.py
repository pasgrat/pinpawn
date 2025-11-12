
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



# Game class to represent a chess game
class Game:

    # initialize the board and the game
    def __init__(self):
        self.board = Board()
        self.board.setup_board()
        self.curr_player = WHITE
        self.curr_opponent = BLACK


    # main game loop
    def play(self):
        while True:

            # display the board
            self.board.display()
            print(f"{self.curr_player}'s turn")

            # make a move
            try:
                # get the user's move
                move = input("Enter your move: ")
                if move.lower() == 'exit':
                    break # quit shortcut
                if len(move) != 4:
                    print("Invalid input. Please use valid algebraic notation (e.g., 'e2e4').")
                    continue
                # check move validity
                start_pos = _n2c(move[:2])
                end_pos = _n2c(move[2:])
                if not self.is_move_legal(start_pos, end_pos, self.curr_player):
                    print(f"Illegal move. Please select a valid move.")
                    continue
                # make the move and switch players
                self.board.move_piece(start_pos, end_pos)
                self.curr_player = BLACK if self.curr_player == WHITE else WHITE
                self.curr_opponent = BLACK if self.curr_player == WHITE else WHITE
            except (ValueError, IndexError):
                print("GENERAL ERROR: Invalid input or illegal move.")
            
            # check for check
            king_pos = self.board.find_king(self.curr_player)
            if king_pos and self.is_square_attacked(king_pos, self.curr_opponent):
                print(f"\n{self.curr_player} is in check!")

    

    # general function to check if a move is legal for a player
    def is_move_legal(self, start_pos, end_pos, player):
        piece = self.board.board[start_pos[0]][start_pos[1]]

        # 0. check that the move makes sense
        if start_pos == end_pos:
            print("Illegal move. Please select a valid move.")
            return False

        # 1. check that the piece exists
        if piece is None:
            print("Illegal move. Please select a valid piece.")
            return False

        # 2. check that the piece belongs to the current player
        if piece.color != player:
            print(f"Illegal move. Please select a valid move for {player}.")
            return False

        # 3. check for capturing own piece
        dest_piece = self.board.board[end_pos[0]][end_pos[1]]
        if dest_piece is not None and dest_piece.color == piece.color:
            print("You cannot capture your own piece! Please try again.")
            return False

        # 4. check piece-specific move logic
        if not self.is_piece_move_legal(piece, start_pos, end_pos, dest_piece):
            return False

        # 5. check for path obstructions
        if piece.type in ["rook", "bishop", "queen"]:
            if not self.board.is_path_clear(start_pos, end_pos):
                print(f"Illegal move, path is obstructed. Please select a valid move for your {piece.type}.")
                return False
        
        # 6. check if move puts own king in check
        # TODO

        # after all checks pass
        return True
    

    # detailed move check function to handle more complex logic
    def is_piece_move_legal(self, piece, start_pos, end_pos, dest_piece):

        # compute deltas
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        d_row = abs(end_row - start_row)
        d_col = abs(end_col - start_col)
        
        # handle complex pawn logic
        if piece.type == "pawn":
            signed_d_row = end_row - start_row
            direction = 1 if piece.color == WHITE else -1

            # forward 1 step
            if signed_d_row == direction and d_col == 0 and dest_piece is None:
                return True
            
            # forward 2 steps from start rank
            start_rank = 1 if piece.color == WHITE else 6
            if start_row == start_rank and signed_d_row == direction * 2 and d_col == 0 and dest_piece is None:
                # also check that path is clear, by checking that the first square is empty
                return self.board.board[start_row + direction][start_col] is None

            # diagonal capture
            if signed_d_row == direction and d_col == 1 and dest_piece is not None:
                return True # dest_piece color check already done in caller function
        
        # other pieces logic
        elif piece.type == "king":
            return (d_row <= 1 and d_col <= 1)
        elif piece.type == "rook":
            return (d_row == 0 or d_col == 0)
        elif piece.type == "bishop":
            return (d_row == d_col)
        elif piece.type == "queen":
            return (d_row == 0 or d_col == 0) or (d_row == d_col)
        elif piece.type == "knight":
            return (d_row == 2 and d_col == 1) or (d_row == 1 and d_col == 2)
            
        # if we get here, the move is not legal
        print("Illegal move, invalid piece logic. Please select a valid move.")
        return False
    

    # check if a square is attacked by a piece of a specific color
    def is_square_attacked(self, position, attacking_color):
        for r in range(8):
            for c in range(8):
                # check if there is a potential attacking piece
                piece = self.board.board[r][c]
                if piece is not None and piece.color == attacking_color:
                    # check if the piece could attack the square
                    if self.is_move_legal((r, c), position, self.curr_opponent):
                        return True # attack detected
                        # TODO: exclude pawns moving 1 or 2 squares forward
        return False # no attack detected



        



# -----

# test
g = Game()
g.play()
