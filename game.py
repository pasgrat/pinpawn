
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

            # display the board and reset flags
            self.board.display()
            print(f"{self.curr_player}'s turn")
            king_in_check = False

            # make the player pick a move
            try:
                move = input("Enter your move: ")
                if move.lower() == 'exit':
                    break # quit shortcut
                if len(move) != 4:
                    print("Invalid input. Please use valid algebraic notation (e.g., 'e2e4').")
                    continue
                start_pos = utils._n2c(move[:2])
                end_pos = utils._n2c(move[2:])
            except (ValueError, IndexError):
                print("GENERAL ERROR: Invalid input.\n")
            
            # check move validity and make the move
            is_legal, error_msg = self.is_move_legal(start_pos, end_pos, self.curr_player)
            if not is_legal:
                print("\n" + error_msg)
                continue
            moved_piece = self.board.board[start_pos[0]][start_pos[1]]
            self.board.move_piece(start_pos, end_pos)

            # check for pawn promotion and handle it
            if moved_piece.type == "pawn" and (end_pos[0] == 0 or end_pos[0] == 7):
                new_type = "_"
                while new_type not in ["Q", "R", "B", "K"]:
                    new_type = input("Pick a piece for pawn promotion (Q,R,B,K): ")
                    if new_type not in ["Q", "R", "B", "K"]:
                        print("Invalid input, please try again.")
                # replace pawn in end position with new piece
                piece_ref = {"Q":"queen", "R":"rook", "B":"bishop", "K":"knight"}
                self.board.board[end_pos[0]][end_pos[1]] = Piece(self.curr_player, piece_ref[new_type])

            # switch players
            self.curr_player = BLACK if self.curr_player == WHITE else WHITE
            self.curr_opponent = BLACK if self.curr_player == WHITE else WHITE

            # check for check
            king_pos = self.board.find_king(self.curr_player)
            if king_pos and self.is_square_attacked(king_pos, self.curr_opponent):
                king_in_check = True # temporary flag
            
            # check for checkmate or stalemate
            moves = self.find_all_legal_moves(self.curr_player) # moves for the player who has to move now
            print(f"{self.curr_player} has {len(moves)} legal move{'s' if len(moves) != 1 else ''} available") # feedback print
            if not moves:
                # no legal moves and king in check -> checkmate
                if king_in_check:
                    print(f"\n{self.curr_player} is in checkmate! {self.curr_opponent} is the winner!\n")
                    break
                # no legal moves and king not in check -> stalemate
                else:
                    print(f"\nStalemate! It's a draw.\n")
                    break
            
            # no checkmate nor stalemate -> announce eventual check
            if king_in_check:
                print(f"\n{self.curr_player} is in check.")
            

    

    # general function to check if a move is legal for a player
    def is_move_legal(self, start_pos, end_pos, player):
        piece = self.board.board[start_pos[0]][start_pos[1]]

        # 0. check that the move makes sense
        if start_pos == end_pos:
            return (False, "Illegal move. Start and end square are the same.")

        # 1. check that the piece exists
        if piece is None:
            return (False, "Illegal move. There is no piece at the starting square.")

        # 2. check that the piece belongs to the current player
        if piece.color != player:
            return (False, f"Illegal move. It is {player}'s turn.")

        # 3. check for capturing own piece
        dest_piece = self.board.board[end_pos[0]][end_pos[1]]
        if dest_piece is not None and dest_piece.color == piece.color:
            return (False, "Illegal move. You cannot capture your own piece.")

        # 4. check piece-specific move logic
        if not self.is_piece_move_legal(piece, start_pos, end_pos, dest_piece):
            return (False, f"Illegal move. A {piece.type} cannot move like that.")

        # 5. check for path obstructions
        if piece.type in ["rook", "bishop", "queen"]:
            if not self.board.is_path_clear(start_pos, end_pos):
                return (False, f"Illegal move. The path for the {piece.type} is obstructed.")
        
        # 6. check if move puts own king in check
        # try to perform move (saving the state)
        piece_at_start = self.board.board[start_pos[0]][start_pos[1]]
        piece_at_end = self.board.board[end_pos[0]][end_pos[1]]
        self.board.board[start_pos[0]][start_pos[1]] = None
        self.board.board[end_pos[0]][end_pos[1]] = piece_at_start
        # check if player's king is in check
        is_illegal = False # temporary flag
        king_pos = self.board.find_king(player)
        if king_pos and self.is_square_attacked(king_pos, self.curr_opponent):
            is_illegal = True # mark move as illegal
        # restore the state and return if move was illegal
        self.board.board[start_pos[0]][start_pos[1]] = piece_at_start
        self.board.board[end_pos[0]][end_pos[1]] = piece_at_end
        if is_illegal:
            return (False, f"Illegal move. You cannot leave or put your own king in check.")

        # after all checks pass
        return (True, "")
    

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


    # lists all the legal moves for a player
    def find_all_legal_moves(self, player):
        moves = []
        # find all starting squares with player's pieces
        for r in range(8):
            for c in range(8):
                piece = self.board.board[r][c]
                # if there's a piece, try to move it to all possible other squares
                if piece is not None and piece.color == player:
                    for end_row in range(8):
                        for end_col in range(8):
                            # check the legality of the move
                            legal_flag, _ = self.is_move_legal((r, c), (end_row, end_col), player)
                            if legal_flag:
                                moves.append((r, c, end_row, end_col))
        return moves