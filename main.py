import pygame
import os


class NewGame:
    WIDTH = 500
    HEIGHT = 500
    WINDOW_COLOR = (97, 97, 97)
    WINDOW_COLOR2 = (255, 255, 255)
    BLACK_COLOR = (0, 0, 0)
    FPS = 60
    MOVEMENT_VELOCITY = 5
    BULLET_VELOCITY = 10
    PIECE_WIDTH = 20
    PIECE_HEIGHT = 20
    YELLOW_PIECE_IMAGE = pygame.image.load(os.path.join('assets', 'yellow.png'))
    PURPLE_PIECE_IMAGE = pygame.image.load(os.path.join('assets', 'purple.png'))
    PLAYER_1_KEYS = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]    # left, right, up, down
    PLAYER_2_KEYS = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
    BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)
    MAX_BULLETS = 3

    def __init__(self, game_options):
        self.options = game_options
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Nine Mens Morris Game v2")

        # transform images before display
        self.yellow_piece = pygame.transform.rotate(
            pygame.transform.scale(self.YELLOW_PIECE_IMAGE, (self.PIECE_WIDTH, self.PIECE_HEIGHT)),
            45)
        self.purple_piece = pygame.transform.rotate(
            pygame.transform.scale(self.PURPLE_PIECE_IMAGE, (self.PIECE_WIDTH, self.PIECE_HEIGHT)),
            -45)

        # rectangles for pieces in order to use the rectangles for movement later
        self.yellow = pygame.Rect(100, 200, self.PIECE_WIDTH, self.PIECE_HEIGHT)  # x, y, width, height
        self.purple = pygame.Rect(300, 200, self.PIECE_WIDTH, self.PIECE_HEIGHT)  # x, y, width, height

        # projectiles
        self.yellow_bullets = []
        self.purple_bullets = []

    @staticmethod
    def update_after_any_change():
        pygame.display.update()

    def draw_window(self, yellow, purple):
        self.window.fill(self.WINDOW_COLOR)  # RGB
        pygame.draw.rect(self.window, self.BLACK_COLOR, self.BORDER)  # draw the border

        self.window.blit(self.yellow_piece, (yellow.x, yellow.y))  # always draw after filling the screen
        self.window.blit(self.purple_piece, (purple.x, purple.y))

        self.update_after_any_change()       # update after a change

    # ToDo: optimize
    def movement(self, key_pressed):

        # yellow
        if key_pressed[self.PLAYER_1_KEYS[0]] \
                and self.yellow.x - self.MOVEMENT_VELOCITY > 0:
            self.yellow.x -= self.MOVEMENT_VELOCITY  # movement @ 60 fps
        if key_pressed[self.PLAYER_1_KEYS[1]] \
                and self.yellow.x + self.MOVEMENT_VELOCITY + self.yellow.width < self.BORDER.x - 5:
            self.yellow.x += self.MOVEMENT_VELOCITY
        if key_pressed[self.PLAYER_1_KEYS[2]] \
                and self.yellow.y - self.MOVEMENT_VELOCITY > 0:
            self.yellow.y -= self.MOVEMENT_VELOCITY
        if key_pressed[self.PLAYER_1_KEYS[3]] \
                and self.yellow.y + self.MOVEMENT_VELOCITY + self.yellow.height < self.HEIGHT - 5:
            self.yellow.y += self.MOVEMENT_VELOCITY

        # purple
        if key_pressed[self.PLAYER_2_KEYS[0]] \
                and self.purple.x - self.MOVEMENT_VELOCITY > self.BORDER.x + self.BORDER.width - 2:
            self.purple.x -= self.MOVEMENT_VELOCITY
        if key_pressed[self.PLAYER_2_KEYS[1]] \
                and self.purple.x + self.MOVEMENT_VELOCITY + self.purple.width < self.WIDTH - 7:
            self.purple.x += self.MOVEMENT_VELOCITY
        if key_pressed[self.PLAYER_2_KEYS[2]] \
                and self.purple.y - self.MOVEMENT_VELOCITY > 0:
            self.purple.y -= self.MOVEMENT_VELOCITY
        if key_pressed[self.PLAYER_2_KEYS[3]] \
                and self.purple.y + self.MOVEMENT_VELOCITY + self.purple.height < self.HEIGHT - 5:
            self.purple.y += self.MOVEMENT_VELOCITY

    # main loop
    def run_game(self):

        run = True
        while run:
            self.clock.tick(self.FPS)

            # exit condition
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # ToDo: optimize
            # check for fire
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL and len(self.yellow_bullets) < self.MAX_BULLETS:
                        current_bullet = pygame.Rect(
                            self.yellow.x + self.yellow.width,
                            self.yellow.y + self.yellow.height/2 - 2,
                            10,
                            5
                        )
                        self.yellow_bullets.append(current_bullet)
                    if event.key == pygame.K_RCTRL and len(self.purple_bullets) < self.MAX_BULLETS:
                        current_bullet = pygame.Rect(
                            self.purple.x,
                            self.purple.y + self.purple.height / 2 - 2,
                            10,
                            5
                        )
                        self.purple_bullets.append(current_bullet)
            print(f"yellow bullets: {len(self.yellow_bullets)}, "
                  f"purple bullets: {len(self.purple_bullets)}")

            # movement
            key_pressed = pygame.key.get_pressed()     # get pressed keys
            self.movement(key_pressed)                 # pass to movement method
            self.draw_window(self.yellow, self.purple)  # update window and pieces' position

        pygame.quit()


options = {}
new_game = NewGame(options)
new_game.run_game()
