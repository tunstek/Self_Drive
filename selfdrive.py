import sys
sys.path.append("/usr/local/lib/python2.7/site-packages")

import math
import pygame
import random
import pickle

from cell import *


# Define some colors
BLACK = (0 ,0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

SCREENWIDTH = 800
SCREENHEIGHT = 600

START_X = 40
START_Y = 40

END_X = 730
END_Y = 590


cellWidth = 40
cellHeight = 25



# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self):
        # Call the parent's constructor
        super(Player, self).__init__()

        self.distanceTraveled = 0

        self.width=20
        self.height=20
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)


        self.movement_speed = 6


        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.rect.x = START_X
        self.rect.y = START_Y


        self.fitness = 0
        # intermitant values for fitness calc we need to keep track of
        self.fitnessTemp = 0
        self.previousCheckpointFitness = 0

        self.checkpointIndex = 0



    def reset(self):
        self.rect.x = START_X
        self.rect.y = START_Y
        self.fitness = 0
        self.fitnessTemp = 0
        self.previousCheckpointFitness = 0
        self.checkpointIndex = 0

    def distanceFromEnd(self):
        return math.sqrt(((END_X-self.rect.x)**2) + ((END_Y-self.rect.y)**2))


    def distanceFromStart(self):
        return math.sqrt(((START_X-self.rect.x)**2) + ((START_Y-self.rect.y)**2))


    def distanceFromCheckpoint(self, checkpoint):
        return math.sqrt(((checkpoint.x-self.rect.x)**2) + ((checkpoint.y-self.rect.y)**2))



    def updateFitness(self, checkpoints):
        if self.checkpointIndex < len(checkpoints):
            dist = self.distanceFromCheckpoint(checkpoints[self.checkpointIndex])
            if dist < 45:
                # Switch to the next checkpoint
                self.checkpointIndex += 1

                self.previousCheckpointFitness = self.fitnessTemp
        else:
            dist = self.distanceFromEnd()

        self.fitnessTemp = self.previousCheckpointFitness + 1/dist
        self.fitness = (self.fitnessTemp * 100000) - 152
        return self.fitness


    # Update the player
    def update(self):

        direction = 0
        keysPressed = pygame.key.get_pressed()

        if keysPressed[pygame.K_a]:
            # Move x according to the axis.
            self.rect.x=int(self.rect.x-self.movement_speed)
            self.distanceTraveled += self.movement_speed
        if keysPressed[pygame.K_d]:
            # Move x according to the axis.
            self.rect.x=int(self.rect.x+self.movement_speed)
            self.distanceTraveled += self.movement_speed
        if keysPressed[pygame.K_w]:
            # Move y according to the axis.
            self.rect.y=int(self.rect.y-self.movement_speed)
            self.distanceTraveled += self.movement_speed
        if keysPressed[pygame.K_s]:
            # Move y according to the axis.
            self.rect.y=int(self.rect.y+self.movement_speed)
            self.distanceTraveled += self.movement_speed








# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])

# Set the title of the window
pygame.display.set_caption('Self Drive')

# Enable this to make the mouse disappear when over our window
pygame.mouse.set_visible(1)

# This is a font we use to draw text on the screen (size 36)
font = pygame.font.Font(None, 36)

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())


movingsprites = pygame.sprite.Group()







#Array for checkpoints and walls
checkpoints = []
walls = []
#The array for surface cells
cellArray = []


# Load the map
#Load the cell data from file
cellData = pickle.load( open( "map.bin", "rb" ) )
#Create the cells
for data in cellData:
    if data[2] == "wall":
        temp = Cell(cellWidth,cellHeight,data[0],data[1])
        movingsprites.add(temp)
        cellArray.append(temp)
        walls.append(temp)
    if data[2] == "checkpoint":
        temp = Checkpoint(cellWidth,cellHeight,data[0],data[1])
        movingsprites.add(temp)
        cellArray.append(temp)
        checkpoints.append(temp)
# Map loaded





# Create the player paddle object
player = Player()
movingsprites.add(player)


clock = pygame.time.Clock()
done = False
exit_program = False


while not exit_program:

    # Clear the screen
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True



    if not done:
        # Update the player
        player.update()
        print player.updateFitness(checkpoints)


    # If we are done, print game over
    if done:
        text = font.render("You Win!!!", 1, RED)
        textpos = text.get_rect(centerx=background.get_width()/2)
        textpos.top = 40
        screen.blit(text, textpos)


    # See if the ball hits the player paddle
    if pygame.sprite.spritecollide(player, walls, False):
        print "Collision"
        player.reset()


    # If the player gets off the screen it wins
    # Right or left side of the screen
    if player.rect.x > player.screenwidth - player.width:
        done = True
    if player.rect.x < 0:
        done = True
    # Top or bottom of the screen
    if player.rect.y > player.screenheight - player.height:
        done = True
    if player.rect.y < 0:
        done = True



    # Draw Everything
    movingsprites.draw(screen)

    # Update the screen
    pygame.display.flip()

    clock.tick(30)

pygame.quit()
