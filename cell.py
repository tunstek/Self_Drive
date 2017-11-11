import pygame

# Define some colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)



class Cell(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self, width, height, x, y):
        # Call the parent's constructor
        super(Cell, self).__init__()

        self.width = width
        self.height = height
        self.x = x
        self.y = y


        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def checkCoords(self,pos):
        #print pos
        if pos[0] > self.x and pos[0] < self.x+self.width:
            if pos[1] > self.y and pos[1] < self.y+self.height:
                return True
        return False




class Checkpoint(Cell):
    def __init__(self, width, height, x, y):
        # Call the parent's constructor
        super(Checkpoint, self).__init__(width,height,x,y)
        self.image.fill(GREEN)
