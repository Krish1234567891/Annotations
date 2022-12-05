#Libraries 
import pygame
import random
import os # so i could have a high score 
from spritesheet import SpriteSheet # imported from self made seprate module.
from enemy import Enemy

#initialize pygame 
pygame.init()

#game window dimensions 
hight = 600
width = 400

# create game window 
screen = pygame.display.set_mode((width, hight))
pygame.display.set_caption("Ninja_platformer")

#frame rate
clock = pygame.time.Clock()
FPS = 60

#game varibles 
GRAVITY = 1
MAX_PLAT = 10
SCROLL_THRESH = 200
scroll = 0 
bg_scroll = 0
score = 0 # Score variable
game_over = False  #Game Over variable 
fade_counter = 0 # Fade variable

if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        High_score = int(file.read())
else:
    High_score = 0

#color
white = (255, 255, 255)
black = (0, 0, 0)
P_col = (169, 169, 169) # Shows contrast of the panel to see the score better.
font_s = pygame.font.SysFont('Lucida Sans', 20)
font_b = pygame.font.SysFont('Lucida Sans', 25)

#load image 
player_img = pygame.image.load('player.png').convert_alpha()
b_img = pygame.image.load('ninjanight.png').convert_alpha()
b_img_1 = pygame.transform.scale(b_img, (400, 600))
platform_img = pygame.image.load('platform_2.png').convert_alpha()
bird_img = pygame.image.load('eagle.png').convert_alpha()
bird_sheet = SpriteSheet(bird_img)

#function for text output 
def draw_text(text, font, Txt_color, x, y):
    img = font.render(text, True, Txt_color)
    screen.blit(img, (x, y))

#game score display
# Draws the score on the top left of the game window and continuously increases as the player climbs up the platforms.
def draw_panel():
    pygame.draw.rect(screen, P_col, (0, 0, width, 30))
    pygame.draw.line(screen, white, (0, 30), (width, 30), 3)
    draw_text('SCORE: '+ str(score), font_s, white, 0, 0)

    
#function for drawing the background 
def draw_bg(bg_scroll):
    screen.blit(b_img_1, (0, 0 + bg_scroll))
    screen.blit(b_img_1, (0, -600 + bg_scroll))

#player class
class Player():
    def __init__(self, x, y):
        self.img = pygame.transform.scale(player_img,(45, 45))
        self.W = 35
        self.H = 45
        self.rect = pygame.Rect(0, 0, self.W, self.H)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def move (self):
        #reset varibles  
        dx = 0 # change in x
        dy = 0 # change in y
        scroll = 0
        #keyboard input and player speed
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -10
            self.flip = True
        if key[pygame.K_d]:
            dx = 10
            self.flip = False

        #gravity 
        self.vel_y += GRAVITY
        dy += self.vel_y

        #so player don't go off bounds 
        if self.rect.left + dx < 0:
            dx = 0 -self.rect.left
        if self.rect.right + dx > width:
            dx = width - self.rect.right 

        #collition with plalatforms 
        for platform in plat_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.W, self.H):
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20
        

        if self.rect.top <= SCROLL_THRESH:
            if self.vel_y < 0:
                scroll = -dy

        # update rect position 
        self.rect.x += dx
        self.rect.y += dy + scroll
        
        return scroll

    def draw(self):
        screen.blit(pygame.transform.flip(self.img, self.flip, False), (self.rect.x - 12, self.rect.y-5 ))
        pygame.draw.rect(screen, white, self.rect, 2)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_img, (width, 10))
        self.moving = moving
        self.move_counter = random.randint(0, 50) # Moves the Platform.
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(1, 2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        #move moving platforms side to side 
        if self.moving == True:
            self.move_counter += 1 # Moves 1 pixel from the left or to the right
            self.rect.x += self.direction * self.speed 
        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > width:
            self.direction *= -1  #self.direction is flipped, so we multiply it by -1; so if it is a positive value it will be negative, and if it was a negative value it will be positive. Resets the direction opposite.
            self.move_counter = 0

        self.rect.y += scroll

        if self.rect.top > hight:
            self.kill()
  

#player instence 
char = Player(width//2, hight - 150)

#create sprite groups 
plat_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

#starting platform
platform = Platform(width // 2 - 50, hight - 50, 100, False)
plat_group.add(platform)



#game loop
run = True
while run:

    clock.tick(FPS)

    if game_over == False: # If the game is over, then all the functions below, like the bacgrounds, and platforms do not appear no more.
        scroll = char.move()

        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(bg_scroll) 
        #generate random sized platforms 
        if len(plat_group)< MAX_PLAT:
                p_w = random.randint(40, 60)
                p_x = random.randint(0, width - p_w)
                p_y = platform.rect.y - random.randint(80, 120)
                p_type = random.randint(1, 2)
                if p_type == 1 and score > 100: # all platforms are stationary after first 500 scrolls 
                    p_moving = True 
                else:
                    p_moving = False
                platform = Platform(p_x, p_y, p_w, p_moving)
                plat_group.add(platform)


        plat_group.update(scroll)

        if len(enemy_group) == 0 and score > 1500:
            enemy = Enemy(width, 100, bird_sheet, 3)
            enemy_group.add(enemy)

        enemy_group.update(scroll, width)

        #draw platform
        if scroll > 0 :
            score += scroll
        # the high score line in the game 
        pygame.draw.line(screen, white, (0, score - High_score + SCROLL_THRESH), (width, score - High_score + SCROLL_THRESH),3)
        draw_text('HIGH SCORE', font_s, white, width - 130, score - High_score + SCROLL_THRESH) # Draws the High-score line when the player has reached a new highscore, with a line.
        #draw player 
        plat_group.draw(screen)
        enemy_group.draw(screen)
        char.draw()

        #game score display
        draw_panel()

        #game over
        if char.rect.top > hight: # If the character has gone below the game  window, then the game is over.
            game_over = True 

    else:
        if fade_counter < width: # Shows the black background when the game is over.
            fade_counter += 5
            #3 black rectangles coming in from the right and 3 rectangles coming from the left. 
            for y in range(0, 6, 2): # 6 rectangles repeating 2 times. Starting at origin.
                pygame.draw.rect(screen, black, (0, y *100, fade_counter, 100))
                pygame.draw.rect(screen, black, (width - fade_counter, (y +1)*100, width, 100))
        else: 
            draw_text("GAME OVER!", font_b, white, 130, 200) # Shows Game Over whenthe player falls of the screen
            draw_text('SCORE: '+ str(score), font_b, white, 130, 250) # Shows the progressive score the player reaches when jump onto higher platforms
            draw_text('PRESS SPACE TO PLAY AGAIN', font_b, white, 40, 300) # Lets you reset the game once the game is over, so you can play again.
            if score > High_score: # If the current score surpasses the previous score, then update the new score to the current one.
                High_score = score 
                with open('score.txt', 'w') as file:
                    file.write(str(High_score))
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]: # If you press the spacebar, then you are able to reset the game, and the score is reset to zero. Basically everything is reset to the beginning.
                game_over = False
                score = 0
                scroll = 0
                fade_counter = 0
                char.rect.center = (width // 2, hight -150)
                plat_group.empty()
                platform = Platform(width // 2 - 50, hight - 50, 100, False) # The starting platform will reset and stay at same position when game is reset.
                plat_group. add(platform)


    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if score > High_score:
                High_score = score 
                with open('score.txt', 'w') as file:
                    file.write(str(High_score))  # so the high score doesn't cancel when the game window is closed, instead it saves the highscore.
            run = False
    
    pygame.display.update()
        
pygame.quit()