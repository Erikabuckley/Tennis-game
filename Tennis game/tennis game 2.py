# import the pygame module to enable pygame to load and sys to allow window to auto-close once game has ended
import pygame
import sys
import random

# this initializes pygame
pygame.init()

# declared constants for width, height and font to ensure they cannot be changed
WIDTH, HEIGHT = 650, 650
FONT = pygame.font.Font('Agrandir-GrandHeavy.otf', 40)
SMALLFONT = pygame.font.Font('Agrandir-GrandHeavy.otf', 20)
COURT_TOP,COURT_BOTTOM = 75,575
COURT_LEFT, COURT_RIGHT = 150, 500
POINTS = (0,15,30,40,'deuce',50)

# created the screen, its dimensions and caption and retreived the clock
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Tennis game")
clock = pygame.time.Clock()

# created player class to hold all the details for the player
class Player:
    def __init__(self,x, y, width, height, v, img,gt):
        self.x =x
        self.y = y
        self.width = width
        self.height = height
        self.v = v
        self.img = img
        self.gt = gt
        self.flip = False
        self.playerRect = pygame.Rect(x, y, width, height)
        self.p = 0
        self.s = 0
        self.g = 0
        self.m = 0
 
    # displays the player on the screen
    def display(self):
        self.player = screen.blit(self.img,self.playerRect)

    # updates the cordinates of the players rectangle
    def update_pos(self):
        # checks the key that has been presed and returns new x and y values
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.v
        elif keys[pygame.K_RIGHT] and self.x < (WIDTH - self.width):
            self.x += self.v
        elif keys[pygame.K_UP] and self.y > 325:
            self.y -= self.v
        elif keys[pygame.K_DOWN] and self.y < (HEIGHT - self.height):
            self.y += self.v
        self.playerRect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    # reflects the image in the y axis
    def change_side(self):
        self.img = pygame.transform.flip(self.img,True,False)
    
    # gets the objects rectangle
    def getRect(self):
        return self.playerRect
    
    def getPoints(self):
        score = self.p,self.s,self.g,self.m
        return(list(score))
    
    # def checkScore(self):
        # if self.p != 50:
            
        
        # elif player[0] == 50:
        #     return(False, 'set')

        # if player[1] != 3:
        #     return(False, 'set')
        
        # elif player[1] == 3:
        #     return(False, 'game')    
        
        # if player[2] != 3:
        #     return(False, 'game')
        
        # elif player[2] == 3:
        #     return(True, 'match')
        # else:
        #     return(True,'error')

# class for the computer to hold its details
class Computer:
    def __init__(self,x, y, width, height, v, img):
        self.x =x
        self.y = y
        self.width = width
        self.height = height
        self.v = v
        self.img = img
        self.compRect = pygame.Rect(x, y, width, height)
        self.flip = False
        self.positive = True
        self.p = 0
        self.s = 0
        self.g = 0
        self.m = 0

 
    # displays the object on the screen
    def display(self):
        self.comp = screen.blit(self.img,self.compRect)
    
    # updates the x value to bounce computer across the screen
    def update_pos(self):
        if self.positive:
            self.x += self.v
            if self.x == (WIDTH - self.width):
                self.positive = False
        else:
            self.x -= self.v
            if self.x == 0:
                self.positive = True
    
        self.compRect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    # reflects the image in the y axis
    def change_side(self):
        self.img = pygame.transform.flip(self.img,True,False)
    
    # gets the objects rectangle
    def getRect(self):
        return self.compRect
    
    def getPoints(self):
        score = self.p,self.s,self.g,self.m
        return(list(score))

# class to hold the balls details     
class Ball:
    def __init__(self, x, y, d, v, img):
        self.x = x
        self.y = y
        self.d = d
        self.v = v
        self.img = img
        self.ballRect = pygame.Rect(x, y,d,d)
        self.xpos = True
        self.ypos = True
 
    # displays the object on the screen
    def display(self):
        self.ball = screen.blit(self.img,self.ballRect)
    
    # updates the balls cordinates dependent on if it has been hit or not
    def update_pos(self,hit):
        if self.y > 650 or self.y < 0:
            self.y = 300
        elif self.ypos:
            if hit:
                self.y = random.randint(COURT_TOP, self.y)
                self.x = random.randint(COURT_LEFT, COURT_RIGHT)
                self.positive = False
            else:
                self.y += self.v
                self.positive = True
        else:
            if hit:
                self.y += self.v
                self.x -= self.v
                self.positive = True
            else:
                 self.y += self.v
                 self.positive = False

        self.ballRect = pygame.Rect(self.x, self.y, self.d, self.d)


    # gets the balls rectangle 
    def getRect(self):
        return self.ballRect
        
# displays the loading image then waits to look like game is loading
def show_SU():
    start_screen = pygame.image.load('title.png')
    screen.blit(start_screen, (0, 0))
    pygame.display.flip()
    clock.tick(0.25)

# function to display the screen for the gamertag selection
def display_gamertag():
    screen.fill('#00BF63')
    text = SMALLFONT.render(
        'Type your gamertag and press RETURN', True, 'white', None)
    text_rect = text.get_rect(center=(WIDTH/2, 50))
    screen.blit(text, text_rect)
    text = SMALLFONT.render(
        "Can not be more than 16 characters long", True, 'white', None)
    text_rect = text.get_rect(center=(WIDTH/2, 100))
    screen.blit(text, text_rect)
    text = SMALLFONT.render(
        'Must be only numbers and letters', True, 'white', None)
    text_rect = text.get_rect(center=(WIDTH/2, 150))
    screen.blit(text, text_rect)
    text = SMALLFONT.render('Your gamertag is:', True, 'white', None)
    text_rect = text.get_rect(center=(WIDTH/2, 300))
    screen.blit(text, text_rect)
    pygame.display.flip()

# creates gamertag selection screen
def start_game():
    screen.fill('#00BF63')
    text = FONT.render('What background?', True, 'white', None)
    text_rect = text.get_rect(center=(WIDTH/2, 50))
    screen.blit(text, text_rect)
    text = FONT.render('1, 2 or 3', True, 'white', None)
    text_rect = text.get_rect(center=(WIDTH/2, 400))
    screen.blit(text, text_rect)
    img = pygame.image.load('bgs.png')
    img = pygame.transform.scale(img, (400, 100))
    screen.blit(img, (120, 200))

    pygame.display.flip()

    # gets users requested background
    bg = None
    while bg is None:
        # checks exit has not been pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # returns to menu if escape has been pressed
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key == 'escape':
                    show_menu()
                elif key in ['1', '2', '3']:
                    bg = 'bg_'+key+'.png'

    # creates player selection screen
    screen.fill('#00BF63')
    text = FONT.render('Which player?', True, 'white', None)
    text_rect = text.get_rect(center=(WIDTH/2, 50))
    screen.blit(text, text_rect)
    text = FONT.render('1, 2 or 3', True, 'white', None)
    text_rect = text.get_rect(center=(WIDTH/2, 400))
    screen.blit(text, text_rect)
    img = pygame.image.load('players.jpg')
    img = pygame.transform.scale(img, (400, 100))
    screen.blit(img, (120, 200))
    pygame.display.flip()

    # gets users requested player
    player = None
    while player is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key == 'escape':
                    show_menu()
                elif key in ['1', '2', '3']:
                    player = 'player_'+key+'.png'

    # shows pick gamertag screen and gets users gamertag
    display_gamertag()

    # start of gamertag selection code by setting all variables
    gamertag = ''
    key = 'null'
    while key != 'return':
        for event in pygame.event.get():
            length = len(gamertag)
            # checks for game quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                # checks if user wants to return to the menu
                if key == 'escape':
                    show_menu()
                # checks if backspace is pressed if so will remove last character
                elif key == 'backspace':
                    gamertag = gamertag[:-1]
                    display_gamertag()
                    text = SMALLFONT.render((gamertag), True, 'white', None)
                    text_rect = text.get_rect(center=(WIDTH/2, 350))
                    screen.blit(text, text_rect)
                    pygame.display.flip()
                # checks length is not over 15 characters
                elif length > 15:
                    text = SMALLFONT.render(
                        ('Must be less than 16'), True, 'white', None)
                    text_rect = text.get_rect(center=(WIDTH/2, 250))
                    screen.blit(text, text_rect)
                    pygame.display.flip()
                elif key == 'return' or len(key) > 1 or not (key.isalpha() or key.isdigit()):
                    pass
                else:
                    # adds character to gamertag
                    gamertag += key
                    display_gamertag()
                    text = SMALLFONT.render((gamertag), True, 'white', None)
                    text_rect = text.get_rect(center=(WIDTH/2, 350))
                    screen.blit(text, text_rect)
                    pygame.display.flip()

    # returns  the values back to the main progam
    return (bg, player, gamertag)



# start of main game by loading images
def play_game(bg, player, gamertag):
    
    bg = pygame.image.load(bg)
    player = pygame.image.load(player)
    player = pygame.transform.scale(player, (50, 100))
    comp = pygame.image.load('player_1.png')
    comp = pygame.transform.scale(comp, (50, 100))
    ball = pygame.image.load('ball.png')
    ball = pygame.transform.scale(ball, (15, 15))
    
    #sets inital values for locations and vs
    user_player = Player(450,450,50,100,2,player,gamertag)
    comp_player = Computer(50,50,50,100,1,comp)
    ball = Ball(400,400,15,2,ball)

    # displays images
    comp_player.display()
    user_player.display()
    ball.display()

    # loop to update the locations by calling the functions
    game_over = False

    while not game_over:
        clock.tick(60)
        for event in pygame.event.get():
            # checks for game quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # checks if the ball is on the right of the player or not and flips the image if so 
        if ball.x > user_player.x and not user_player.flip:
            user_player.change_side()
            user_player.flip = True
        # checks if the ball is on the left of the player and flips the image back
        elif ball.x < user_player.x and user_player.flip:
            user_player.change_side()
            user_player.flip = False
        # repeats for the computers player
        if ball.x > comp_player.x and not comp_player.flip:
            comp_player.change_side()
            comp_player.flip = True
        elif ball.x < comp_player.x and comp_player.flip:
            comp_player.change_side()
            comp_player.flip = False
        
        # checks for collision betwein either player or computer and updates accordingly
        if ball.ballRect.colliderect(user_player.playerRect) or ball.ballRect.colliderect(comp_player.compRect):
            ball.update_pos(True)
            user_player.update_pos()
            comp_player.update_pos()
        else:
            ball.update_pos(False)
            user_player.update_pos()
            comp_player.update_pos()

        # displays the changes
        screen.blit(bg, (0, 0))
        ball.display()
        user_player.display()
        comp_player.display()
        pygame.display.flip()

        player_score = user_player.getPoints()
        computer_score = comp_player.getPoints()
        # point_winner = 'bob'

        # if point_winner == 'player':
        #     game_over = ,update = check_score(player_score)
        # else:
        #     game_over,update = check_score(computer_score)


# function to show instruction screen
def show_instructions():
    instructions = pygame.image.load('instructions.png')
    screen.blit(instructions, (0, 0))
    for event in pygame.event.get():
        # checks if user pressed exit
        if event.type == pygame.QUIT:
            # this closes pygame
            pygame.quit()
            sys.exit()
        # checks if a key has been pressed and will go to correct screen if so
        elif event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            if key == 'escape':
                show_menu()

# function to show the leaderboard
def show_board():
    instructions = pygame.image.load('instructions.png')
    screen.blit(instructions, (0, 0))
    for event in pygame.event.get():
        # checks if user pressed exit
        if event.type == pygame.QUIT:
            # this closes pygame
            pygame.quit()
            sys.exit()
        # checks if a key has been pressed and will go to correct screen if so
        elif event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            if key == 'escape':
                show_menu()

# function to show trophy menu
def show_trophies():
    instructions = pygame.image.load('instructions.png')
    screen.blit(instructions, (0, 0))
    for event in pygame.event.get():
        # checks if user pressed exit
        if event.type == pygame.QUIT:
            # this closes pygame
            pygame.quit()
            sys.exit()
        # checks if a key has been pressed and will go to correct screen if so
        elif event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            if key == 'escape':
                show_menu()

# displays menu screen
def show_menu():
    menu = pygame.image.load('menu.png')
    screen.blit(menu, (0, 0))
    pygame.display.flip()
    repeat = True
    while repeat:
        for event in pygame.event.get():
            # checks if user pressed exit
            if event.type == pygame.QUIT:
                repeat = False
                # this closes pygame
                pygame.quit()
                sys.exit()
            # checks if a key has been pressed and will go to correct screen if so
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key == 's':
                    bg_pick, comp_pick, gamertag = start_game()
                    play_game(bg_pick, comp_pick, gamertag)
                    repeat = False
                elif key == 'i':
                    show_instructions()
                    repeat = False
                elif key == 'l':
                    show_board()
                    repeat = False
                elif key == 't':
                    show_trophies()
                    repeat = False
                elif key == 'escape':
                    show_menu()          
        # update the display to show the changes
        pygame.display.flip()

# main game loop

# calls start up screen function
show_SU()
# calls show_menu function
show_menu()


# # checks if mouse has been pressed and will go to the correct screen if so
# elif event.type == pygame.MOUSEBUTTONDOWN:
#  pos=pygame.mouse.get_pos()
#  if pos[0] > 150 and pos[0] < 450:
#     if pos[1] > 130 and pos[1] < 210:
#         start_game()
#     elif pos[1] > 250 and pos[1] < 330:
#         show_instructions()
#     elif pos[1] >370 and pos[1] < 450:
#         show_leaderboard()
#     elif pos[1] >490 and pos[1] < 570:
#         show_trophies()

# # changes to game over screen
# screen.fill('#00BF63')
# text = FONT.render('Game over', True, 'white', None)
# text_rect = text.get_rect(center=(WIDTH/2, 300))
# screen.blit(text, text_rect)
# pygame.display.flip()
# show_menu()