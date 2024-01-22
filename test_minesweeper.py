import unittest
from unittest.mock import patch
from io import StringIO
import pygame
from minesweeper import Minesweeper

class TestMinesweeper(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1))  # Initialize Pygame with a minimal display

    def tearDown(self):
        pygame.quit()

    @patch("sys.stdout", new_callable=StringIO)
    def test_initialization(self, mock_stdout):
        minesweeper = Minesweeper()
        self.assertEqual(minesweeper.WIDTH, 800)
        self.assertEqual(minesweeper.HEIGHT, 800)
        self.assertEqual(minesweeper.GRID_SIZE, 15)
        self.assertEqual(minesweeper.CELL_SIZE, 53)  # Adjust this based on your calculations
        self.assertEqual(minesweeper.NUM_MINES, 15)
        # Add more assertions based on your game initialization

    def test_draw_grid(self):
        minesweeper = Minesweeper()
        with patch("pygame.draw.rect") as mock_draw_rect:
            minesweeper.draw_grid()
            # Add assertions for the expected calls to mock_draw_rect

    def test_reveal_adjacent(self):
        minesweeper = Minesweeper()

        # Helper function to count the number of revealed cells
        def count_revealed():
            return sum(sum(1 for cell in row if cell) for row in minesweeper.revealed)

        # Initial state before any revealing
        self.assertEqual(count_revealed(), 0)

        # Reveal a cell with value > 0
        minesweeper.reveal_adjacent(5, 5, minesweeper.is_revealed)
        self.assertEqual(count_revealed(), 10)  # Only the cell itself

        # Reveal a cell with value > 0 and already revealed
        minesweeper.reveal_adjacent(5, 5, minesweeper.is_revealed)
        self.assertEqual(count_revealed(), 10)  # No change

        # Reveal a cell outside the grid
        minesweeper.reveal_adjacent(20, 20, minesweeper.is_revealed)
        self.assertEqual(count_revealed(), 10)  # No change

    def test_is_running(self):
        minesweeper = Minesweeper()

        # Simulate a left-click event triggering a win (revealing all non-mine cells)
        minesweeper.is_revealed = minesweeper.GRID_SIZE * minesweeper.GRID_SIZE - minesweeper.NUM_MINES
        with patch("pygame.event.get", return_value=[pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (50, 50)})]):
            minesweeper.is_running(pygame.event.Event(pygame.MOUSEBUTTONDOWN))

        self.assertTrue(minesweeper.game_over)
        self.assertTrue(minesweeper.game_win)
        self.assertFalse(minesweeper.game_lose)

        # Simulate a right-click event
        with patch("pygame.event.get", return_value=[pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 3, "pos": (50, 50)})]):
            minesweeper.is_running(pygame.event.Event(pygame.MOUSEBUTTONDOWN))

if __name__ == "__main__":
    unittest.main()
