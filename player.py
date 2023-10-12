#Import the nesicary modules
import pygame 

# created parent class to hold all the details for the player
class Player:
    def __init__(self, v, img,screen,points,server):
        self.x = 0
        self.y = 0
        self.width = 92
        self.height = 100
        self.v = v
        self.img = img
        self.flip = False
        self.playerRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.p = self.s = self.g = self.m = 0
        self.screen = screen
        self.points = points
        self.server = server
        self.courttop = 75
        self.courtbottom = 575
        self.courtleft = 174
        self.courtright = 471

    # displays the player on the self.screen
    def display(self):
        self.player = self.screen.blit(self.img,self.playerRect)
    
    # reflects the image in the y axis
    def changeSide(self):
        self.img = pygame.transform.flip(self.img,True,False)
    
    # method to return the current score

    def getPoints(self):
        score = self.points[int(self.p)],self.s,self.g,self.m
        return(list(score))
    
    # method to find the score that needs to be incremented then increments it and returns wether the game is over or not
    def updateScore(self):
        point = self.points[int(self.p)]
        if point != 40:
            self.p += 1
            return(True,False,False,False)
        elif point == 40 and self.s !=2 and self.g !=2:
            self.s += 1
            global server 
            self.server = not self.server
            return(False,True,False,False)
        elif self.s != 2:
            self.s += 1
            return(False,True,False,False)
        elif self.s == 2 and self.g !=2:
            self.g += 1 
            return(False,False,True,False)    
        elif self.g != 2:
            self.g += 1 
            return(False,False,True,False)
        elif self.g == 2:
            self.m += 1 
            return(False,False,False,True)
        else:
            return(False,False,False,False)
        
    # method to update x and y     
    def update(self,x,y):
        self.x = x
        self.y = y
        self.playerRect = pygame.Rect(self.x, self.y, self.width, self.height)