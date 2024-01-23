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

if __name__ == "__main__":
    unittest.main()
