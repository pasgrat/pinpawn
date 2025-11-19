
import unittest
import sys

sys.path.append('..')
from piece import Piece, WHITE, BLACK
from board import Board


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_setup_board(self):
        self.board.setup_board()
        self.assertIsInstance(self.board.board[0][0], Piece)
        self.assertEqual(self.board.board[0][0].type, "rook")
        self.assertEqual(self.board.board[0][0].color, WHITE)
        self.assertIsInstance(self.board.board[6][4], Piece)
        self.assertEqual(self.board.board[6][4].type, "pawn")
        self.assertEqual(self.board.board[6][4].color, BLACK)
        self.assertIsNone(self.board.board[3][4])

    def test_is_path_clear_horizontal(self):
        self.assertTrue(self.board.is_path_clear((3, 0), (3, 7)))
        self.board.board[3][4] = Piece(WHITE, "pawn") # blocking piece
        self.assertFalse(self.board.is_path_clear((3, 0), (3, 7)))
    
    def test_is_path_clear_vertical(self):
        self.assertTrue(self.board.is_path_clear((0, 2), (0, 5)))
        self.board.board[0][4] = Piece(WHITE, "pawn") # blocking piece
        self.assertFalse(self.board.is_path_clear((0, 2), (0, 5)))

    def test_is_path_clear_diagonal(self):
        self.assertTrue(self.board.is_path_clear((0, 0), (5, 5)))
        self.board.board[2][2] = Piece(BLACK, "knight") # blocking piece
        self.assertFalse(self.board.is_path_clear((0, 0), (5, 5)))

    def test_move_piece(self):
        piece_to_move = Piece(WHITE, "queen")
        start_pos = (3, 3)
        end_pos = (5, 5)
        # place the piece
        self.board.board[start_pos[0]][start_pos[1]] = piece_to_move
        self.assertEqual(self.board.board[start_pos[0]][start_pos[1]], piece_to_move)
        # move the piece
        self.board.move_piece(start_pos, end_pos)
        self.assertIsNone(self.board.board[start_pos[0]][start_pos[1]])
        self.assertEqual(self.board.board[end_pos[0]][end_pos[1]], piece_to_move)