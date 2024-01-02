import pygame
import time
import random
import sys
import time

pygame.font.init()

WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE DODGE")

BG = pygame.transform.scale(pygame.image.load("Bg.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH, PLAYER_HEIGHT = 60, 40
PLAYER_VEL = 5
DEFAULT_PLAYER_VEL = 5
POWERUP_DURATION = 5  # seconds

STAR_WIDTH, STAR_HEIGHT, STAR_VELOCITY = 50, 70, 3
POWERUP_WIDTH, POWERUP_HEIGHT, POWERUP_VELOCITY = 50, 50, 3

FONT = pygame.font.SysFont("oswald", 50)

def draw_stars(stars):
    star_image = pygame.transform.scale(pygame.image.load("R1.png").convert_alpha(), (STAR_WIDTH, STAR_HEIGHT))
    for star in stars:
        WIN.blit(star_image, star.topleft)

def draw_powerups(powerups):
    powerup_image = pygame.transform.scale(pygame.image.load("power_up.jpg").convert_alpha(), (POWERUP_WIDTH, POWERUP_HEIGHT))
    for powerup in powerups:
        WIN.blit(powerup_image, powerup.topleft)

def draw_player(player):
    player_image = pygame.transform.scale(pygame.image.load("Ship.png").convert_alpha(), (PLAYER_WIDTH, PLAYER_HEIGHT))
    WIN.blit(player_image, player.topleft)

def draw_background():
    WIN.blit(BG, (0, 0))


def draw_text(elapsed_time):
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    player_image = pygame.transform.scale(pygame.image.load("tiny_ship6.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
    WIN.blit(player_image, player.topleft)

    star_image = pygame.transform.scale(pygame.image.load("R1.png"), (STAR_WIDTH, STAR_HEIGHT))
    for star in stars:
        WIN.blit(star_image, star.topleft)

    pygame.display.update()

def show_score(elapsed_time):
    score_text = FONT.render(f"Your Time: {elapsed_time}s", 1, "white")
    score_text_pos = (380,290)
    WIN.blit(score_text, score_text_pos)
    pygame.display.update()

def get_elapsed_time(start_time):
    return round(time.time() - start_time)

def game_over_screen():
    game_over_text = FONT.render("Game Over", 1, "red")
    restart_text = FONT.render("Press R to restart", 1, "white")
    quit_text = FONT.render("Press Q to quit", 1, "white")

    game_over_text_pos = (380,325)
    restart_text_pos = (380,360)
    quit_text_pos = (380,390)

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
    global PLAYER_VEL
    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    start_time = start_menu()
    elapsed_time = 0
    powerup_timer = 0
    powerup_active = False

    star_add_increment = 2000
    star_count = 0
    powerup_count = 0

    stars = []
    powerups = []
    hit = False


    while run:
        dt = clock.tick(60) / 1000.0  # Convert to seconds
        star_count += dt
        powerup_count += dt
        elapsed_time = get_elapsed_time(start_time)

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_count = 0

        if powerup_count > powerup_add_increment:
            powerup_x = random.randint(0, WIDTH - POWERUP_WIDTH)
            powerup = pygame.Rect(powerup_x, -POWERUP_HEIGHT, POWERUP_WIDTH, POWERUP_HEIGHT)
            powerups.append(powerup)
            powerup_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x - PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars:
            star.y += STAR_VELOCITY
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        for powerup in powerups:
            powerup.y += POWERUP_VELOCITY
            if powerup.y > HEIGHT:
                powerups.remove(powerup)
            elif player.colliderect(powerup):
                powerups.remove(powerup)
                PLAYER_VEL += 2
                powerup_timer = time.time()
                powerup_active = True

        if powerup_active and time.time() - powerup_timer > POWERUP_DURATION:
            # Powerup duration has expired
            PLAYER_VEL = DEFAULT_PLAYER_VEL
            powerup_active = False

        if hit:
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
                powerups = []
                hit = False
                PLAYER_VEL = DEFAULT_PLAYER_VEL
                powerup_active = False
            else:
                break

        draw_game(player, elapsed_time, stars, powerups)

    pygame.quit()

if __name__ == "__main__":
    main()