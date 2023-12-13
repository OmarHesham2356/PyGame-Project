import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

BG= pygame.transform.scale(pygame.image.load("bg.jpg"),(WIDTH,HEIGHT))

def draw():
    WIN.blit(BG,(0,0))
    pygame.display.update()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Player
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - 2 * player_size
player_speed = 100

# Enemies
enemy_size = 200
enemy_speed = 100

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Functions

def draw_player(x, y):
    pygame.draw.rect(screen, WHITE, [x, y, player_size, player_size])

def draw_enemy(x, y):
    pygame.draw.rect(screen, RED, [x, y, enemy_size, enemy_size])

def display_score(score):
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, [10, 10])

def game_over():
    game_over_text = font.render("Game Over", True, WHITE)
    screen.blit(game_over_text, [WIDTH // 2 - 100, HEIGHT // 2 - 50])
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    quit()

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                return -player_speed
            elif event.key == pygame.K_RIGHT:
                return player_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                return 0
    return 0

def move_player(player_x_change):
    global player_x
    player_x += player_x_change

    if player_x < 0:
        player_x = 0
    elif player_x > WIDTH - player_size:
        player_x = WIDTH - player_size

def move_enemy():
    global enemy_x, enemy_y, score
    enemy_y += enemy_speed

    if enemy_y > HEIGHT:
        enemy_y = -enemy_size
        enemy_x = random.randrange(0, WIDTH - enemy_size)
        score += 1

def check_collision():
    if (
        player_x < enemy_x + enemy_size
        and player_x + player_size > enemy_x
        and player_y < enemy_y + enemy_size
        and player_y + player_size > enemy_y
    ):
        game_over()

def draw_objects():
    screen.fill((0, 0, 0))
    draw_player(player_x, player_y)
    draw_enemy(enemy_x, enemy_y)
    display_score(score)

def game_loop():
    global player_x, player_y, enemy_x, enemy_y, score

    player_x_change = 0
    enemy_x = random.randrange(0, WIDTH - enemy_size)
    enemy_y = -enemy_size
    score = 0

    while True:
        player_x_change = handle_events()
        move_player(player_x_change)
        move_enemy()
        check_collision()
        draw_objects()

        pygame.display.flip()
        clock.tick(60)

# Run the game loop
game_loop()
