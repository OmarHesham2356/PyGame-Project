import pygame
import time
import random
import sys

pygame.font.init()

WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE DODGE")

BG = pygame.transform.scale(pygame.image.load("Bg.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 60
PLAYER_HEIGHT = 40
PLAYER_VEL = 5

STAR_WIDTH = 50
STAR_HEIGHT = 70
STAR_VELOCITY = 3

FONT = pygame.font.SysFont("oswald", 50)

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    player_image = pygame.transform.scale(pygame.image.load("tiny_ship6.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
    WIN.blit(player_image, player.topleft)

    star_image = pygame.transform.scale(pygame.image.load("R1.png"), (STAR_WIDTH, STAR_HEIGHT))
    for star in stars:
        WIN.blit(star_image, star.topleft)

    pygame.display.update()

def get_elapsed_time(start_time):
    return round(time.time() - start_time)

def game_over_screen():
    game_over_text = FONT.render("Game Over", 1, "red")
    restart_text = FONT.render("Press R to restart", 1, "white")
    quit_text = FONT.render("Press Q to quit", 1, "white")

    game_over_text_pos = (400, 350)
    restart_text_pos = (WIDTH / 2 - restart_text.get_width() / 2, game_over_text_pos[1] + game_over_text.get_height())
    quit_text_pos = (WIDTH / 2 - quit_text.get_width() / 2, restart_text_pos[1] + restart_text.get_height())

    WIN.blit(game_over_text, game_over_text_pos)
    WIN.blit(restart_text, restart_text_pos)
    WIN.blit(quit_text, quit_text_pos)

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x - PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VELOCITY
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            elapsed_time = get_elapsed_time(start_time)
            lost_text = FONT.render(f"You Lost :( Time: {elapsed_time}s", 1, "red")
            lost_text_pos = (320, 300)
            WIN.blit(lost_text, lost_text_pos)
            pygame.display.update()
            pygame.time.delay(2000)

            if game_over_screen():
                player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
                start_time = time.time()
                elapsed_time = 0
                stars = []
                hit = False
            else:
                break

        draw(player, elapsed_time, stars)

    pygame.quit()

if __name__ == "__main__":
    main()
