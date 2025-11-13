
from board import *
import utils


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
                start_pos = utils._n2c(move[:2])
                end_pos = utils._n2c(move[2:])
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
    

    # geometric piece-specific move check function to handle complex logic
    def is_piece_move_legal(self, piece, start_pos, end_pos, dest_piece, is_attack_check=False):

        # compute deltas
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        d_row = abs(end_row - start_row)
        d_col = abs(end_col - start_col)
        
        # handle complex pawn logic
        if piece.type == "pawn":
            signed_d_row = end_row - start_row
            direction = 1 if piece.color == WHITE else -1

            # diagonal capture
            if signed_d_row == direction and d_col == 1 and dest_piece is not None:
                return True # dest_piece color check already done in caller function
            
            # forward moves (not allowed for attack checks)
            if not is_attack_check:
                # forward 1 step
                if signed_d_row == direction and d_col == 0 and dest_piece is None:
                    return True
                # forward 2 steps from start rank
                start_rank = 1 if piece.color == WHITE else 6
                if start_row == start_rank and signed_d_row == direction * 2 and d_col == 0 and dest_piece is None:
                    # also check that path is clear, by checking that the first square is empty
                    return self.board.board[start_row + direction][start_col] is None
        
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
                    # check piece logic only, bypassing turn and friendly fire checks
                    start_pos = (r, c)
                    dest_piece = self.board.board[position[0]][position[1]] # for consistency
                    if self.is_piece_move_legal(piece, start_pos, position, dest_piece, is_attack_check=True):
                        # check path for sliding pieces
                        if piece.type in ["rook", "bishop", "queen"]:
                            if self.board.is_path_clear((r, c), position):
                                return True # path clear, attack detected
                        else:
                            return True # for other pieces, attack detected
        return False # no attack detected

