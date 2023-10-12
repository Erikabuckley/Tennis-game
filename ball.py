#Import the nesicary modules
import pygame

# class to hold the balls details     
class Ball:
    def __init__(self, d, v, img,screen):
        self.x = 425
        self.y = 505
        self.d = d
        self.v = v
        self.img = img
        self.ballRect = pygame.Rect(self.x, self.y,self.d,self.d)
        self.xpos = True
        self.ypos = True
        self.direction = 1
        self.screen = screen
        self.courttop,self.courtbottom = 75,575
        self.courtleft, self.courtright = 174,471

    # displays the object on the self.screen
    def display(self):
        self.ball = self.screen.blit(self.img,self.ballRect)
    
    # updates the balls cordinates dependent on if it has been hit or not
    def updatePos(self,hit):
        if self.y > 650 or self.y < 0:
            self.y = 300
        elif self.ypos:
            if hit:
                self.y -= 10 *self.v
                self.y -= 3 *self.v
                self.ypos = False
            else:
                self.y += self.v
                self.ypos = True
        else:
            if hit:
                self.y += 10 * self.v
                self.y += 3 *self.v
                self.ypos = True
            else:
                self.y -= self.v
                self.ypos = False
        # alters x direction
        if self.direction == 1:
            self.x -= self.v/2
        elif self.direction == 2:
            pass
        elif self.direction == 3:
            self.x += self.v/2
        self.ballRect = pygame.Rect(self.x, self.y, self.d, self.d)

    # checks who hit the ball out and returns the winner of the point
    def checkPos(self):
        winner = ''
        if self.ballRect.left <= self.courtleft or self.ballRect.right >= self.courtright:
            if self.ypos:
                if self.ballRect.bottom <= 325:
                    winner = 'player'
                else:
                    winner = 'computer'
            elif not self.ypos:
                if self.ballRect.top >= 325:
                    winner = 'computer'
                else:
                    winner = 'player'
        elif self.y > self.courtbottom:
            winner = 'computer'
        elif self.y < self.courttop:
            winner = 'player' 
        # play sound    
        if winner == 'computer':
            loss = pygame.mixer.Sound('loss.mp3')
            loss.play()
        elif winner == 'player':
            win = pygame.mixer.Sound('win.mp3')
            win.play()
        return winner
    
    # method to set x and y
    def startPos(self,server):
        if server:
            self.x, self.y = 425,505
        else:
            self.x, self.y = 240,180
            self.ypos = True
        self.ballRect = pygame.Rect(self.x, self.y, self.d, self.d)