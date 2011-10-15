# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://cs.simpson.edu

import pygame

# Define some colors
white=[255,255,255]
black=[0,0,0]

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])

# This sets the name of the window
pygame.display.set_caption('CMSC 150 is cool')

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Fill the screen with a black background
background.fill(black)

clock = pygame.time.Clock()

# Before the loop, load the sounds:
click_sound = pygame.mixer.Sound("click.wav")

# Set positions of graphics
background_position=[0,0]

# Load and set up graphics.
background_image = pygame.image.load("saturn_family1.jpg").convert()
player_image = pygame.image.load("player.png").convert()
player_image.set_colorkey(white)

done = False

while done==False:
    clock.tick(10)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_sound.play() 
            
    # Copy image to screen:
    screen.blit(background_image, background_position)

    # Get the current mouse position. This returns the position
    # as a list of two numbers.
    player_position = pygame.mouse.get_pos()
    x=player_position[0]
    y=player_position[1]
    
    # Copy image to screen:
    screen.blit(player_image, [x,y])
    
    pygame.display.flip()

pygame.quit ()
