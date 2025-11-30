
import pygame, sys, random
from game import Game, WHITE, BLACK
from ai import get_random_move, get_minimax_move



# CONSTANTS
WIDTH, HEIGHT = 512, 512 # window size
DIMENSION = 8 # chess board
SQ_SIZE = WIDTH // DIMENSION # size of single square
MAX_FPS = 15
IMAGES = {}

# GUI COLORS
BG_COLOR = pygame.Color("white")
BTN_COLOR = pygame.Color("lightgray")
BTN_HOVER = pygame.Color("darkgray")
BTN_SELECTED = pygame.Color("yellow")
TEXT_COLOR = pygame.Color("black")

# DIFFICULTY
DIFF_VERY_EASY = 0
DIFF_EASY = 1
DIFF_MEDIUM = 2
DIFF_HARD = 3



# function to load the graphics of the game from the /images folder
# naming convention: 'wP' for white pawn, 'bK' for black king, etc.
def load_graphics():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        image_path = f"images/{piece}.png"
        try:
            image = pygame.image.load(image_path)
            IMAGES[piece] = pygame.transform.scale(image, (SQ_SIZE, SQ_SIZE)) # icon size adjustment
        except FileNotFoundError:
            print(f"ERROR: Could not load image {image_path}")



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PinPawn")
    # show main menu
    player_color, difficulty = main_menu(screen)
    # run the game when user selects the game mode, difficulty, and clicks "Play"
    run_game(screen, player_color, difficulty)



# function to display the main menu of the game
def main_menu(screen):
    clock = pygame.time.Clock()
    font_title = pygame.font.SysFont("Helvetica", 48, True, False)
    font_sub = pygame.font.SysFont("Helvetica", 20)

    # buttons size and position parameters
    btn_w, btn_h = 120, 40
    center_x = WIDTH // 2
    row1_y, row2_y, row3_y = 130, 280, 420
    gap = 10
    total_w = (btn_w * 2) + (gap * 2)
    start_x = center_x - (total_w // 2)
    # buttons row 1 (game mode)
    white_btn  = pygame.Rect(center_x-190, row1_y, 120, btn_h)
    black_btn  = pygame.Rect(center_x-60, row1_y, 120, btn_h)
    random_btn = pygame.Rect(center_x+70, row1_y, 120, btn_h)
    pvp_btn    = pygame.Rect(center_x-60, row1_y+50, 120, btn_h)
    # buttons row 2 (difficulty)
    diff0_btn = pygame.Rect(start_x,               row2_y,    btn_w, btn_h)
    diff1_btn = pygame.Rect(start_x + (btn_w+gap), row2_y,    btn_w, btn_h)
    diff2_btn = pygame.Rect(start_x,               row2_y+50, btn_w, btn_h)
    diff3_btn = pygame.Rect(start_x + (btn_w+gap), row2_y+50, btn_w, btn_h)
    # buttons row 3 (play)
    play_btn = pygame.Rect(center_x - (btn_w+80)//2, row3_y, btn_w+80, btn_h+10)
    
    # state
    selected_option = WHITE # default
    selected_difficulty = DIFF_MEDIUM # default
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        # --- EVENT HANDLING SECTION ---

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # color choice logic
                if white_btn.collidepoint(mouse_pos):
                    selected_option = WHITE
                elif black_btn.collidepoint(mouse_pos):
                    selected_option = BLACK
                elif random_btn.collidepoint(mouse_pos):
                    selected_option = "random"
                elif pvp_btn.collidepoint(mouse_pos):
                    selected_option = "PVP"
                # difficulty choice logic
                if selected_option != "PVP":
                    if diff0_btn.collidepoint(mouse_pos): selected_difficulty = DIFF_VERY_EASY
                    elif diff1_btn.collidepoint(mouse_pos): selected_difficulty = DIFF_EASY
                    elif diff2_btn.collidepoint(mouse_pos): selected_difficulty = DIFF_MEDIUM
                    elif diff3_btn.collidepoint(mouse_pos): selected_difficulty = DIFF_HARD
                # play button logic
                if play_btn.collidepoint(mouse_pos):
                    final_color = selected_option
                    if final_color == "random":
                        final_color = random.choice([WHITE, BLACK]) # necessary to correctly display random button
                    return final_color, selected_difficulty

        # --- DRAWING SECTION ---

        # draw the menu
        screen.fill(BG_COLOR)
        # game title
        title_surf = font_title.render("PinPawn", True, TEXT_COLOR)
        title_rect = title_surf.get_rect(center=(WIDTH//2, 50))
        screen.blit(title_surf, title_rect)
        # subtitle
        sub_surf = font_sub.render("Play as:", True, TEXT_COLOR)
        screen.blit(sub_surf, (WIDTH//2 - sub_surf.get_width()//2, row1_y-30))
        # buttons row 1 (game mode)
        draw_button(screen, white_btn, "White", is_selected=(selected_option == WHITE), is_hovered=white_btn.collidepoint(mouse_pos))
        draw_button(screen, black_btn, "Black", is_selected=(selected_option == BLACK), is_hovered=black_btn.collidepoint(mouse_pos))
        draw_button(screen, random_btn, "Random", is_selected=(selected_option == "random"), is_hovered=random_btn.collidepoint(mouse_pos))
        draw_button(screen, pvp_btn, "2 Players", is_selected=(selected_option == "PVP"), is_hovered=pvp_btn.collidepoint(mouse_pos))
        # buttons row 2 (difficulty)
        if selected_option != "PVP":
            sub_diff = font_sub.render("Select AI difficulty:", True, TEXT_COLOR)
            screen.blit(sub_diff, (WIDTH//2 - sub_diff.get_width()//2, row2_y-30))
            draw_button(screen, diff0_btn, "Easiest", is_selected=(selected_difficulty == DIFF_VERY_EASY), is_hovered=diff0_btn.collidepoint(mouse_pos))
            draw_button(screen, diff1_btn, "Easy", is_selected=(selected_difficulty == DIFF_EASY), is_hovered=diff1_btn.collidepoint(mouse_pos))
            draw_button(screen, diff2_btn, "Medium", is_selected=(selected_difficulty == DIFF_MEDIUM), is_hovered=diff2_btn.collidepoint(mouse_pos))
            draw_button(screen, diff3_btn, "Hard", is_selected=(selected_difficulty == DIFF_HARD), is_hovered=diff3_btn.collidepoint(mouse_pos))
        # buttons row 3 (play)
        draw_button(screen, play_btn, "PLAY", is_hovered=play_btn.collidepoint(mouse_pos))
        # display the menu
        pygame.display.flip()
        clock.tick(MAX_FPS)



# function to run the actual chess game
def run_game(screen, player_color, difficulty):
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    
    game = Game() # initialize game engine
    load_graphics() # load graphics
    
    # players configuration
    white_is_human = True
    black_is_human = True

    if player_color == WHITE:
        black_is_human = False
    elif player_color == BLACK:
        white_is_human = False
    # if player_color == None, both are True (2 players mode)

    running = True
    game_over = False
    game_over_text = ""
    selected_square = None # tuple: (row, col)
    player_clicks = [] # tracks player clicks, e.g. [(6, 4), (4, 4)]
    
    # game loop
    while running:
        
        # 0. determine if turn is for human or AI
        is_human_turn = False
        if game.curr_player == WHITE and white_is_human:
            is_human_turn = True
        elif game.curr_player == BLACK and black_is_human:
            is_human_turn = True

        # 1. handle events for human turn
        for event in pygame.event.get():
        
            # if user quits the game
            if event.type == pygame.QUIT:
                running = False
            
            # handle mouse clicks only if turn is human)
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and is_human_turn:
                location = pygame.mouse.get_pos() # location of mouse as (x, y) tuple
                col = location[0] // SQ_SIZE
                row = 7 - location[1] // SQ_SIZE # pygame 0,0 is top left
                # the Y axis is inverted so that the bottom (screen row 7) corresponds to board row 0
                
                # check if user clicked the same square twice (undo selection)
                if selected_square == (row, col):
                    selected_square = None
                    player_clicks = []
                else:
                    selected_square = (row, col)
                    player_clicks.append(selected_square)
                
                # if there are two different clicks, try to make a move
                if len(player_clicks) == 2:
                    start_pos = player_clicks[0]
                    end_pos = player_clicks[1]
                    
                    # validate and perform move
                    is_legal, error_msg = game.is_move_legal(start_pos, end_pos, game.curr_player)
                    if is_legal:
                        # make the move
                        game.make_move(start_pos, end_pos)
                        print(f"Move made: {start_pos} -> {end_pos}") # console feedback
                        # reset clicks after valid move
                        selected_square = None
                        player_clicks = [] # reset clicks

                    else:
                        print(error_msg) # print error to console
                        player_clicks = [selected_square] # keep the second click as the new start
        
        # 2. AI turn logic
        if not game_over and not is_human_turn:
            pygame.time.wait(500) # wait at least 0.5 seconds to make it look more realistic
            # get AI move
            if difficulty == DIFF_VERY_EASY:
                ai_move = get_random_move(game)
            else:
                ai_move = get_minimax_move(game, difficulty)
            # make AI move
            if ai_move is None:
                game_over = True # safety check
            else:
                start_pos, end_pos = ai_move
                game.make_move(start_pos, end_pos)
                print(f"AI Move: {start_pos} -> {end_pos}")

        # 3. check for game over
        moves = game.find_all_legal_moves(game.curr_player)
        if len(moves) == 0:
            game_over = True
            king_pos = game.board.find_king(game.curr_player)
            if game.is_square_attacked(king_pos, game.curr_opponent):
                # king is in check, checkmate
                winner = "White" if game.curr_opponent == WHITE else "Black"
                game_over_text = f"Checkmate! {winner} wins!"
            else:
                # king is not in check, stalemate
                game_over_text = "Stalemate! It's a draw."

        # 4. display board
        draw_game_state(screen, game, selected_square)
        if game_over:
            draw_end_game_text(screen, game_over_text)
        clock.tick(MAX_FPS)
        pygame.display.flip()



# higher-level function to draw the game board and pieces
def draw_game_state(screen, game, selected_square):
    draw_board(screen, selected_square)
    draw_pieces(screen, game.board)


# function to draw the chess board
def draw_board(screen, selected_square):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)] # pattern: if r+c is even = white, else black
            # highlight selected square
            if selected_square == (7-r, c): # 7-r is to account for inverted Y axis
                color = pygame.Color("yellow")
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


# function to draw the individual chess pieces
def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board.board[7-r][c] # 7-r is to account for inverted Y axis
            if piece is not None:
                # map the Piece object to the image key (e.g. 'wR')
                color_prefix = 'w' if piece.color == WHITE else 'b'
                type_map = {"pawn": "P", "rook": "R", "knight": "N", "bishop": "B", "queen": "Q", "king": "K"}
                key = color_prefix + type_map[piece.type]
                if key in IMAGES:
                    screen.blit(IMAGES[key], pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


# function to draw text on top of the board
def draw_end_game_text(screen, text):
    # create a font object (system font, size 32, bold)
    font = pygame.font.SysFont("Helvetica", 32, True, False)
    # render the text
    text_object = font.render(text, 0, pygame.Color("Red"))
    text_location = pygame.Rect(0, 0, WIDTH, HEIGHT).move(
        WIDTH // 2 - text_object.get_width() // 2, 
        HEIGHT // 2 - text_object.get_height() // 2
    )
    screen.blit(text_object, text_location.move(2, 2))


# function to draw buttons on the menu screen
def draw_button(screen, rect, text, is_selected=False, is_hovered=False):
    color = BTN_SELECTED if is_selected else (BTN_HOVER if is_hovered else BTN_COLOR)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, TEXT_COLOR, rect, 2) # border
    font = pygame.font.SysFont("Helvetica", 24, True, False)
    text_surf = font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)



# EXECUTION

if __name__ == "__main__":
    main()
