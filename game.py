import pygame
import pygame.mask
import random
import sys
import time

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE DODGE")

BG = pygame.transform.scale(pygame.image.load("BG.jpg"), (WIDTH, HEIGHT))
BLACK = (0, 0, 0)

sound2_sfx = pygame.mixer.Sound("Kandil.wav")
sound2_sfx.set_volume(0.5)

sound_sfx = pygame.mixer.Sound("3.wav")
sound_sfx.set_volume(0.5)

PLAYER_WIDTH, PLAYER_HEIGHT = 60, 40
PLAYER_VEL = 5
DEFAULT_PLAYER_VEL = 5
POWERUP_DURATION = 5  

STAR_WIDTH, STAR_HEIGHT, STAR_VELOCITY = 50, 70, 3
POWERUP_WIDTH, POWERUP_HEIGHT, POWERUP_VELOCITY = 50, 50, 3

FONT = pygame.font.SysFont("oswald", 50)
#This Variabule is for ship photo
ship_images = [
    pygame.image.load("Ship.png").convert_alpha(),
    pygame.image.load("Ship2.png").convert_alpha(),
    pygame.image.load("Ship3.png").convert_alpha(),
    pygame.image.load("Ship4.png").convert_alpha(),
]

def draw_stars(stars):
    star_image = pygame.transform.scale(pygame.image.load("Star.png").convert_alpha(), (STAR_WIDTH, STAR_HEIGHT))
    for star in stars:
        WIN.blit(star_image, star.topleft)

#This Function is for the powerup which it will make them draw on the screen
def draw_powerups(powerups):
    powerup_image = pygame.transform.scale(pygame.image.load("power_up.png").convert_alpha(), (POWERUP_WIDTH, POWERUP_HEIGHT))
    for powerup in powerups:
        WIN.blit(powerup_image, powerup.topleft)

def draw_player(player, player_image):
    WIN.blit(player_image, player.topleft)

def draw_background():
    WIN.blit(BG, (0, 0))

def draw_text(elapsed_time):
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

def draw_game(player, elapsed_time, stars, powerups, player_image):
    draw_background()
    draw_text(elapsed_time)
    draw_player(player, player_image)
    draw_stars(stars)
    draw_powerups(powerups)
    pygame.display.update()

def get_elapsed_time(start_time, paused_time):
    current_time = time.time()
    if paused_time:
        return round(paused_time - start_time)
    return round(current_time - start_time)

#This Function is for player mask to fix the collision
def create_player_mask(player):
    player_image = pygame.transform.scale(ship_images[0], (PLAYER_WIDTH, PLAYER_HEIGHT))
    return pygame.mask.from_surface(player_image)

#This Function is for star mask to fix collision
def create_star_masks(stars):
    star_masks = []
    star_image = pygame.transform.scale(pygame.image.load("Star.png").convert_alpha(), (STAR_WIDTH, STAR_HEIGHT))
    for star in stars:
        mask = pygame.mask.from_surface(star_image)
        star_masks.append(mask)
    return star_masks

#This Functions Checks for collisions between the player and stars
def check_star_collision(player, stars, star_masks):
    player_mask = create_player_mask(player)
    for i, star in enumerate(stars):
        star_mask = star_masks[i]
        offset = (int(star.x - player.x), int(star.y - player.y))
        if player_mask.overlap(star_mask, offset):
            return True
    return False

def game_over_screen():
    game_over_text = FONT.render("Game Over", 1, "red")
    restart_text = FONT.render("Press R to restart", 1, "white")
    quit_text = FONT.render("Press Q to quit", 1, "white")

    game_over_text_pos = (400, 350)
    restart_text_pos = (WIDTH // 2 - restart_text.get_width() // 2, game_over_text_pos[1] + game_over_text.get_height())
    quit_text_pos = (WIDTH // 2 - quit_text.get_width() // 2, restart_text_pos[1] + restart_text.get_height())

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

def pause_menu():
    pause_text = FONT.render("Paused", 1, "white")
    resume_text = FONT.render("Press P to resume", 1, "white")

    pause_text_pos = (WIDTH // 2 - pause_text.get_width() // 2, 250)
    resume_text_pos = (WIDTH // 2 - resume_text.get_width() // 2, pause_text_pos[1] + pause_text.get_height() + 70)

    WIN.blit(pause_text, pause_text_pos)
    WIN.blit(resume_text, resume_text_pos)
    pygame.display.update()

def start_menu():
    menu_font = pygame.font.Font("Fonts.ttf", 100)
    menu_font2 = pygame.font.Font("2.ttf", 60)
    menu_title = menu_font.render("SPACE DODGE", 1, "purple")
    menu_subtitle = menu_font2.render("Press Enter to start", 1, "white")
    menu_subtitle2 = menu_font2.render("Press Escape to quit", 1, "white")

    title_pos = (WIDTH // 2 - menu_title.get_width() // 2, 100)
    subtitle_pos = (WIDTH // 2 - menu_subtitle.get_width() // 2, title_pos[1] + menu_title.get_height() + 70)
    subtitle_pos2 = (WIDTH // 2 - menu_subtitle2.get_width() // 2, title_pos[1] + menu_subtitle.get_height() + 220)

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
                if event.key == pygame.K_RETURN:
                    fade_counter2 = 0
                    while fade_counter2 < WIDTH:
                        fade_counter2 += 10
                        pygame.draw.rect(WIN, BLACK, (0, 0, fade_counter2, HEIGHT))
                        pygame.display.update()
                        pygame.time.delay(7)
                    start_time = time.time()
                    return start_time
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

#This functions for powerups which  it will make them spawn randomly
def spawn_powerup(powerups):
    powerup_x = random.randint(0, WIDTH - POWERUP_WIDTH)
    powerup = pygame.Rect(powerup_x, -POWERUP_HEIGHT, POWERUP_WIDTH, POWERUP_HEIGHT)
    powerups.append(powerup)

#This function for player movement
def handle_input(player):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
        player.x -= PLAYER_VEL
    if keys[pygame.K_RIGHT] and player.x - PLAYER_VEL + player.width <= WIDTH:
        player.x += PLAYER_VEL
    if keys[pygame.K_UP] and player.y - PLAYER_VEL >= 0:
        player.y -= PLAYER_VEL
    if keys[pygame.K_DOWN] and player.y + PLAYER_VEL + player.height <= HEIGHT:
        player.y += PLAYER_VEL

def customization_menu():
    menu_font = pygame.font.Font("2.ttf", 60)
    menu_font1 = pygame.font.Font("Fonts.ttf", 60)
    menu_title = menu_font1.render("Choose Your Ship", 1, "purple")
    ship_option1 = menu_font.render("Press 1 for Ship 1", 1, "white")
    ship_option2 = menu_font.render("Press 2 for Ship 2", 1, "white")
    ship_option3 = menu_font.render("Press 3 for Ship 3", 1, "white")
    ship_option4 = menu_font.render("Press 4 for Ship 4", 1, "white")
   

    title_pos = (WIDTH // 2 - menu_title.get_width() // 2, 100)
    option1_pos = (WIDTH // 2 - ship_option1.get_width() // 2, title_pos[1] + menu_title.get_height() + 50)
    option2_pos = (WIDTH // 2 - ship_option2.get_width() // 2, option1_pos[1] + ship_option1.get_height() + 20)
    option3_pos = (WIDTH // 2 - ship_option3.get_width() // 2, option2_pos[1] + ship_option2.get_height() + 20)
    option4_pos = (WIDTH // 2 - ship_option4.get_width() // 2, option3_pos[1] + ship_option3.get_height() + 20)
    
    

    WIN.blit(BG, (0, 0))
    WIN.blit(menu_title, title_pos)
    WIN.blit(ship_option1, option1_pos)
    WIN.blit(ship_option2, option2_pos)
    WIN.blit(ship_option3, option3_pos)
    WIN.blit(ship_option4, option4_pos)

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 0  
                elif event.key == pygame.K_2:
                    return 1
                elif event.key == pygame.K_3:
                    return 2
                elif event.key == pygame.K_4:
                    return 3  
                

def main():
    global PLAYER_VEL, STAR_VELOCITY
    run = True
    player_image_index = customization_menu()
    player_image = ship_images[player_image_index]

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    sound_sfx.play()
    clock = pygame.time.Clock()
    start_time = start_menu()
    elapsed_time = 0
    powerup_timer = 0
    powerup_active = False
    last_difficulty_increase = 0
    paused_time = None  

    powerup_add_increment = 5
    star_count = 0
    powerup_count = 0

    stars = []
    powerups = []
    hit = False
    paused = False

    while run:
        dt = clock.tick(60) / 1000.0  
        star_count += dt
        powerup_count += dt
        elapsed_time = get_elapsed_time(start_time, paused_time)

        
        if elapsed_time - last_difficulty_increase >= 20:
            STAR_VELOCITY += 1
            last_difficulty_increase = elapsed_time

        if star_count > 1:
            for _ in range(2):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_count = 0

        if powerup_count > powerup_add_increment:
            spawn_powerup(powerups)
            powerup_count = 0

        star_masks = create_star_masks(stars)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        
                        paused_start_time = time.time()
                    else:
                        
                        paused_duration = time.time() - paused_start_time
                        start_time += paused_duration
                        paused_time = None

        if not paused:
            handle_input(player)

            for i, star in enumerate(stars):
                star.y += STAR_VELOCITY
                if star.y > HEIGHT:
                    stars.remove(star)
                elif check_star_collision(player, [star], [star_masks[i]]):
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
                
                PLAYER_VEL = DEFAULT_PLAYER_VEL
                powerup_active = False

            if hit:
                sound2_sfx.play()
                sound_sfx.stop()

                fade_counter = 0
                while fade_counter < WIDTH:
                    fade_counter += 10
                    pygame.draw.rect(WIN, BLACK, (0, 0, fade_counter, HEIGHT))
                    pygame.display.update()
                    pygame.time.delay(7)

                elapsed_time = get_elapsed_time(start_time, paused_time)
                lost_text = FONT.render(f"You Lost :( Your Score: {elapsed_time}s", 1, "red")
                lost_text_pos = (320, 300)
                WIN.blit(lost_text, lost_text_pos)

                pygame.display.update()
                pygame.time.delay(2000)

                if game_over_screen():
                    sound_sfx.play()
                    player_image_index = customization_menu()
                    player_image = ship_images[player_image_index]
                    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
                    start_time = time.time()
                    elapsed_time = 0
                    stars = []
                    powerups = []
                    hit = False
                    PLAYER_VEL = DEFAULT_PLAYER_VEL
                    powerup_active = False
                    last_difficulty_increase = elapsed_time
                    paused_time = None  
                else:
                    break

            draw_game(player, elapsed_time, stars, powerups, player_image)
        else:
            pause_menu()

    pygame.quit()


if __name__ == "__main__":
    main()
