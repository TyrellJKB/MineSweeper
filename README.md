# Minesweeper - Hazard Hunt

## Overview

Welcome to the Minesweeper - Hazard Hunt repository! This Python implementation of the classic Minesweeper game provides a captivating gaming experience with a graphical user interface built using the Pygame library. Uncover hidden mines, strategically flag them, and navigate the grid to victory.

## Features

1. **Grid Setup:**
    - The game grid is initialized with a specified size and number of mines.
    - Mines are randomly placed on the grid, and neighboring mine counts are calculated.

2. **User Interface:**
    - Utilizes Pygame for a graphical user interface.
    - Cells are revealed or flagged by left or right-clicking, respectively.

3. **Sounds and Music:**
    - Includes background music, win and lose sound effects, and interactive sounds during gameplay.

4. **Gameplay Mechanics:**
    - Revealing a cell with a mine ends the game in a loss.
    - Flagging all mines and revealing all non-mine cells results in a win.

5. **Game Over Screens:**
    - Displays a "You Win" or "You Lose" screen upon game completion.

6. **Difficulty Levels:**
    - Currently supports a single difficulty level with a fixed grid size and number of mines.
    - This can be manually ammened by editing the GRID_SIZE and NUM_MINES variables

## Functionality

### Grid Initialization

The grid is initialized with the specified size, and mines are randomly placed. Neighboring mine counts are calculated for each cell.

### Game Logic

- Left-clicking reveals a cell. If the revealed cell contains a mine, the game ends in a loss.
- Right-clicking flags or unflags a cell.
- The game ends in a win when all non-mine cells are revealed and all mines are flagged.

### Game Over Screens

Distinct screens are displayed for winning and losing scenarios, featuring appropriate messages and effects.

### Calculate Neighboring Mines

The following loop iterates through each cell in the grid and calculates the number of neighboring mines for each cell. It checks the eight adjacent positions around the current cell, ensuring that the indices are within the grid bounds. If a neighboring cell contains a mine, the count is incremented.

```python
for x in range(self.GRID_SIZE):
    for y in range(self.GRID_SIZE):
        if self.grid[x][y] != -1:
            count = sum(
                1 for i in range(-1, 2) for j in range(-1, 2)
                if 0 <= x + i < self.GRID_SIZE and 0 <= y + j < self.GRID_SIZE and self.grid[x + i][y + j] == -1
            )
            self.grid[x][y] = count
```

### Reveal Adjacent Method

The `reveal_adjacent` method recursively reveals adjacent cells in a depth-first manner. It starts at the specified cell `(x, y)` and reveals it. If the cell is empty, the method is called recursively for all adjacent cells. The recursion continues until all adjacent cells are revealed, providing a cascade effect.

```python
def reveal_adjacent(self, x, y, reveal_count):
    if 0 <= x < self.GRID_SIZE and 0 <= y < self.GRID_SIZE and not self.revealed[x][y]:
        self.is_revealed += 1
        if self.is_revealed == self.GRID_SIZE * self.GRID_SIZE - self.NUM_MINES:
            self.game_win = True
            return
        self.revealed[x][y] = True
        if self.grid[x][y] == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    self.reveal_adjacent(x + i, y + j, reveal_count)
```

## Planned Enhancements

1. **Menu System:**
    - Implement a menu system with options to start a new game, choose difficulty levels, and access additional features.

2. **Multiple Difficulty Levels:**
    - Add support for multiple difficulty levels by increasing the grid size and adjusting the number of mines.

3. **Improved Aesthetics:**
    - Enhance the visual appeal of the game with improved graphics and animations.

4. **Leaderboards:**
    - Implement a leaderboard system to track and display high scores.

5. **Timer:**
    - Add a timer to track the duration of each game.

6. **Flag / Remaining Bomb Counter:**
    - Display a counter indicating the number of flags placed and the remaining bombs.

7. **Volume Mixer:**
    - Incorporate a volume mixer to allow players to adjust the game's audio levels.

8. **First Click Safety:**
    - Ensure that the first click does not reveal a mine, providing a safer start for the player.
