import pygame, sys, random

def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, enemy_score, score_time

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1

    # Player Score
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()

    # Enemy Score
    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        enemy_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(enemy) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - enemy.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - enemy.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - enemy.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def enemy_ai():
    if enemy.top < ball.y:
        enemy.top += enemy_speed
    if enemy.bottom > ball.y:
        enemy.bottom -= enemy_speed
    if enemy.top <= 0:
        enemy.top = 0
    if enemy.bottom >= screen_height:
        enemy.bottom = screen_height

def ball_start():
    global ball_speed_x, ball_speed_y, score_time

    ball.center = (screen_width/2, screen_height/2)
    current_time = pygame.time.get_ticks()
    player.center = (screen_width - 10, screen_height/2)
    enemy.center = (10, screen_height/2)


    if current_time - score_time < 500:
        number_three = game_font.render("3",True,light_grey)
        screen.blit(number_three,(screen_width/2 - 10, screen_height/2 + 20))
    if 500 < current_time - score_time < 1000:
        number_two = game_font.render("2",True,light_grey)
        screen.blit(number_two,(screen_width/2 - 10, screen_height/2 + 20))
    if 1000 < current_time - score_time < 1500:
        number_one = game_font.render("1",True,light_grey)
        screen.blit(number_one,(screen_width/2 - 10, screen_height/2 + 20))

    if current_time - score_time < 1500:
        ball_speed_x, ball_speed_y = 0,0
    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        pygame.mixer.Sound.play(start_sound)
        score_time = None

# General Setup
# pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

# Game Rectangles
ball = pygame.Rect(screen_width/2 - 15,screen_height/2 - 15,30,30)
player = pygame.Rect(screen_width - 10,screen_height/2 - 70,10,140)
enemy = pygame.Rect(10, screen_height/2 - 70, 10, 140)

# Colors
bg_color = pygame.Color('grey12')
light_grey = (200,200,200)

# Game Variables
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
enemy_speed = 7

# Text Variables
player_score = 0
enemy_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)
score_time = True

# Sound
pong_sound = pygame.mixer.Sound("pong.wav")
score_sound = pygame.mixer.Sound("score.wav")
start_sound = pygame.mixer.Sound("start.wav")

while True:
    # Handling Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7
        
    # Game Logic
    ball_animation()
    player_animation()
    enemy_ai()


    # Visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen,light_grey,player)
    pygame.draw.rect(screen,light_grey,enemy)
    pygame.draw.ellipse(screen,light_grey,ball)
    pygame.draw.aaline(screen,light_grey,(screen_width/2,0),(screen_width/2,screen_height))

    if score_time:
        ball_start()


    player_text = game_font.render(f"{player_score}",True,light_grey)
    screen.blit(player_text,(660,470))

    enemy_text = game_font.render(f"{enemy_score}",True,light_grey)
    screen.blit(enemy_text,(600,470))

    # Updating the window
    pygame.display.flip()
    clock.tick(60)
