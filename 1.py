import pygame
from pygame import mixer
import time
import random
import sys

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.font.init()

WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE DODGE")

BG = pygame.transform.scale(pygame.image.load("Bg.jpg"), (WIDTH, HEIGHT))
transition_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
BLACK = (0, 0, 0)

sound2_sfx = pygame.mixer.Sound("3.wav")
sound2_sfx.set_volume(0.5)

sound_sfx = pygame.mixer.Sound("2.wav")
sound_sfx.set_volume(0.5)
FONT1 = pygame.font.Font("1.ttf", 100)

PLAYER_WIDTH = 60
PLAYER_HEIGHT = 40
PLAYER_VEL = 5

STAR_WIDTH = 50
STAR_HEIGHT = 70
STAR_VELOCITY = 3

FONT = pygame.font.SysFont("oswald", 50)

def draw(player, elapsed_time, stars, transition_alpha):
    WIN.blit(BG, (0, 0))

    transition_surface.fill((0, 0, 0, transition_alpha))
    WIN.blit(transition_surface, (0, 0))



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

def start_menu():
    menu_font = pygame.font.Font("1.ttf", 100)
    menu_font2 = pygame.font.Font("2.ttf", 60)
    menu_title = menu_font.render("SPACE DODGE", 1, "purple")
    menu_subtitle = menu_font2.render("Press Enter to start", 1, "white")
    menu_subtitle2 = menu_font2.render("Press Escape to quit", 1, "white")

    title_pos = (WIDTH / 2 - menu_title.get_width() / 2, 100)
    subtitle_pos = (WIDTH / 2 - menu_subtitle.get_width() / 2, title_pos[1] + menu_title.get_height() + 70)
    subtitle_pos2 = (WIDTH / 2 - menu_subtitle2.get_width() / 2, title_pos[1] + menu_subtitle.get_height() + 220)

    WIN.blit(BG, (0, 0))
    WIN.blit(menu_title, title_pos)
    WIN.blit(menu_subtitle, subtitle_pos)
    WIN.blit(menu_subtitle2, subtitle_pos2)

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    run = True
    transition_alpha = 260
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    sound2_sfx.play()
    
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 3000
    star_count = 0

    stars = []
    hit = False

    start_menu()

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

        if transition_alpha > 0 and run:
            transition_alpha -= 10 
            clock.tick(45)

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
            sound2_sfx.stop()
            sound_sfx.play()

            fade_counter = 0
            while fade_counter < WIDTH:
                fade_counter = fade_counter + 10
                pygame.draw.rect(WIN, BLACK, (0, 0, fade_counter, HEIGHT))
                pygame.display.update()
                pygame.time.delay(7)

            elapsed_time = get_elapsed_time(start_time)
            lost_text = FONT.render(f"You Lost :( Your Score: {elapsed_time}s", 1, "red")
            lost_text_pos = (320, 300)
            WIN.blit(lost_text, lost_text_pos)

            pygame.display.update()
            pygame.time.delay(2000)

            if game_over_screen():
                player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
                sound2_sfx.play()
                start_time = time.time()
                elapsed_time = 0
                stars = []
                hit = False
            else:
                break

        draw(player, elapsed_time, stars, transition_alpha)

    pygame.quit()

if __name__ == "__main__":
    main()
