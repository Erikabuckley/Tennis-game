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

# con = sqlite3.connect("scores_database.db")
# cursor = con.cursor()
# cursor.execute("DELETE FROM scores WHERE score = 0 or score = 1").fetchall()
# con.commit()
# con.close()

# created the screen, its dimensions and caption and retreived the clock
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Tennis game")
clock = pygame.time.Clock()

##########################################################################################classes#######################################################################################
# created player class to hold all the details for the player
class Player:
    def __init__(self, v, img,gt):
        self.x = 425
        self.y = 525
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
            self.x , self.y = 450,450
            return(False)
        elif point == 40 and self.s !=2 and self.g !=2:
            self.p = 0
            self.s += 1
            global server 
            server = not server
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
        
    # method to update x and y     
    def update(self,x,y):
        self.x = x
        self.y = y
        self.playerRect = pygame.Rect(self.x, self.y, self.width, self.height)

# class for the computer to hold its details
class Computer:
    def __init__(self, v, img):
        self.x = 175
        self.y = 75
        self.width = IMGWIDTH
        self.height = IMGHEIGHT
        self.v = v
        self.img = img
        self.compRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.flip = False
        self.xpos = True
        self.p = self.s = self.g = self.m= 0
 
    # displays the object on the screen
    def display(self):
        self.comp = screen.blit(self.img,self.compRect)
    
    # updates the x value to bounce computer across the screen
    def updatePos(self):
        if self.xpos:
            self.x += self.v
            if self.x >= (WIDTH - 150 - self.width):
                self.xpos = False
        else:
            self.x -= self.v
            if self.x <= 150:
                self.xpos = True
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
            self.x , self.y = 150,75
            return(False)
        elif point == 40 and self.s !=2 and self.g !=2:
            self.p = 0
            self.s += 1
            global server 
            server = not server
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
    
    # method to update x and y     
    def update(self,x,y):
        self.x = x
        self.y = y
        self.compRect = pygame.Rect(self.x, self.y, self.width, self.height)

# class to hold the balls details     
class Ball:
    def __init__(self, d, v, img):
        self.x = 425
        self.y = 505
        self.d = d
        self.v = v
        self.img = img
        self.ballRect = pygame.Rect(self.x, self.y,self.d,self.d)
        self.xpos = True
        self.ypos = True
 
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
                self.x -= 2*self.v
                self.ypos = False
            else:
                self.y += self.v
                self.x += 1
                self.ypos = True
        else:
            if hit:
                self.y += 10 * self.v
                self.y += 3 *self.v
                self.ypos = True
            else:
                self.y -= self.v
                self.ypos = False
                self.x -= 1

        self.ballRect = pygame.Rect(self.x, self.y, self.d, self.d)

    # checks who hit the ball out and returns the winner of the point
    def checkPos(self):
        winner = ''
        if self.x < 150 or self.x > 500: 
            if self.ypos:
                winner = 'computer'
                loss = pygame.mixer.Sound('loss.mp3')
                loss.play()
            elif not self.ypos:
                winner = 'player' 
                win = pygame.mixer.Sound('win.mp3')
                win.play()
        elif self.y > 575:
            winner = 'computer'
            loss = pygame.mixer.Sound('loss.mp3')
            loss.play()
        elif self.y < 75:
            winner = 'player'
            win = pygame.mixer.Sound('win.mp3')
            win.play()
        return winner
    
    # method to set x and y
    def startPos(self,server):
        if server:
            self.x, self.y = 425,505
        else:
            self.x, self.y = 240,80
            self.ypos = True
        self.ballRect = pygame.Rect(self.x, self.y, self.d, self.d)
        return

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
    text = SMALLFONT.render('Type your gamertag and press RETURN', True, 'white', None)
    text_rect = text.get_rect(center=(WIDTH/2, 50))
    screen.blit(text, text_rect)
    text = SMALLFONT.render('Can not be more than 12 characters long', True, 'white', None)
    text_rect = text.get_rect(center=(WIDTH/2, 100))
    screen.blit(text, text_rect)
    text = SMALLFONT.render('Must be only numbers and letters', True, 'white', None)
    text_rect = text.get_rect(center=(WIDTH/2, 150))
    screen.blit(text, text_rect)
    text = SMALLFONT.render('Your gamertag is:', True, 'white', None)
    text_rect = text.get_rect(center=(WIDTH/2, 300))
    screen.blit(text, text_rect)
    pygame.display.flip()
    return

# function to get the gamertag
def get_gamertag():
    # shows pick gamertag screen and gets users gamertag
    display_gamertag()
    # start of gamertag selection code by setting all variables
    gamertag = ''
    key = 'null'
    while key != 'return':
        for event in pygame.event.get():
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
                # checks length is not over 12 characters
                elif key == 'return' or len(key) > 1 or not (key.isalpha() or key.isdigit()):
                    pass
                elif len(gamertag) >= 12:
                        text = SMALLFONT.render(('Must be less than 13'), True, 'white', None)
                        text_rect = text.get_rect(center=(WIDTH/2, 250))
                        screen.blit(text, text_rect)
                else:
                    # adds character to gamertag
                    gamertag += key
                    display_gamertag()
                    text = SMALLFONT.render((gamertag), True, 'white', None)
                    text_rect = text.get_rect(center=(WIDTH/2, 350))
                    screen.blit(text, text_rect)
                pygame.display.flip()

    con = sqlite3.connect("scores_database.db")
    cursor = con.cursor()
    cursor.execute("INSERT INTO scores (gamertag,score) VALUES(?,0)",(gamertag,)).fetchall()
    con.commit()
    con.close()
    return(gamertag)

# creates player and court selection screen
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
    # returns  the values back to the main progam
    return (bg, player)

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

# function to wait for user input
def wait_for_start():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key == 's':
                    waiting = False
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
    
    #sets inital values for locations and velocities
    user_player = Player(2,player,gamertag)
    comp_player = Computer(2,comp)
    ball = Ball(15,1.5,ball)

    game_over = False
    global server
    server = True
    reset = False

    # displays inital screen
    screen.blit(bg, (0, 0))
    ball.display()
    user_player.display()
    comp_player.display()
    u_points = str(user_player.getPoints())
    c_points = str(comp_player.getPoints())
    text = SMALLFONT.render('{}: {}'.format(gamertag,u_points[1:-1]), True, 'white', None)
    text_rect = text.get_rect(topleft = (5,5))
    screen.blit(text, text_rect)
    text = SMALLFONT.render('Computer: {}'.format(c_points[1:-1]), True, 'white', None)
    text_rect = text.get_rect(topleft = (5,30))
    screen.blit(text, text_rect)
    pygame.draw.rect(screen, 'white', pygame.Rect(3, 2, 250, 48),2)
    text = SMALLFONT.render('Press s to serve', True, 'white', None)
    text_rect = text.get_rect(center=(WIDTH/2, 300))
    screen.blit(text, text_rect)
    pygame.display.flip()
    wait_for_start()

    # loop to update the game until the game is over
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

        if reset:
            user_player.update(425, 525)
            comp_player.update(175, 75)
            ball.startPos(server)
            reset = False
            screen.blit(bg, (0, 0))
            ball.display()
            user_player.display()
            comp_player.display()
            ball.display()
            # shows score board 
            u_points = str(user_player.getPoints())
            c_points = str(comp_player.getPoints())
            text = SMALLFONT.render('{}: {}'.format(gamertag,u_points[1:-1]), True, 'white', None)
            text_rect = text.get_rect(topleft = (5,5))
            screen.blit(text, text_rect)
            text = SMALLFONT.render('Computer: {}'.format(c_points[1:-1]), True, 'white', None)
            text_rect = text.get_rect(topleft = (5,30))
            screen.blit(text, text_rect)
            pygame.draw.rect(screen, 'white', pygame.Rect(3, 2, 250, 48),2)
            pygame.display.flip()
            if server:
                wait_for_start()

        else:
            # checks if the ball is on the right of the player or not and flips the image if so 
            if ball.x > user_player.playerRect.midtop[0] and not user_player.flip:
                user_player.changeSide()
                user_player.flip = True
            # checks if the ball is on the left of the player and flips the image back
            elif ball.x < user_player.playerRect.midtop[0] and user_player.flip:
                user_player.changeSide()
                user_player.flip = False
            # repeats for the computers player
            if ball.x > comp_player.compRect.midtop[0] and not comp_player.flip:
                comp_player.changeSide()
                comp_player.flip = True
            elif ball.x < comp_player.compRect.midtop[0] and comp_player.flip:
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
        
            # checks who won the point and checks which scoring attribute needs updating and then updates it
            if ball.checkPos() == 'player':
                game_over = user_player.updateScore()
                if game_over:
                    game_over_screen(gamertag)
                else:
                    reset = True
            elif ball.checkPos() == 'computer':
                game_over = comp_player.updateScore()
                if game_over:
                    game_over_screen('computer')
                else:
                    reset = True

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
        pygame.draw.rect(screen, 'white', pygame.Rect(3, 2, 250, 48),2)
        pygame.display.flip()
             
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

# function to check how many trophys are earnt
def check_score(s):
    if s >= 80:
        return(16)
    elif s >= 70:
        return(15)
    elif s >= 60:
        return(14)
    elif s >= 50:
        return(13)
    elif s >= 45:
        return(12)
    elif s >= 40:
        return(11)
    elif s >= 35:
        return(10)
    elif s >= 30:
        return(9)
    elif s >= 25:
        return(8)
    elif s >= 20:
        return(7)
    elif s >= 15:
        return(6)
    elif s >= 10:
        return(5)
    elif s >= 5:
        return(4)
    elif s >= 4:
        return(3)
    elif s >= 2:
        return(2)
    elif s >= 1:
        return(1)
    else:
        return(0)
    
# function to show trophy menu
def show_trophies(gamertag):
    in_instruction = True
    while in_instruction:
        screen.fill('#00BF63')
        text = FONT.render('Trophies', True, 'white', None)
        text_rect = text.get_rect(center=(WIDTH/2, 50))
        screen.blit(text, text_rect)
        # open database and get score
        con = sqlite3.connect("scores_database.db")
        cursor = con.cursor()
        score = cursor.execute("SELECT score FROM scores WHERE gamertag = ?",(gamertag,)).fetchall()
        con.close()
        score = int(score[0][0])
        number = check_score(score)
        # display correct trophies
        count = 1
        y = 100
        for i in range (4):
            x = 50
            for j in range (4):
                if count <= number:
                    img = pygame.image.load('wtrophy.png')
                    img = pygame.transform.scale(img, (100, 100))
                    screen.blit(img, (x, y))
                else:
                    img = pygame.image.load('nwtrophy.png')
                    img = pygame.transform.scale(img, (100, 100))
                    screen.blit(img, (x, y))
                x += 150
                count += 1
            y += 130
        pygame.display.flip()
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
    gt = get_gamertag()
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
                    bg_pick, comp_pick = start_game()
                    play_game(bg_pick, comp_pick, gt)
                elif key == 'i':
                    show_instructions()
                elif key == 'l':
                    show_board()
                elif key == 't':
                    show_trophies(gt)
                elif key == 'escape':
                    show_menu()    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] > 150 and pos[0] < 450:
                    if pos[1] > 130 and pos[1] < 210:
                        bg_pick, comp_pick = start_game()
                        play_game(bg_pick, comp_pick, gt)
                    elif pos[1] > 250 and pos[1] < 330:
                        show_instructions()
                    elif pos[1] >370 and pos[1] < 450:
                        show_board()
                    elif pos[1] >490 and pos[1] < 570:
                        show_trophies(gt)      
        # update the display to show the changes
        pygame.display.flip()

##########################################################################main game loop###############################################################################################

# calls start up screen function
show_startup()
# calls show_menu function
show_menu()