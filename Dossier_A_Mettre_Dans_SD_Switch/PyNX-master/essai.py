import pygame
import sys
import random


class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))


class Player(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0
        self.health = 5

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constrain()


class Ball(Block):
    def __init__(self, path, x_pos, y_pos, speed_x, speed_y, paddles, player_health, opponent_health, time):
        super().__init__(path, x_pos, y_pos)
        self.speed_x = speed_x * random.choice((-1, 1))
        self.speed_y = speed_y * random.choice((-1, 1))
        self.paddles = paddles
        self.active = False
        self.score_time = 0
        self.player_health = 100
        self.opponent_health = 100
        self.time = 0
    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            time = 0
            self.restart_counter()

    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            pygame.mixer.Sound.play(plob_sound)
            self.speed_y *= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):
            pygame.mixer.Sound.play(plob_sound)
            collision_paddle = pygame.sprite.spritecollide(
                self, self.paddles, False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
                if is_Combo_Player:
                    self.opponent_health -= 30
                else:
                    self.opponent_health -= 4
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
                self.player_health -= 4
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_paddle.bottom
                self.speed_y *= -1
                self.player_health -= 4

            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.rect.bottom = collision_paddle.top
                self.speed_y *= -1
                self.player_health -= 4

    def reset_ball(self):
        self.active = False
        self.speed_x *= random.choice((-1, 1))
        self.speed_y *= random.choice((-1, 1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width/2, screen_height/2)
        pygame.mixer.Sound.play(score_sound)

    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 3

        if current_time - self.score_time <= 1400:
            countdown_number = "3, Press Bar For Combo"
            if self.time == 0:
                pygame.mixer.Sound.play(three_sound)
                self.time += 1


        if 1400 < current_time - self.score_time <= 2100:
            countdown_number = "2, The first to 11 Win the game"
            if self.time == 0:
                pygame.mixer.Sound.play(two_sound)
                self.time += 1


        if 2100 < current_time - self.score_time <= 2800:
            countdown_number = "1, or the last who stay alive !"
            if self.time == 0:
                pygame.mixer.Sound.play(one_sound)
                self.time = 1

        if current_time - self.score_time >= 2800:
            self.active = True
        
        time_counter = basic_font.render(
            str(countdown_number), True, accent_color)
        time_counter_rect = time_counter.get_rect(
            center=(screen_width/2, screen_height/2 + 50))
        pygame.draw.rect(screen, bg_color, time_counter_rect)
        screen.blit(time_counter, time_counter_rect)


class Opponent(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed

    def update(self, ball_group):
        if self.rect.top < ball_group.sprite.rect.y:
            self.rect.y += self.speed
        if self.rect.bottom > ball_group.sprite.rect.y:
            self.rect.y -= self.speed
        self.constrain()

    def constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height


class GameManager:
    def __init__(self, ball_group, paddle_group):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group

    def run_game(self):
        # Drawing the game objects
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        # Updating the game objects
        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.opponent_score += 1
            #self.player_health -= 5
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            #self.opponent_health -= 5
            self.ball_group.sprite.reset_ball()

    def draw_score(self):
        player_score = basic_font.render(
            str(self.player_score), True, accent_color)
        opponent_score = basic_font.render(
            str(self.opponent_score), True, accent_color)

        player_score_rect = player_score.get_rect(
            midleft=(screen_width / 2 + 40, screen_height/2))
        opponent_score_rect = opponent_score.get_rect(
            midright=(screen_width / 2 - 40, screen_height/2))

        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)


#setup général
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()


# Fenetre principale
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Variables GLobales
bg_color = pygame.Color('#2F373F')
bg_color_combo = pygame.Color('#13FDE2')
accent_color = (27, 35, 43)
basic_font = pygame.font.Font('freesansbold.ttf', 32)
plob_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")

three_sound = pygame.mixer.Sound("3.ogg")
two_sound = pygame.mixer.Sound("2.ogg")
one_sound = pygame.mixer.Sound("1.ogg")

#bande qui sépare le terrain en deux
middle_strip = pygame.Rect(screen_width/2 - 2, 0, 4, screen_height)

# objets du jeu
player = Player('Paddle.png', screen_width - 20, screen_height/2, 5)
opponent = Opponent('Paddle.png', 20, screen_width/2, 5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

# ball rouge du simple jeu

ball = Ball('Ball.png', screen_width/2, screen_height /
            2, 4, 4, paddle_group, 100, 100,0)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)



# if(not(is_Combo_Player)):
game_manager = GameManager(ball_sprite, paddle_group)
# else:
#game_manager = GameManager(ball_blue_sprite, paddle_group)

# import de l'image du logo

logo_surface = pygame.image.load('1.png').convert_alpha()

logo_surface = pygame.transform.scale(logo_surface, (250, 100))

# import des health bar des joueurs
# on a 7 états des healthbars


h0 = pygame.image.load("vide.png")

h0 = pygame.transform.scale(h0, (190, 30))


h1 = pygame.image.load("1 de 6.png")

h1 = pygame.transform.scale(h1, (190, 30))


h2 = pygame.image.load("2 de 6.png")

h2 = pygame.transform.scale(h2, (190, 30))


h3 = pygame.image.load("3 de 6.png")

h3 = pygame.transform.scale(h3, (190, 30))


h4 = pygame.image.load("4 de 6.png")

h4 = pygame.transform.scale(h4, (190, 30))


h5 = pygame.image.load("5 de 6.png")

h5 = pygame.transform.scale(h5, (190, 30))

h6 = pygame.image.load("full.png")

h6 = pygame.transform.scale(h6, (190, 30))


# combo health full energy bar import

combo_full = pygame.image.load("combofull.png")

combo_full = pygame.transform.scale(combo_full, (238, 120))

# combo health empty energy bar import

combo_empty = pygame.image.load("combovide.png")

combo_empty = pygame.transform.scale(combo_empty, (238, 160))

# import de l'igame de game_over

go = pygame.image.load("go.png")

go = pygame.transform.scale(go, (300, 200))

is_Combo_Player = False

frame = 120

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.movement -= player.speed
            if event.key == pygame.K_DOWN:
                player.movement += player.speed
            if event.key == pygame.K_SPACE:
                is_Combo_Player = True
                bg_color = bg_color_combo



                
            

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.movement += player.speed
            if event.key == pygame.K_DOWN:
                player.movement -= player.speed

    # Background Stuff
    screen.fill(bg_color)
    pygame.draw.rect(screen, accent_color, middle_strip)

    # insertion du logo
    screen.blit(logo_surface, (510, 780))

    # insertion des pv du joueur 1 full bar
    if 90 <= ball.player_health <= 100:
        screen.blit(h6, (210+screen_width/2, 50))
    elif 70 <= ball.player_health < 90:
        # insertion des pv du joueur 1 full bar
        screen.blit(h5, (210+screen_width/2, 50))
    elif 50 <= ball.player_health < 70:
        # insertion des pv du joueur 1 full bar
        screen.blit(h4, (210+screen_width/2, 50))
    elif 30 <= ball.player_health < 70:
        # insertion des pv du joueur 1 full bar
        screen.blit(h3, (210+screen_width/2, 50))
    elif 20 <= ball.player_health < 30:
        # insertion des pv du joueur 1 full bar
        screen.blit(h2, (210+screen_width/2, 50))
    elif 10 <= ball.player_health < 20:
        # insertion des pv du joueur 1 full bar
        screen.blit(h1, (210+screen_width/2, 50))
    elif 0 < ball.player_health < 10:
        # insertion des pv du joueur 1 full bar
        screen.blit(h0, (210+screen_width/2, 50))
        # ici game over du joueur 1
    elif ball.player_health <= 0 or game_manager.opponent_score >=11 :
        screen.blit(go, (210+screen_width/2, 500))
        pygame.quit()
        sys.exit()

    # insertion des pv du joueur adverse full bar
    if 90 <= ball.opponent_health <= 100:
        screen.blit(h6, (210, 50))
    elif 70 <= ball.opponent_health < 90:
        # insertion des pv du joueur 2 full bar
        screen.blit(h5, (210, 50))
    elif 50 <= ball.opponent_health < 70:
        # insertion des pv du joueur 2 full bar
        screen.blit(h4, (210, 50))
    elif 30 <= ball.opponent_health < 70:
        # insertion des pv du joueur 2 full bar
        screen.blit(h3, (210, 50))
    elif 20 <= ball.opponent_health < 30:
        # insertion des pv du joueur 2 full bar
        screen.blit(h2, (210, 50))
    elif 10 <= ball.opponent_health < 20:
        # insertion des pv du joueur 2 full bar
        screen.blit(h1, (210, 50))
    elif 0 < ball.opponent_health < 10:
        # insertion des pv du joueur 2 full bar
        screen.blit(h0, (210, 50))
        
        # ici game over d'un joueur adverse
    elif ball.opponent_health <= 0 or game_manager.player_score >= 9 :
        screen.blit(go, (210, 500))
        pygame.quit()
        sys.exit()

    # insertion de la pv du combo full du joueur player
    screen.blit(combo_full, (200, 65))
    screen.blit(combo_full, (200+screen_width/2, 65))
    if is_Combo_Player:
        screen.blit(combo_empty, (200+screen_width/2, 23))

    # else:
    # insertion de la pv du combo full du joueur opponent
    #    screen.blit(combo_empty, (200, 65))

    # insertion de la pv du combo full du joueur opponent
    # if(not(is_Combo_Player)):
    #    screen.blit(combo_full, (200+screen_width/2, 65))self.opponent_health -= 30
    # else:
    #    # insertion de la pv du combo vide du joueur opponent
    #    screen.blit(combo_empty, (200, 65))

    # démarrage du jeu
    game_manager.run_game()

    # Rendering
    pygame.display.flip()
    clock.tick(frame)
