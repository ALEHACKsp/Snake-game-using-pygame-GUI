from random import randint
import pygame

WINDOW_WIDTH = 510
MOVE_INCREMENT = 30
GAME_SPEED = 10
ROWS = 17

snake_color = (78, 124, 246)
fruit_color = (231, 71, 29)
line_color = (255, 255, 255)
boarder_color = (64, 139, 4)
checker_board = ((134, 209, 73), (168, 215, 81))

flag = True
score = 0
max_score = 0

pygame.init()
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_WIDTH))


def text_objects(text, font):
    text_surface = font.render(text, True, (0, 0, 0))
    return text_surface, text_surface.get_rect()


def message_display(text, x, y):
    large_text = pygame.font.Font('freesansbold.ttf', 30)
    text_surf, text_rect = text_objects(text, large_text)
    text_rect.center = (x, y)
    win.blit(text_surf, text_rect)


class Game:
    def __init__(self, game_map):
        self.game_map = game_map
        self.fruit_x, self.fruit_y = self.random_square()

    def draw_map(self):
        # Bars
        if self.game_map == 0:
            for i in range(ROWS):
                # Vertical, Horizontal
                x = i * 30
                y = i * 30

                # vertical, horizontal
                if i == 16:
                    pygame.draw.line(win, line_color, (x, 0), (x, WINDOW_WIDTH))
                    pygame.draw.line(win, line_color, (0, y), (WINDOW_WIDTH, y))
                    pygame.draw.line(win, line_color, (x + 29, 0), (x + 29, WINDOW_WIDTH))
                    pygame.draw.line(win, line_color, (0, y + 29), (WINDOW_WIDTH, y + 29))
                else:
                    pygame.draw.line(win, line_color, (x, 0), (x, WINDOW_WIDTH))
                    pygame.draw.line(win, line_color, (0, y), (WINDOW_WIDTH, y))
        # Checkerboard
        elif self.game_map == 1:
            switch = True
            x = 0
            for i in range(ROWS+1):
                y = 0
                for j in range(1, 18):
                    if i != 0:
                        if (switch and j % 2 == 0) or (not switch and j % 2 != 0):  # even
                            pygame.draw.rect(win, checker_board[1], (x, y, 30, 30))
                    y = y + 30
                switch = not switch
                x = i * 30

    def draw_boarder_and_score(self):
        pygame.draw.rect(win, boarder_color, (0, 0, 510, 30)) # ---- top
        pygame.draw.rect(win, boarder_color, (0, 0, 30, 510)) # |--- left
        pygame.draw.rect(win, boarder_color, (0, 480, 510, 30)) # ---- bottom
        pygame.draw.rect(win, boarder_color, (480, 0, 30, 510)) # ---| right
        msg = "Score: " + str(score)
        message_display(msg, 87, 17)

    def random_square(self):
        row = randint(1, ROWS - 2)
        x = row * 30
        y = row * 30
        return x, y

    def manage_fruit(self):
        # Draw the fruit
        if (self.fruit_x, self.fruit_y) not in snake.snake_body:
            pygame.draw.circle(win, fruit_color, (self.fruit_x + 15, self.fruit_y + 15), 10)

        if (self.fruit_x, self.fruit_y) in snake.snake_body:
            global score
            snake.add_body()
            score = score + 1
            self.fruit_x, self.fruit_y = self.random_square()

    def check_collisions(self):
        # in itself
        head_pos_x, head_pos_y = snake.snake_body[0]
        if (head_pos_x, head_pos_y) in snake.snake_body[1:]:
            snake.snake_body = [(210, 240), (180, 240), (150, 240)]
            snake.direction = "Right"
            return False

        # Boundaries
        for x, y in snake.snake_body:
            if x < 30 or x >= 480 or y < 30 or y >= 480:
                snake.snake_body = [(210, 240), (180, 240), (150, 240)]
                snake.direction = "Right"
                return False

        return True

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_RIGHT]:
                    snake.direction = "Right"
                elif keys[pygame.K_LEFT]:
                    snake.direction = "Left"
                elif keys[pygame.K_UP]:
                    snake.direction = "Up"
                elif keys[pygame.K_DOWN]:
                    snake.direction = "Down"


class Snake:
    def __init__(self):
        self.snake_body = [(210, 240), (180, 240), (150, 240)]
        self.direction = "Right"

    def move(self):
        snake_pos_x, snake_pos_y = self.snake_body[0]
        new_head_pos = (snake_pos_x, snake_pos_y)

        if self.direction == "Right":
            new_head_pos = (snake_pos_x + MOVE_INCREMENT, snake_pos_y)
        if self.direction == "Left":
            new_head_pos = (snake_pos_x - MOVE_INCREMENT, snake_pos_y)
        if self.direction == "Up":
            new_head_pos = (snake_pos_x, snake_pos_y - MOVE_INCREMENT)
        if self.direction == "Down":
            new_head_pos = (snake_pos_x, snake_pos_y + MOVE_INCREMENT)

        self.snake_body = [new_head_pos] + self.snake_body[:-1]  # adds new head plus all other body parts

        for x, y in self.snake_body:
            pygame.draw.rect(win, snake_color, (x + 1, y + 1, 29, 29))

    def add_body(self):
        snake_pos_x, snake_pos_y = self.snake_body[0]
        new_head_pos = (snake_pos_x, snake_pos_y)

        if self.direction == "Right":
            new_head_pos = (snake_pos_x + MOVE_INCREMENT, snake_pos_y)
        if self.direction == "Left":
            new_head_pos = (snake_pos_x - MOVE_INCREMENT, snake_pos_y)
        if self.direction == "Up":
            new_head_pos = (snake_pos_x, snake_pos_y - MOVE_INCREMENT)
        if self.direction == "Down":
            new_head_pos = (snake_pos_x, snake_pos_y + MOVE_INCREMENT)

        self.snake_body += [new_head_pos]


def draw_game():
    win.fill(checker_board[0])
    game.draw_map()
    game.manage_fruit()
    snake.move()
    game.draw_boarder_and_score()
    pygame.display.update()
    pass


# Window setup
pygame.display.set_caption("Snake by NMan")

# Setup game elements
snake = Snake()
game = Game(1)
clock = pygame.time.Clock()

while flag:
    # slow loop & limit fps / speed of game
    pygame.time.delay(50)
    clock.tick(10)

    # key input & moving snake
    game.get_input()
    if not game.check_collisions():
        score = 0

    # draw snake, food, and window itself
    draw_game()
