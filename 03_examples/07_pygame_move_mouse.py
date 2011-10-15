# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://cs.simpson.edu

import pygame

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
blue     = (  50,  50, 255)
green    = (   0, 255,   0)
dkgreen  = (   0, 100,   0)
red      = ( 255,   0,   0)
purple   = (0xBF,0x0F,0xB5)
brown    = (0x55,0x33,0x00)

# Function to draw the background
def draw_background(screen):
    # Set the screen background
    screen.fill(white)

def draw_item(screen,x,y):
    pygame.draw.rect(screen,green,[0+x,0+y,30,10],0)
    pygame.draw.circle(screen,black,[15+x,5+y],7,0)

pygame.init()

# Set the height and width of the screen
size=[700,500]
screen=pygame.display.set_mode(size)

# Initial position of our object
item_pos=-30

#Loop until the user clicks the close button.
done=False

# Used to manage how fast the screen updates
clock=pygame.time.Clock()

while done==False:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop

    draw_background(screen)
    
    # Get the current mouse position. This returns the position
    # as a list of two numbers.
    pos = pygame.mouse.get_pos()
    
    # Fetch the x and y out of the list, just like we'd fetch letters out of a string.
    x=pos[0]
    y=pos[1]
    
    # Draw the item where the mouse is.
    draw_item(screen,x,y)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)

pygame.quit ()

