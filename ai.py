
import random
import copy
from game import WHITE, BLACK


# piece values (positive for white, negative for black)
PIECE_SCORE = {"king": 0, "queen": 9, "rook": 5, "bishop": 3, "knight": 3,"pawn": 1}



# function to find the best move on a given game state, using minimax with alpha-beta pruning
def find_best_move(game):
    DEPTH = 2 # minimax search depth
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
            evaluation = minimax(game_copy, DEPTH - 1, alpha, beta, False) # recursive call
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
            evaluation = minimax(game_copy, DEPTH - 1, alpha, beta, True)
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
        return score_board(game.board) # use current score (high/low if checkmate)

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


# function to evaluate the score of a given board (positive = white advantange)
def score_board(board):
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



### UNUSED
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
