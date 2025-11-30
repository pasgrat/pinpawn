
import random
import copy
from game import WHITE, BLACK
from pst import PIECE_TABLES


# piece values (positive for white, negative for black)
PIECE_SCORE = {"king": 0, "queen": 900, "rook": 500, "bishop": 330, "knight": 320, "pawn": 100}



# function to find the best move on a given game state, using minimax with alpha-beta pruning
# takes as optional input the depth of the minimax search (defaults to 2)
def get_minimax_move(game, depth=2):
    moves = game.find_all_legal_moves(game.curr_player)
    random.shuffle(moves) # randomize order to avoid AI playing the exact same moves every time
    maximize = True if game.curr_player == WHITE else False # flag to check who is maximizing
    # initialize alpha/beta values
    alpha = -100000 # best score white can guarantee
    beta = 100000 # best score black can guarantee
    best_move = None
    
    if maximize: # white
        max_eval = -100000
        for move in moves:
            # create a copy of the game to simulate the move (computationally expensive but necessary)
            game_copy = copy.deepcopy(game)
            start_pos = (move[0], move[1])
            end_pos = (move[2], move[3])
            game_copy.make_move(start_pos, end_pos)
            # perform minimax
            evaluation = minimax(game_copy, depth - 1, alpha, beta, False) # recursive call
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = (start_pos, end_pos)
            # alpha-beta pruning
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break # pruning
        return best_move

    else: # black (minimize)
        min_eval = 100000
        for move in moves:
            game_copy = copy.deepcopy(game)
            start_pos = (move[0], move[1])
            end_pos = (move[2], move[3])
            game_copy.make_move(start_pos, end_pos)
            # perform minimax
            evaluation = minimax(game_copy, depth - 1, alpha, beta, True)
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = (start_pos, end_pos)
            # alpha-beta pruning
            beta = min(beta, evaluation)
            if beta <= alpha:
                break # pruning
        return best_move


# minimax algorithm recursive function
def minimax(game, depth, alpha, beta, maximizing_player):
    # base stopping condition
    if depth == 0:
        return score_board(game.board)
    
    # list moves and check for game over inside the recursion
    moves = game.find_all_legal_moves(game.curr_player)
    if len(moves) == 0:
        # if checkmate, return high/low score to incentivize moves that lead to it
        if game.is_square_attacked(game.board.find_king(game.curr_player), game.curr_opponent):
            if maximizing_player:
                return -100000 + depth # white must favor later black checkmates
            else:
                return 100000 - depth # black must favor sooner black checkmates
        else:
            return 0 # stalemate

    if maximizing_player: # white
        max_eval = -100000
        for move in moves:
            gs_copy = copy.deepcopy(game)
            gs_copy.make_move((move[0], move[1]), (move[2], move[3]))
            # recursive step
            eval = minimax(gs_copy, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            # alpha/beta update and pruning
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else: # black
        min_eval = 100000
        for move in moves:
            gs_copy = copy.deepcopy(game)
            gs_copy.make_move((move[0], move[1]), (move[2], move[3]))
            # recursive step
            eval = minimax(gs_copy, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            # alpha/beta update and pruning
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


# function to evaluate the score of a given board using PST (positive = white advantange)
def score_board(board):
    score = 0
    for r in range(8):
        for c in range(8):
            piece = board.board[r][c]
            if piece is not None:
                # material score
                material_score = PIECE_SCORE[piece.type]
                # positional score
                if piece.color == WHITE:
                    idx = r*8 + c # 2D to 1D index
                    pos_score = PIECE_TABLES[piece.type][idx]
                    score += material_score + pos_score
                else:
                    # black pieces use a mirrored PST
                    idx = (r-7)*8 + c
                    pos_score = PIECE_TABLES[piece.type][idx]
                    score -= material_score + pos_score
    return score


### UNUSED
# function to evaluate the score of a given board (positive = white advantange)
def score_board_trivial(board):
    score = 0
    for r in range(8):
        for c in range(8):
            piece = board.board[r][c]
            if piece is not None:
                val = PIECE_SCORE[piece.type]
                if piece.color == WHITE:
                    score += val
                else:
                    score -= val
    return score



# function that returns a random legal move (tuple of tuples) or None, for the given game state
def get_random_move(game):
    valid_moves = game.find_all_legal_moves(game.curr_player)
    if not valid_moves:
        return None # checkmate or stalemate
    chosen_move = random.choice(valid_moves) # pick a random move
    # convert the flat tuple (r, c, r, c) back into two tuples for make_move
    start_pos = (chosen_move[0], chosen_move[1])
    end_pos = (chosen_move[2], chosen_move[3])
    return start_pos, end_pos
