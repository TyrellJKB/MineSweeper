import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
NUM_MINES = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Create a Minesweeper grid
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
flags = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
mines = set()

# Place mines randomly
while len(mines) < NUM_MINES:
    x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
    mines.add((x, y))
    grid[x][y] = -1  # Mark mine

# Calculate neighboring mine counts
for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        if grid[x][y] != -1:
            count = sum(
                1
                for i in range(-1, 2)
                for j in range(-1, 2)
                if 0 <= x + i < GRID_SIZE and 0 <= y + j < GRID_SIZE and grid[x + i][y + j] == -1
            )
            grid[x][y] = count

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)

def draw_mine(x, y):
    pygame.draw.circle(screen, BLACK, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 2)

def draw_number(x, y, number):
    font = pygame.font.Font(None, 36)
    text = font.render(str(number), True, BLACK)
    text_rect = text.get_rect(center=(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2))
    screen.blit(text, text_rect)

def draw_flag(x, y):
    pygame.draw.polygon(screen, RED, [(x * CELL_SIZE + 5, y * CELL_SIZE + 5),
                                      (x * CELL_SIZE + CELL_SIZE - 5, y * CELL_SIZE + CELL_SIZE // 2),
                                      (x * CELL_SIZE + 5, y * CELL_SIZE + CELL_SIZE - 5)])

def draw_cell_content(x, y):
    if revealed[x][y]:
        if (x, y) in mines and not game_over:
            draw_mine(x, y)
        else:
            draw_number(x, y, grid[x][y])

def draw_revealed(x, y):
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, (0, 0, 255), rect)  # Use blue color for revealed squares
    pygame.draw.rect(screen, GRAY, rect, 1)

    if flags[x][y]:
        draw_flag(x, y)
    else:
        draw_cell_content(x, y)

def reveal_adjacent(x, y):
    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and not revealed[x][y]:
        revealed[x][y] = True
        if grid[x][y] == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    reveal_adjacent(x + i, y + j)

def main():
    global game_over
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE

                if event.button == 1:  # Left-click
                    if (x, y) in mines:
                        # Game over, reveal all mines
                        for mine_x, mine_y in mines:
                            draw_mine(mine_x, mine_y)
                        pygame.display.flip()
                        pygame.time.delay(2000)
                        pygame.quit()
                        quit()
                        game_over = True
                    else:
                        # Reveal the clicked cell and its adjacent tiles
                        reveal_adjacent(x, y)

                elif event.button == 3:  # Right-click
                    flags[x][y] = not flags[x][y]

        screen.fill(WHITE)
        draw_grid()

        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if revealed[x][y]:
                    draw_revealed(x, y)
                elif flags[x][y]:
                    draw_flag(x, y)

        pygame.display.flip()

if __name__ == "__main__":
    main()


"""""
The game loops
Theres a win screen
There is a lose screen
The first tile can't be a bomb
The first click at the very least reveals all non bomb tiles in the 3by3 area
"""""