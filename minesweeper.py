import pygame
import random

class Minesweeper:
    def start_game():
    
    
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = 800, 800
        self.GRID_SIZE = 15
        self.CELL_SIZE = self.WIDTH // self.GRID_SIZE
        self.NUM_MINES = 15

        # Progress tracker
        self.is_revealed = 0

        # Music and Sounds
        pygame.mixer.music.load("Sakura-Girl-Beach-chosic.com_.mp3")
        self.loss_sound = pygame.mixer.Sound("lose_sfx.mp3")
        self.win_sound = pygame.mixer.Sound("win_sfx.mp3")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREY = (200, 200, 200)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.LIGHT_BLUE = (173, 216, 230)

        # Create a Minesweeper grid
        self.grid = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.revealed = [[False for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.flags = [[False for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.mines = set()

        # Place mines randomly
        while len(self.mines) < self.NUM_MINES:
            x, y = random.randint(0, self.GRID_SIZE - 1), random.randint(0, self.GRID_SIZE - 1)
            self.mines.add((x, y))
            self.grid[x][y] = -1  # Mark mine

        # Calculate neighboring mine counts
        for x in range(self.GRID_SIZE):
            for y in range(self.GRID_SIZE):
                if self.grid[x][y] != -1:
                    count = sum(
                        1 for i in range(-1, 2) for j in range(-1, 2)
                        if 0 <= x + i < self.GRID_SIZE and 0 <= y + j < self.GRID_SIZE and self.grid[x + i][y + j] == -1
                    )
                    self.grid[x][y] = count

        # Pygame setup
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Minesweeper")

    def draw_grid(self):
        for x in range(self.GRID_SIZE):
            for y in range(self.GRID_SIZE):
                rect = pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                pygame.draw.rect(self.screen, self.GREY, rect, 1)

    def draw_mine(self, x, y):
        pygame.draw.circle(self.screen, self.BLACK, (x * self.CELL_SIZE + self.CELL_SIZE // 2, y * self.CELL_SIZE + self.CELL_SIZE // 2), self.CELL_SIZE // 2 - 2)

    def draw_number(self, x, y, number):
        font = pygame.font.Font("font.ttf", 14)
        text = font.render(str(number), True, self.BLACK) if number > 0 else font.render(str(number), True, self.BLUE)
        text_rect = text.get_rect(center=(x * self.CELL_SIZE + self.CELL_SIZE // 2, y * self.CELL_SIZE + self.CELL_SIZE // 2))
        self.screen.blit(text, text_rect)

    def draw_flag(self, x, y):
        pygame.draw.polygon(self.screen, self.RED, [(x * self.CELL_SIZE + 5, y * self.CELL_SIZE + 5),
                                                     (x * self.CELL_SIZE + self.CELL_SIZE - 5, y * self.CELL_SIZE + self.CELL_SIZE // 2),
                                                     (x * self.CELL_SIZE + 5, y * self.CELL_SIZE + self.CELL_SIZE - 5)])

    def draw_cell_content(self, x, y):
        if self.revealed[x][y]:
            if (x, y) in self.mines and not self.game_over:
                self.draw_mine(x, y)
            else:
                self.draw_number(x, y, self.grid[x][y])

    def draw_revealed(self, x, y):
        rect = pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
        pygame.draw.rect(self.screen, self.BLUE, rect)  # Use blue color for revealed squares
        pygame.draw.rect(self.screen, self.LIGHT_BLUE, rect, 1)

        if self.flags[x][y]:
            self.draw_flag(x, y)
        else:
            self.draw_cell_content(x, y)

    def reveal_adjacent(self, x, y, reveal_count):
        if 0 <= x < self.GRID_SIZE and 0 <= y < self.GRID_SIZE and not self.revealed[x][y]:
            self.is_revealed += 1
            if self.is_revealed == self.GRID_SIZE * self.GRID_SIZE - self.NUM_MINES:
                self.win_screen()
                return
            self.revealed[x][y] = True
            if self.grid[x][y] == 0:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        self.reveal_adjacent(x + i, y + j, reveal_count)

    def is_running(self, event):
        x, y = event.pos[0] // self.CELL_SIZE, event.pos[1] // self.CELL_SIZE

        if event.button == 1:  # Left-click
            if (x, y) in self.mines:
                # Game over, reveal all mines
                for mine_x, mine_y in self.mines:
                    self.draw_mine(mine_x, mine_y)
                pygame.display.flip()
                pygame.time.delay(2000)
                self.game_over = True
                self.loss_screen()
            else:
                # Reveal the clicked cell and its adjacent tiles
                self.reveal_adjacent(x, y, self.is_revealed)

        elif event.button == 3:  # Right-click
            self.flags[x][y] = not self.flags[x][y]

    def get_font(self, size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("font.ttf", size)

    def intro(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    running = False

            self.screen.fill(self.WHITE)
            intro_img = pygame.image.load('Bomb.png')
            self.screen.blit(intro_img, (0, 0))
            pygame.display.update()

    def win_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            pygame.mixer.music.set_volume(0)
            self.win_sound.set_volume(0.05)
            self.win_sound.play(0)

            self.screen.fill(self.WHITE)
            PLAY_TEXT = self.get_font(45).render("YOU WIN", True, self.BLACK)
            PLAY_RECT = PLAY_TEXT.get_rect(center=(400, 400))
            self.screen.blit(PLAY_TEXT, PLAY_RECT)

            pygame.display.update()

    def loss_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            pygame.mixer.music.set_volume(0)
            self.loss_sound.set_volume(0.05)
            pygame.mixer.Sound.play(self.loss_sound, 1)
            self.screen.fill(self.WHITE)
            PLAY_TEXT = self.get_font(45).render("YOU LOSE", True, self.BLACK)
            PLAY_RECT = PLAY_TEXT.get_rect(center=(400, 400))
            self.screen.blit(PLAY_TEXT, PLAY_RECT)

            pygame.display.update()

    def main(self):
        self.game_over = False
        self.game_win = False
        self.game_lose = False
        self.is_revealed = 0

        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)

        self.intro()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if not self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_win:
                        self.game_over = True
                        self.win_screen()
                    elif self.game_lose:
                        self.game_over = True
                        self.loss_screen()
                    else:
                        self.is_running(event)

            self.screen.fill(self.WHITE)
            self.draw_grid()

            for x in range(self.GRID_SIZE):
                for y in range(self.GRID_SIZE):
                    if self.revealed[x][y]:
                        self.draw_revealed(x, y)
                    elif self.flags[x][y]:
                        self.draw_flag(x, y)

            pygame.display.flip()

if __name__ == "__main__":
    minesweeper = Minesweeper()
    minesweeper.main()


"""""
add multiple difficulties by increasing the grid amount and num of bombs
The game loops
The first tile can't be a bomb
The first click at the very least reveals all non bomb tiles in the 3by3 area
improve aesthetic
add sound effects
add a timer
add a flag / remaining bomb counter
"""""