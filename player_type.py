#imported pygame to accsess its modules
import pygame
from player import Player

# child class for the user to hold its added details
class User(Player):
    def __init__(self, v, img, screen,points,server):
        Player.__init__(self,v, img,screen,points,server)
        self.x = 425
        self.y = 525
        self.playerRect = pygame.Rect(self.x, self.y, self.width, self.height)

    # updates the cordinates of the players rectangle
    def updatePos(self):
        # checks the key that has been presed and returns new x and y values
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.v
        elif keys[pygame.K_RIGHT] and self.playerRect.right < 650:
            self.x += self.v
        elif keys[pygame.K_UP] and self.y > 325:
            self.y -= self.v
        elif keys[pygame.K_DOWN] and self.playerRect.bottom < 650:
            self.y += self.v
        self.playerRect = pygame.Rect(self.x, self.y, self.width, self.height)
    
# child class for the computer to hold its details
class Computer(Player):
    def __init__(self, v, img,screen,points,server):
        Player.__init__(self,v,img,screen,points,server)
        self.x = 175
        self.y = 75
        self.playerRect = pygame.Rect(self.x, self.y, self.width, self.height)

    # updates the location of the computer player
    def updatePos(self,x,y,v):
        new_ball_x = x 
        new_ball_y = y + v

        # move x value
        if self.playerRect.centerx < new_ball_x and self.playerRect.right < self.courtright:
            if new_ball_x - self.playerRect.centerx >= 5:
                self.x += self.v
                
        elif self.playerRect.centerx > new_ball_x and self.playerRect.left > self.courtleft:
            if self.playerRect.centerx -new_ball_x >= 5:
                self.x -= self.v
        # check if out of court
        if self.x >= self.courtright:
            self.x = self.courtright - self.width
        elif self.x <= self.courtleft:
            self.x = self.courtleft
        self.playerRect = pygame.Rect(self.x, self.y, self.width, self.height)
        