#import libraries to use the pygame and ranom objects to apply the built-in functions for the game.
import pygame 
import random # Imports various randomized methods.

#initialise pygame imports all pygame modules. 
pygame.init()

# Dimensions for Game Window
SCREEN_WIDTH = 400 # 400 pixels will be the width ("Wide") assigned to variable SCREEN_WIDTH. This is a constant variable this is why it is capitilized
SCREEN_HEIGHT = 600 # 600 pixels will be the height ("Tall") assigned to variable SCREEN_HEIGHT
 
#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #Creates the actual game window with the "SCREEN_WIDTH" and "SCREE_HEIGHT" and assigns it to variable screen.
pygame.display.set_caption('Jumpy') # This is a caption, which is the text that is at the top of the window when the games runs

#set frame rate
clock = pygame.time.Clock() # The function to set the frame rate.
FPS = 60 #We want to start with 60 frames per second.

#game variables
SCROLL_THRESH = 200 
GRAVITY = 1 # Setting Gravity to one pixel
MAX_PLATFORMS = 10 #There is a contstant steam of 10 platforms generated each turn.
scroll = 0
bg_scroll = 0

#define colours
WHITE = (255, 255, 255) # RGB values to assign the colour white

#load images
# The variables import downloaded images, using pygame.image.load(), we want as the background, player, and platforms. Withtin the '' (quotations) we specify where the images are located on our computer.
jumpy_image = pygame.image.load('assets/jump.png').convert_alpha() 
bg_image = pygame.image.load('assets/bg.png').convert_alpha()
platform_image = pygame.image.load('assets/wood.png').convert_alpha()

#function for drawing the background
def draw_bg(bg_scroll):
	screen.blit(bg_image, (0, 0 + bg_scroll)) # We want to blit and show the images "bg_image" located at the top left corner (0,0)
	screen.blit(bg_image, (0, -600 + bg_scroll))

#player class
# Classes provide a means of bundling data and functionality together. 
class Player():
	def __init__(self, x, y): # x,y are the starting coordinates of the player.
		self.image = pygame.transform.scale(jumpy_image, (45, 45)) #The jumpy_image is assigned to the player. With the transform.scale we scale it to be 45 pixels wide and 45 pixels tall.
		self.width = 25 # Player's width is 25 pixels
		self.height = 40 # Player's height is 40 pixels
		self.rect = pygame.Rect(0, 0, self.width, self.height) # Making a rectangle for the image of the player
		self.rect.center = (x, y)
		self.vel_y = 0 #Velocity in the y-direction.
		self.flip = False

	def move(self):
		#reset variables
		scroll = 0
		dx = 0 # The change in the x-coordinate.
		dy = 0 # The chnage in the y-coordinate.

		#process keypresses
		key = pygame.key.get_pressed() # This tell us which keys are being pressed on the keyboard.
		if key[pygame.K_a]: # This says if the key "a" is pressed then the player will move left.
			dx = -10 
			self.flip = True # pygame's function self.flip allows you to flip an image 180 degrees. This makes the image flip whenn the key "a" is pressed.
		if key[pygame.K_d]: # If the key "d" is pressed then the player will move right.
			dx = 10
			self.flip = False # Player starts as not flipped.

		#gravity
		self.vel_y += GRAVITY # The velocity in the y-direction will increase every itteration by 1 pixel. Accelerates at every itteration.
		dy += self.vel_y

		#ensure player doesn't go off the edge of the screen
        # Can only move left and right on within the game window.
		if self.rect.left + dx < 0: # Checking the direction of the left, to not move the charcater off the left hand side of the screen.
			dx = -self.rect.left
		if self.rect.right + dx > SCREEN_WIDTH: # Checking the direction of the right, to not move the charcater off the right hand side of the screen
			dx = SCREEN_WIDTH - self.rect.right


		#check collision with platforms
		for platform in platform_group:
			#collision in the y direction
			if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height): #Checking if there is a collision whent he player hits the bottom of the platforms.
				#check if above the platform
				if self.rect.bottom < platform.rect.centery:
					if self.vel_y > 0: #The player is falling because of the positive variable.
						self.rect.bottom = platform.rect.top
						dy = 0
						self.vel_y = -20 # Allows the player to jump off the platforms at the same y-velocity as jumping from the bottom of the game window.


		#check collision with ground
		if self.rect.bottom + dy > SCREEN_HEIGHT: # Checking whether moving by the variable "dy" will move us off the screen in the game window.
			dy = 0 # Once the charcater hits the bottom of the game window, we want the character to freeze.
			self.vel_y = -20 # determines how hard the player bounces off the screen.


		#check if the player has bounced to the top of the screen
		if self.rect.top <= SCROLL_THRESH:
			#if player is jumping
			if self.vel_y < 0: 
				scroll = -dy # If the player is moving up the screen, then we want everything else to move down.

		#update rectangle position
		self.rect.x += dx
		self.rect.y += dy + scroll # Freezes on the position of the screen. Surpases the high-score white line.

		return scroll

	def draw(self):
        #pygame.transform.flip flips the image of the character.
		screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5)) # Method within the player class, this draws the image of the character. The self.rect.x or self.rect.y offests the white border and the player's image.
		pygame.draw.rect(screen, WHITE, self.rect, 2) # Making the border of the character white.



#platform class
class Platform(pygame.sprite.Sprite): # The Sprite class is intended to be used as a base class for the different types of objects in the game. They are a convenient way of grouping data and code into a single entity
	def __init__(self, x, y, width):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(platform_image, (width, 10)) #Scaling the platforms image, makin all the platforms 10 pixels.
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, scroll):

		#update platform's vertical position
		self.rect.y += scroll

		#check if platform has gone off the screen
		if self.rect.top > SCREEN_HEIGHT: # Checking if the platform is below the game window.
			self.kill()

#player instance
jumpy = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150) # Making the player's dimensions on the game, which is located at the bottom of the game window.

#create sprite groups
platform_group = pygame.sprite.Group()

#create starting platform
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100)
platform_group.add(platform)

#game loop
run = True # Setting the variable "run" to True to help the loop below. This is not a constant variable because it can change to false, this is why it isn't capitalized.
while run: # This is an infinite loop that keeps the game constantly on the screen, until we tell it to exit. As long as the variable "run" is True, then we can continue executing the code we have above.

	clock.tick(FPS) # Initiates the frame rate to being able to control the speed of the frames in the game.

	scroll = jumpy.move() # This allows to move the character.

	#draw background
	bg_scroll += scroll
	if bg_scroll >= 600: # Resets the background image when the player exceeds the previous background image.
		bg_scroll = 0
	draw_bg(bg_scroll)

	#generate platforms
	if len(platform_group) < MAX_PLATFORMS: # How many platforms we have generated at that moment. If the number of platforms is less than 10, the generate more.
		p_w = random.randint(40, 60) # Randomizes the width of the platforms.
		p_x = random.randint(0, SCREEN_WIDTH - p_w) # Randomizes the location for the x-diretions, but cannot exceed the platform's width.
		p_y = platform.rect.y - random.randint(80, 120) # Furthest the platorms can go to the right is limited to the width. Spacing all the platforms by 80 to 120 pixels.
		platform = Platform(p_x, p_y, p_w) 
		platform_group.add(platform)

	#update platforms
	platform_group.update(scroll)

	#draw sprites
	platform_group.draw(screen)
	jumpy.draw()


	#event handler
	for event in pygame.event.get(): # runs through the code line by line and allows use to press keys on the keyboard or the mouse to close the game down.
		if event.type == pygame.QUIT: # The specific event we want to target is when we want to quit or exit the game, by clicking the "x on the top right of the game window."
			run = False # To come out of the while loop we need to set the run variable to False


	#update display window
	pygame.display.update() #Takes all the information and updates the screen with it. This line in the game loop allows the background image, play image, and platform image to continue existing and looping.



pygame.quit() # This is the opposite of the pygame.init to quit all pygame imports in all pygame modules.