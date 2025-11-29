
import random


# function that returns a random legal move (tuple of tuples) or None, for the given game state
def get_random_move(game_state):
    valid_moves = game_state.find_all_legal_moves(game_state.curr_player)
    if not valid_moves:
        return None # checkmate or stalemate
    chosen_move = random.choice(valid_moves) # pick a random move
    # convert the flat tuple (r, c, r, c) back into two tuples for make_move
    start_pos = (chosen_move[0], chosen_move[1])
    end_pos = (chosen_move[2], chosen_move[3])
    return start_pos, end_pos
