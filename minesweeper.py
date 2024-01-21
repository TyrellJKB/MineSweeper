import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
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

def draw_revealed(x, y):
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, WHITE, rect)
    pygame.draw.rect(screen, GRAY, rect, 1)

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                if (x, y) in mines:
                    # Game over, reveal all mines
                    for mine_x, mine_y in mines:
                        draw_mine(mine_x, mine_y)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    pygame.quit()
                    quit()
                else:
                    # Reveal the clicked cell
                    revealed[x][y] = True

        screen.fill(WHITE)
        draw_grid()

        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if revealed[x][y]:
                    if (x, y) in mines:
                        draw_mine(x, y)
                    else:
                        draw_number(x, y, grid[x][y])
                elif (x, y) in mines:  # Draw mines when the game is won
                    draw_mine(x, y)

        pygame.display.flip()

if __name__ == "__main__":
    main()
