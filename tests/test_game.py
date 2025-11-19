
import unittest
import sys

sys.path.append('..')
from utils import _n2c
from piece import Piece, WHITE, BLACK
from board import Board
from game import Game


class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_pawn_forward_two_squares(self):
        # test that e2e4 is legal
        start_pos = _n2c('e2')
        end_pos = _n2c('e4')
        is_legal, msg = self.game.is_move_legal(start_pos, end_pos, WHITE)
        self.assertTrue(is_legal, msg)
    
    def test_illegal_pawn_move_blocked(self):
        # test that e2e4 is NOT legal if a piece is at e3
        self.game.board.board[2][4] = Piece(BLACK, "pawn") # blocking piece
        start_pos = _n2c('e2')
        end_pos = _n2c('e4')
        is_legal, msg = self.game.is_move_legal(start_pos, end_pos, WHITE)
        self.assertFalse(is_legal)
        self.assertIn("obstructed", msg)
    
    def test_illegal_capture_own_piece(self):
        # test moving the rook at a1 to a2 (where there is a white pawn)
        start_pos = _n2c('a1')
        end_pos = _n2c('a2')
        is_legal, msg = self.game.is_move_legal(start_pos, end_pos, WHITE)
        self.assertFalse(is_legal)
        self.assertIn("own piece", msg)
    
    def test_illegal_putting_king_in_check(self):
        # setup a custom scenario:
        # white king at e2, black rook at a2, white pawn at d2, white to move
        # moving the white pawn at d2 to d4 would expose the king to check
        self.game.board.board = [[None for _ in range(8)] for _ in range(8)] # clear board
        self.game.board.board[1][4] = Piece(WHITE, "king")   # king at e2
        self.game.board.board[1][0] = Piece(BLACK, "rook")   # rook at a2
        self.game.board.board[1][3] = Piece(WHITE, "pawn")   # pawn at d2
        self.game.curr_player = WHITE
        self.game.curr_opponent = BLACK
        # make moves
        start_pos = _n2c('d2')
        end_pos = _n2c('d4') # this move would open the file for the rook
        is_legal, msg = self.game.is_move_legal(start_pos, end_pos, WHITE)
        self.assertFalse(is_legal)
        self.assertIn("own king", msg)
    
    def test_fools_mate(self):
        # a full scenario test for checkmate
        # 1. f3 e6
        self.game.board.move_piece(_n2c('f2'), _n2c('f3'))
        self.game.board.move_piece(_n2c('e7'), _n2c('e6'))
        # 2. g4 Qh4#
        self.game.board.move_piece(_n2c('g2'), _n2c('g4'))
        self.game.board.move_piece(_n2c('d8'), _n2c('h4'))
        # after the moves, check for checkmate on white's turn
        # king is in check, and there should be no legal moves
        white_king_pos = self.game.board.find_king(WHITE)
        self.assertTrue(self.game.is_square_attacked(white_king_pos, BLACK))
        white_legal_moves = self.game.find_all_legal_moves(WHITE)
        self.assertEqual(len(white_legal_moves), 0)