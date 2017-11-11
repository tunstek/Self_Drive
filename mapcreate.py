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

SCREENWIDTH = 800
SCREENHEIGHT = 600

cellWidth = 40
cellHeight = 25




def toggleCellOnMap(movingsprites, cellArray, cellType):
    pos = pygame.mouse.get_pos()
    spriteRemoved = False


    for sprite in movingsprites:
        if type(sprite) is Cell or type(sprite) is Checkpoint:
            #print "CELL OBJECT"
            if sprite.checkCoords(pos):
                # A cell already exists in this position
                movingsprites.remove(sprite)
                for cell in cellArray:
                    if cell.x == sprite.x and cell.y == sprite.y:
                        cellArray.remove(cell)
                        #print "Removed cell from cellArray"
                spriteRemoved = True
                #print "Cell Removed"
                break
    if not spriteRemoved:
        if cellType is "wall":
            temp = Cell(cellWidth,cellHeight,pos[0]-cellWidth/2,pos[1]-cellHeight/2)
            cellArray.append(temp)
        elif cellType is "checkpoint":
            temp = Checkpoint(cellWidth,cellHeight,pos[0]-cellWidth/2,pos[1]-cellHeight/2)
            cellArray.append(temp)
        else:
            print "ERR: unknown cell type!"
            exit()
        movingsprites.add(temp)

        #print "Cell Added"


    # Save state
    dataArray = []
    for cell in cellArray:
        cellData = []
        cellData.append(cell.x)
        cellData.append(cell.y)
        if type(cell) == Cell:
            cellData.append("wall")
        if type(cell) == Checkpoint:
            cellData.append("checkpoint")
        dataArray.append(cellData)

    #Save moving sprites to bin file
    binary_file = open('map.bin',mode='wb')
    cellArray_bin = pickle.dump(dataArray, binary_file)
    binary_file.close()




movingsprites = pygame.sprite.Group()




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


clock = pygame.time.Clock()
done = False
exit_program = False




#The array for surface cells
cellArray = []

#Load the cell data from file
cellData = pickle.load( open( "map.bin", "rb" ) )
#Create the cells
checkpointCount = 0
for data in cellData:
    if data[2] == "wall":
        temp = Cell(cellWidth,cellHeight,data[0],data[1])
        movingsprites.add(temp)
        cellArray.append(temp)
    if data[2] == "checkpoint":
        checkpointCount += 1
        temp = Checkpoint(cellWidth,cellHeight,data[0],data[1])
        movingsprites.add(temp)
        cellArray.append(temp)
        print "Checkpoint " + str(checkpointCount) + " : (" + str(data[0]) + ", " + str(data[1]) + ")" 



while not exit_program:

    # Clear the screen
    screen.fill(BLACK)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True
        if event.type == pygame.MOUSEBUTTONUP:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LSHIFT]:
               toggleCellOnMap(movingsprites, cellArray, "checkpoint")
            else:
               toggleCellOnMap(movingsprites, cellArray, "wall")




    # Draw Everything
    movingsprites.draw(screen)

    # Update the screen
    pygame.display.flip()

    clock.tick(30)

pygame.quit()
