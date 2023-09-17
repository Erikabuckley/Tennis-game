# import the pygame module to enable pygame to load,  sys to allow window to auto-close once game has ended, sqlite to create the databse
import pygame
import sys
import sqlite3

# this initializes pygame
pygame.init()

# declared constants for player, court and screen width and height and font to ensure they cannot be changed
WIDTH, HEIGHT = 650, 650
FONT = pygame.font.Font('Agrandir-GrandHeavy.otf', 40)
SMALLFONT = pygame.font.Font('Agrandir-GrandHeavy.otf', 16)
COURT_TOP,COURT_BOTTOM = 75,575
COURT_LEFT, COURT_RIGHT = 150, 500
POINTS = (0,15,30,40,'deuce')
IMGWIDTH, IMGHEIGHT = 50,100

# created the screen, its dimensions and caption and retreived the clock
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Tennis game")
clock = pygame.time.Clock()

##########################################################################################classes#######################################################################################
# created player class to hold all the details for the player
class Player:
    def __init__(self, v, img,gt):
        self.x = 450
        self.y = 450
        self.width = IMGWIDTH
        self.height = IMGHEIGHT
        self.v = v
        self.img = img
        self.gt = gt
        self.flip = False
        self.playerRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.p = self.s = self.g = self.m= 0
 
    # displays the player on the screen
    def display(self):
        self.player = screen.blit(self.img,self.playerRect)

    # updates the cordinates of the players rectangle
    def updatePos(self):
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
    def changeSide(self):
        self.img = pygame.transform.flip(self.img,True,False)
    
    # method to return the current score
    def getPoints(self):
        score = POINTS[int(self.p)],self.s,self.g,self.m
        return(list(score))
    
    # method to find the score that needs to be incremented then increments it and returns wether the game is over or not
    def updateScore(self):
        point = POINTS[int(self.p)]
        if point != 40:
            self.p += 1
            return(False)
        elif point == 40 and self.s !=2 and self.g !=2:
            self.p = 0
            self.s += 1
            return(False)
        elif self.s != 2:
            self.s += 1
            return(False)
        elif self.s == 2 and self.g !=2:
            self.s = 0
            self.g += 1 
            return(False)    
        elif self.g != 2:
            self.g += 1 
            return(False)
        elif self.g == 2:
            self.g = 0
            self.m += 1 
            return(True)

# class for the computer to hold its details
class Computer:
    def __init__(self, v, img):
        self.x = 150
        self.y = 150
        self.width = IMGWIDTH
        self.height = IMGHEIGHT
        self.v = v
        self.img = img
        self.compRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.flip = False
        self.positive = True
        self.p = self.s = self.g = self.m= 0
 
    # displays the object on the screen
    def display(self):
        self.comp = screen.blit(self.img,self.compRect)
    
    # updates the x value to bounce computer across the screen
    def updatePos(self):
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
    def changeSide(self):
        self.img = pygame.transform.flip(self.img,True,False)
    
    # method to return the score of the computer
    def getPoints(self):
        score = POINTS[int(self.p)],self.s,self.g,self.m
        return(list(score))
    
    # method to check the score that needs to be incremented  then increments it and returns wether the game is over or not
    def updateScore(self):
        point = POINTS[int(self.p)]
        if point != 40:
            self.p += 1
            return(False)
        elif point == 40 and self.s !=2 and self.g !=2:
            self.p = 0
            self.s += 1
            return(False)
        elif self.s != 2:
            self.s += 1
            return(False)
        elif self.s == 2 and self.g !=2:
            self.s = 0
            self.g += 1 
            return(False)    
        elif self.g != 2:
            self.g += 1 
            return(False)
        elif self.g == 2:
            self.g = 0
            self.m += 1 
            return(False)

# class to hold the balls details     
class Ball:
    def __init__(self, d, v, img):
        self.x = 0
        self.y = 0
        self.d = d
        self.v = v
        self.img = img
        self.ballRect = pygame.Rect(self.x, self.y,self.d,self.d)
        self.xpos = True
        self.ypos = True
        self.start_side = True
 
    # displays the object on the screen
    def display(self):
        self.ball = screen.blit(self.img,self.ballRect)
    
    # updates the balls cordinates dependent on if it has been hit or not
    def updatePos(self,hit):
        if self.y > 650 or self.y < 0:
            self.y = 300
        elif self.ypos:
            if hit:
                self.y -= 10 *self.v
                self.ypos = False
            else:
                self.y += self.v
                self.ypos = True
        else:
            if hit:
                self.y += 10 * self.v
                self.ypos = True
            else:
                 self.y -= self.v
                 self.ypos = False
        self.ballRect = pygame.Rect(self.x, self.y, self.d, self.d)

    # checks who hit the ball out and returns the winner of the point
    def checkPos(self):
        winner = ''
        if self.x > 150 or self.x > 500: 
            if self.ypos:
                winner = 'comp'
                loss = pygame.mixer.Sound('loss.mp3')
                loss.play()
            elif not self.ypos:
                winner = 'player' 
                win = pygame.mixer.Sound('win.mp3')
                win.play()
        elif self.y > 350:
            winner = 'comp'
            loss = pygame.mixer.Sound('loss.mp3')
            loss.play()
        elif self.y < 0:
            winner = 'player'
            win = pygame.mixer.Sound('win.mp3')
            win.play()
        return winner

######################################################################################################################################################################################

# displays the loading image then waits to look like game is loading
def show_startup():
    start_screen = pygame.image.load('title.png')
    screen.blit(start_screen, (0, 0))
    pygame.display.flip()
    clock.tick(0.25)

# displays the screen for the gamertag selection
def display_gamertag():
    screen.fill('#00BF63')
    text = SMALLFONT.render(
        'Type your gamertag and press RETURN', True, 'white', None)
    text_rect = text.get_rect(center=(WIDTH/2, 50))
    screen.blit(text, text_rect)
    text = SMALLFONT.render(
        "Can not be more than 12 characters long", True, 'white', None)
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
                # checks length is not over 12 characters
                elif length > 12:
                    text = SMALLFONT.render(
                        ('Must be less than 13'), True, 'white', None)
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

# displays the game over screen, saves score then returns to the menu
def game_over_screen(winner):
    screen.fill('#00BF63')
    text = FONT.render('Game over', True, 'white', None)
    text_rect = text.get_rect(center=(WIDTH/2, 300))
    screen.blit(text, text_rect)
    pygame.display.flip()
    if winner != 'computer':
        con = sqlite3.connect("scores_database.db")
        cursor = con.cursor()
        gts = cursor.execute("SELECT gamertag FROM scores WHERE gamertag = ?",(winner,)).fetchall()
        print(gts)
        if gts == []:
            cursor.execute("INSERT INTO scores VALUES (?, ?)",(winner, 1))
        else:
            newscore = cursor.execute("SELECT score FROM scores WHERE gamertag = ?",(winner,)).fetchall()
            newscore = int(newscore[0][0]) + 1
            cursor.execute("UPDATE scores SET score = ? WHERE gamertag = ?",(newscore, winner))
        con.commit()
        con.close()
    clock.tick(0.25)
    show_menu()

# displays the pause screen 
def pause_screen():
        paused = True 
        while paused:
            screen.fill('#00BF63')
            text = FONT.render('Press "p" to unpause', True, 'white', None)
            text_rect = text.get_rect(center=(WIDTH/2, 300))
            screen.blit(text, text_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)
                    if key == 'p':
                        paused = False
                        return

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
    user_player = Player(2,player,gamertag)
    comp_player = Computer(1,comp)
    ball = Ball(15,2,ball)

    # displays images
    comp_player.display()
    user_player.display()
    ball.display()

    # loop to update the game until the game is over
    game_over = False
    while not game_over:
        clock.tick(60)
        for event in pygame.event.get():
            # checks for game quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key == 'p':
                    pause_screen()

        # checks if the ball is on the right of the player or not and flips the image if so 
        if ball.x > user_player.x and not user_player.flip:
            user_player.changeSide()
            user_player.flip = True
        # checks if the ball is on the left of the player and flips the image back
        elif ball.x < user_player.x and user_player.flip:
            user_player.changeSide()
            user_player.flip = False
        # repeats for the computers player
        if ball.x > comp_player.x and not comp_player.flip:
            comp_player.changeSide()
            comp_player.flip = True
        elif ball.x < comp_player.x and comp_player.flip:
            comp_player.changeSide()
            comp_player.flip = False
        
        # checks for collision between either player or computer and updates accordingly
        if ball.ballRect.colliderect(user_player.playerRect) or ball.ballRect.colliderect(comp_player.compRect):
            ball.updatePos(True)
            user_player.updatePos()
            comp_player.updatePos()
        else:
            ball.updatePos(False)
            user_player.updatePos()
            comp_player.updatePos()

        # displays the changes
        screen.blit(bg, (0, 0))
        ball.display()
        user_player.display()
        comp_player.display()

        # shows score board 
        u_points = str(user_player.getPoints())
        c_points = str(comp_player.getPoints())
        text = SMALLFONT.render('{}: {}'.format(gamertag,u_points[1:-1]), True, 'white', None)
        text_rect = text.get_rect(topleft = (5,5))
        screen.blit(text, text_rect)
        text = SMALLFONT.render('Computer: {}'.format(c_points[1:-1]), True, 'white', None)
        text_rect = text.get_rect(topleft = (5,30))
        screen.blit(text, text_rect)
        pygame.draw.rect(screen, 'white', pygame.Rect(3, 2, 300, 48),2)
        pygame.display.flip()

        # checks who won the point and checks which scoring attribute needs updating and then updates it
        if ball.checkPos() == 'player':
            game_over = user_player.updateScore()
            if game_over:
                game_over_screen(gamertag)
        else:
            game_over = comp_player.updateScore()
            if game_over:
                game_over_screen('computer')

             
# function to show instruction screen
def show_instructions():
    in_instruction = True
    while in_instruction:
        instructions = pygame.image.load('instructions.png')
        screen.blit(instructions, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            # checks if user pressed exit
            if event.type == pygame.QUIT:
                # this closes pygame
                pygame.quit()
                sys.exit()
            # checks if escape has been pressed and returns to the menu if so
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key == 'escape':
                    show_menu()

# function to show the leaderboard
def show_board():
    in_board = True
    while in_board:
        screen.fill('#00BF63')
        text = FONT.render('Leaderboard', True, 'white', None)
        text_rect = text.get_rect(center=(WIDTH/2, 50))
        screen.blit(text, text_rect)

        # gets top 10 names and scores then displays them
        con = sqlite3.connect("scores_database.db")
        cursor = con.cursor()
        gts = cursor.execute("SELECT gamertag FROM scores ORDER BY score DESC").fetchall()
        scores = cursor.execute("SELECT score FROM scores ORDER BY score DESC").fetchall()
        con.commit()
        con.close()
        for x in range (10):
            text = FONT.render(gts[x][0], True, 'white', None)
            text_rect = text.get_rect(topleft =(50, 100 + ( 55*x)))
            screen.blit(text, text_rect)
            text = FONT.render(str(scores[x][0]), True, 'white', None)
            text_rect = text.get_rect(topright =(600, 100 + ( 55*x)))
            screen.blit(text, text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            # checks if user pressed exit
            if event.type == pygame.QUIT:
                in_board = False
                # this closes pygame
                pygame.quit()
                sys.exit()
            # checks if escape has been pressed and returns to the menu if so
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key == 'escape':
                    in_board = False
                    show_menu()


# function to show trophy menu
def show_trophies():
    in_instruction = True
    while in_instruction:
        instructions = pygame.image.load('instructions.png')
        screen.blit(instructions, (0, 0))
        for event in pygame.event.get():
            # checks if user pressed exit
            if event.type == pygame.QUIT:
                in_instruction = False
                pygame.quit()
                sys.exit()
            # checks if a key has been pressed and will go to correct screen if so
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key == 'escape':
                    in_instruction = False
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

##########################################################################main game loop###############################################################################################

# calls start up screen function
show_startup()
# calls show_menu function
show_menu()

######################################################################################################################################################################################

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


# if self.start_side:
#     self.x, self.y = 450,425
# else:
#     self.x, self.y = 150,125 
