import pygame
import os
pygame.font.init()   # enable the fonts
pygame.mixer.init()  # enable sounds


class NewGame:
    WIDTH = 500
    HEIGHT = 500
    WINDOW_COLOR = (97, 97, 97)
    WINDOW_COLOR2 = (255, 255, 255)
    BLACK_COLOR = (0, 0, 0)
    RED_COLOR = (255, 0, 0)
    GREEN_COLOR = (0, 255, 0)
    HEALTH_FONT = pygame.font.SysFont('comicsans', 30)
    WINNER_FONT = pygame.font.SysFont('comicsans', 60)
    BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'gun_sound.mp3'))
    BULLET_FIRE_SOUND.set_volume(0.2)   # lower volume
    BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'hit_sound.mp3'))
    FPS = 60
    MOVEMENT_VELOCITY = 5
    BULLET_VELOCITY = 8
    PIECE_WIDTH = 20
    PIECE_HEIGHT = 20
    YELLOW_PIECE_IMAGE = pygame.image.load(os.path.join('assets', 'yellow.png'))
    PURPLE_PIECE_IMAGE = pygame.image.load(os.path.join('assets', 'purple.png'))
    BACKGROUND = pygame.image.load(os.path.join('assets', 'space.png'))
    PLAYER_1_KEYS = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]    # left, right, up, down
    PLAYER_2_KEYS = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
    BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)   # only int
    MAX_BULLETS = 3

    def __init__(self, game_options):

        self.options = game_options
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Spaceships")

        # transform images before display
        self.yellow_piece = pygame.transform.rotate(
            pygame.transform.scale(self.YELLOW_PIECE_IMAGE, (self.PIECE_WIDTH, self.PIECE_HEIGHT)),
            45)
        self.purple_piece = pygame.transform.rotate(
            pygame.transform.scale(self.PURPLE_PIECE_IMAGE, (self.PIECE_WIDTH, self.PIECE_HEIGHT)),
            -45)
        self.background = pygame.transform.scale(self.BACKGROUND, (self.WIDTH, self.HEIGHT))

        # rectangles for pieces in order to use the rectangles for movement later
        self.yellow = pygame.Rect(100, 200, self.PIECE_WIDTH, self.PIECE_HEIGHT)  # x, y, width, height
        self.purple = pygame.Rect(300, 200, self.PIECE_WIDTH, self.PIECE_HEIGHT)  # x, y, width, height

        # projectiles
        self.yellow_bullets = []
        self.purple_bullets = []

        # events when hit
        self.yellow_is_hit = pygame.USEREVENT + 1   # event to check for during the main loop
        self.purple_is_hit = pygame.USEREVENT + 2

        # health
        self.yellow_health = 10
        self.purple_health = 10

    @staticmethod
    def update_after_any_change():
        pygame.display.update()

    def draw_window(
            self,
            yellow,
            purple,
            yellow_bullets,
            purple_bullets,
            yellow_health,
            purple_health
            ):
        # self.window.fill(self.WINDOW_COLOR)  # RGB
        self.window.blit(self.background, (0, 0))
        pygame.draw.rect(self.window, self.BLACK_COLOR, self.BORDER)  # draw the border

        yellow_health_text = self.HEALTH_FONT.render(
            'Tati Health: ' + str(yellow_health), True, self.RED_COLOR)  # render font
        purple_health_text = self.HEALTH_FONT.render(
            'Maxi Health: ' + str(purple_health), True, self.GREEN_COLOR)  # render font
        self.window.blit(purple_health_text, (self.WIDTH - yellow_health_text.get_width()-30, 10))
        self.window.blit(yellow_health_text, (10, 10))

        self.window.blit(self.yellow_piece, (yellow.x, yellow.y))  # always draw after filling the screen
        self.window.blit(self.purple_piece, (purple.x, purple.y))

        for bullet in yellow_bullets:
            pygame.draw.rect(self.window, self.RED_COLOR, bullet)

        for bullet in purple_bullets:
            pygame.draw.rect(self.window, self.GREEN_COLOR, bullet)

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

    # ToDo: optimize
    def handle_bullets(self, yellow_bullets, purple_bullets, yellow, purple):

        for bullet in yellow_bullets:
            bullet.x += self.BULLET_VELOCITY
            if self.purple.colliderect(bullet):  # check for collision if both objects are rectangles
                pygame.event.post(pygame.event.Event(self.purple_is_hit))
                self.yellow_bullets.remove(bullet)
            elif bullet.x > self.WIDTH:
                self.yellow_bullets.remove(bullet)

        for bullet in purple_bullets:
            bullet.x -= self.BULLET_VELOCITY
            if self.yellow.colliderect(bullet):  # check for collision if both objects are rectangles
                pygame.event.post(pygame.event.Event(self.yellow_is_hit))
                self.purple_bullets.remove(bullet)
            elif bullet.x < 0:
                self.purple_bullets.remove(bullet)

    def draw_winner(self, text):
        draw_text = self.WINNER_FONT.render(text, True, self.WINDOW_COLOR2)
        self.window.blit(draw_text,
                         (self.WIDTH//2 - draw_text.get_width()//2,
                          self.HEIGHT//2 - draw_text.get_height()//2))
        self.update_after_any_change()  # update after a change
        pygame.time.delay(3000)

    # main loop
    def run_game(self):

        run = True
        while run:
            self.clock.tick(self.FPS)

            # exit condition
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()   # when we press the x it will actually close the game

            # ToDo: optimize
            # check for fire
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL and len(self.yellow_bullets) < self.MAX_BULLETS:
                        current_bullet = pygame.Rect(
                            self.yellow.x + self.yellow.width,
                            self.yellow.y + self.yellow.height//2 - 2,
                            10,
                            5
                        )           # cannot have float, only int inside
                        self.yellow_bullets.append(current_bullet)
                        self.BULLET_FIRE_SOUND.play()

                    if event.key == pygame.K_RCTRL and len(self.purple_bullets) < self.MAX_BULLETS:
                        current_bullet = pygame.Rect(
                            self.purple.x,
                            self.purple.y + self.purple.height//2 - 2,
                            10,
                            5
                        )
                        self.purple_bullets.append(current_bullet)
                        self.BULLET_FIRE_SOUND.play()

            # do something after getting hit
                if event.type == self.yellow_is_hit:
                    self.yellow_health -= 1
                    self.BULLET_HIT_SOUND.play()
                if event.type == self.purple_is_hit:
                    self.purple_health -= 1
                    self.BULLET_HIT_SOUND.play()

            winner_text = ''
            if self.purple_health <= 0:
                winner_text = "Tati is Pro!"
            if self.yellow_health <= 0:
                winner_text = "Maxi is Pro!"
            if winner_text != '':
                self.draw_winner(winner_text)
                break

            # movement
            key_pressed = pygame.key.get_pressed()     # get pressed keys
            self.movement(key_pressed)                 # pass to movement method

            self.handle_bullets(self.yellow_bullets, self.purple_bullets, self.yellow, self.purple)

            self.draw_window(
                self.yellow,
                self.purple,
                self.yellow_bullets,
                self.purple_bullets,
                self.yellow_health,
                self.purple_health
            )  # update window and pieces' position

        # instead of quitting the game it is restarting by re-initiating!
        # pygame.quit()
        game = NewGame(options)
        game.run_game()


options = {}
new_game = NewGame(options)
new_game.run_game()
