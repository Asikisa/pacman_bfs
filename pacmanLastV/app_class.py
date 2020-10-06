import sys
import time

from pacman_class import *

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.start_time = time.time()
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH // COLS
        self.cell_height = MAZE_HEIGHT // ROWS
        self.walls = []
        self.pacmen = []
        self.e_pos = []
        self.space = []
        self.c_pos = None
        self.load()
        self.make_pacman()

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
                self.game_over_events()
            else:
                self.running = False
        pygame.quit()
        sys.exit()

    # draw function
    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        # Opening walls file
        # Creating walls list with co-ords of walls
        # stored as  a vector
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                    elif char == "0":
                        element = str(str(xidx) + ' ' + str(yidx))
                        self.space.append(element)
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx * self.cell_width, yidx * self.cell_height,
                                                                  self.cell_width, self.cell_height))
        self.c_pos = self.choose_pos()

    def make_pacman(self):
        self.e_pos = self.choose_pos()
        self.pacmen.append(Pacman(self, vec(self.e_pos)))

    def draw_grid(self):
        for x in range(WIDTH // self.cell_width):
            pygame.draw.line(self.background, GREY, (x * self.cell_width, 0),
                             (x * self.cell_width, HEIGHT))
        for x in range(HEIGHT // self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x * self.cell_height),
                             (WIDTH, x * self.cell_height))

    # intro functions
    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH SPACE BAR', self.screen, [
            WIDTH // 2, HEIGHT // 2 - 50], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        self.draw_text('1 PACMAN ONLY', self.screen, [
            WIDTH // 2, HEIGHT // 2 + 50], START_TEXT_SIZE, (44, 167, 198), START_FONT, centered=True)
        pygame.display.update()

    def choose_pos(self):
        chosen_point = self.space[random.randrange(len(self.space))]
        self.space.remove(chosen_point)
        chosen_point = chosen_point.split()
        res = [int(chosen_point[0]), int(chosen_point[1])]
        return res

    # playing functions
    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def playing_update(self):
        for pacman in self.pacmen:
            pacman.update()
        for pacman in self.pacmen:
            if pacman.grid_pos == self.c_pos:
                self.remove_life()

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
        self.draw_coins()
       # self.draw_grid()
        self.draw_text('SEARCHING FOR CANDY...', self.screen, [WIDTH // 2 + 30, 0], 18, WHITE, START_FONT)
        for pacman in self.pacmen:
            pacman.draw()
        pygame.display.update()

    def remove_life(self):
        self.pacmen[0].time_to_go = time.time() - self.pacmen[0].start_time
        self.state = "game over"

    def draw_coins(self):
        pygame.draw.circle(self.screen, (255, 142, 212),
                           (int(self.c_pos[0] * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2,
                            int(self.c_pos[1] * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 5)

    # game over functions
    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.screen.fill(BLACK)
        quit_text = "Press the escape button to QUIT"
        titles_text = "Created by Vera & Asya"
        time_for_algorithm = self.pacmen[0].time_for_algorithm
        time_to_go = self.pacmen[0].time_to_go
        number_steps = self.pacmen[0].steps
        number_all_steps = self.pacmen[0].all_steps
        self.draw_text(titles_text, self.screen, [WIDTH // 2, 130], 36, (190, 190, 190), "arial", centered=True)
        self.draw_text("Time for algorithm: " + str(time_for_algorithm), self.screen, [WIDTH // 2, 250], 20, RED,
                       "arial", centered=True)
        self.draw_text("Time to go: " + str(time_to_go), self.screen, [WIDTH // 2, 280], 20, RED,
                       "arial", centered=True)
        self.draw_text("Shortest path number of steps: " + str(number_steps), self.screen, [WIDTH // 2, 310], 20, RED,
                       "arial", centered=True)
        self.draw_text("Number of all steps within a search: " + str(number_all_steps), self.screen, [WIDTH // 2, 340],
                       20, RED,
                       "arial", centered=True)
        self.draw_text(quit_text, self.screen, [
            WIDTH // 2, HEIGHT // 1.5], 36, (190, 190, 190), "arial", centered=True)
        pygame.display.update()
