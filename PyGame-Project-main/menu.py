import pygame

pygame.init()

# create game window
WIDTH, HEIGHT = 1000, 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#BG
BG = pygame.transform.scale(pygame.image.load("BG.jpg"), (WIDTH, HEIGHT))

#title 
FONT1 = pygame.font.Font("Fonts.ttf", 100)

# define variables
game_paused = True
menu_state = "main menu"

# load button images
start_img = pygame.image.load("start.jpg").convert_alpha()
options_img = pygame.image.load("button_options.png").convert_alpha()
quit_img = pygame.image.load("button_quit.png").convert_alpha()
video_img = pygame.image.load("button_video.png").convert_alpha()
audio_img = pygame.image.load("button_audio.png").convert_alpha()
keys_img = pygame.image.load("button_keys.png").convert_alpha()
back_img = pygame.image.load("button_back.png").convert_alpha()

# button class
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.click = False

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        start_text = FONT1.render("SPACE DODGE", 1, "purple") 
        WIN.blit(start_text, (120, 55))


        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.click:
                self.click = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.click = False  

        # draw button on the screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

# create button instances
start_button = Button(395, 250, start_img, 0.07)
options_button = Button(392, 400, options_img, 1)
quit_button = Button(432 , 550, quit_img, 1)
audio_button = Button(325, 250, audio_img, 1)
keys_button = Button(350 , 350, keys_img, 1)
back_button = Button(432 , 450, back_img, 1)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# main menu loop
while game_paused:
    screen.fill((52, 78, 91))
    screen.blit(BG, (0, 0)) 

    # check the menu state
    if menu_state == "main menu":
        # draw main menu buttons
        if start_button.draw(screen):
            game_paused = False
        if options_button.draw(screen):
            menu_state = "options"
        if quit_button.draw(screen):
            pygame.quit()

    # check if the options menu is opened
    if menu_state == "options":
        # draw the different options buttons
        if audio_button.draw(screen):
            print("audio settings")
        if keys_button.draw(screen):
            print("keys settings") 
        if back_button.draw(screen):
            menu_state = "main menu"

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_paused = False

pygame.quit()
