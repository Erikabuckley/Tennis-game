# imported the modules needed for the game
import pygame
import sys
import sqlite3
import random

# imports the classes for the differnt objects
from ball import Ball
from player_type import User, Computer

# initialise pygame
pygame.init()
FONT = pygame.font.Font('Agrandir-GrandHeavy.otf', 40)
SMALLFONT = pygame.font.Font('Agrandir-GrandHeavy.otf', 16)
POINTS = (0, 15, 30, 40, 'deuce')
TROPHIES = [2, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 80]

########################################################################################## classes#######################################################################################


class Game:
    def __init__(self):
        # declared constants for the game
        self.width = self.height = 650
        self.courttop = 75
        self.courtbottom = 575
        self.courtleft = 174
        self.courtright = 471
        self.server = True
        # created the self.screen, its dimensions and caption and retreived the clock
        self.screen = pygame.display.set_mode([self.width, self.height])
        pygame.display.set_caption("Tennis game")
        self.clock = pygame.time.Clock()

    # displays the loading image then waits to look like game is loading
    def showStartup(self):
        start_screen = pygame.image.load('title.png')
        self.screen.blit(start_screen, (0, 0))
        pygame.display.flip()
        self.clock.tick(0.25)

    # displays the self.screen for the gamertag selection
    def displayGamertag(self):
        self.screen.fill('#00BF63')
        text = SMALLFONT.render(
            'Type your gamertag and press RETURN', True, 'white', None)
        text_rect = text.get_rect(center=(self.width/2, 50))
        self.screen.blit(text, text_rect)
        text = SMALLFONT.render(
            'Can not be more than 12 characters long', True, 'white', None)
        text_rect = text.get_rect(center=(self.width/2, 100))
        self.screen.blit(text, text_rect)
        text = SMALLFONT.render(
            'Must be only numbers and letters', True, 'white', None)
        text_rect = text.get_rect(center=(self.width/2, 150))
        self.screen.blit(text, text_rect)
        text = SMALLFONT.render('Your gamertag is:', True, 'white', None)
        text_rect = text.get_rect(center=(self.width/2, 300))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        return

    # function to get the gamertag
    def getGamertag(self):
        # shows pick gamertag self.screen and gets users gamertag
        self.displayGamertag()
        # start of gamertag selection code by setting all variables
        repeat = True
        gamertag = ''
        while repeat:
            for event in pygame.event.get():
                # checks for game quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)
                    # checks if user wants to return to the menu
                    if key == 'escape':
                        self.showMenu()
                    elif key == 'return' and len(gamertag) >= 1:
                        repeat = False
                    # checks if backspace is pressed if so will remove last character
                    elif key == 'backspace':
                        gamertag = gamertag[:-1]
                        self.displayGamertag()
                        text = SMALLFONT.render(
                            (gamertag), True, 'white', None)
                        text_rect = text.get_rect(center=(self.width/2, 350))
                        self.screen.blit(text, text_rect)
                    # checks length is not over 12 characters
                    elif len(key) > 1 or not (key.isalpha() or key.isdigit()):
                        pass
                    elif len(gamertag) >= 12:
                        text = SMALLFONT.render(
                            ('Must be less than 13'), True, 'white', None)
                        text_rect = text.get_rect(center=(self.width/2, 250))
                        self.screen.blit(text, text_rect)
                    else:
                        # adds character to gamertag
                        gamertag += key.lower()
                        self.displayGamertag()
                        text = SMALLFONT.render(
                            (gamertag), True, 'white', None)
                        text_rect = text.get_rect(center=(self.width/2, 350))
                        self.screen.blit(text, text_rect)
                    pygame.display.flip()

        con = sqlite3.connect("scores_database.db")
        cursor = con.cursor()
        gts = cursor.execute(
            "SELECT gamertag FROM scores WHERE gamertag = ?", (gamertag,)).fetchall()
        if gts == []:
            cursor.execute(
                "INSERT INTO scores (gamertag,score) VALUES(?,0)", (gamertag,)).fetchall()
        con.commit()
        con.close()
        return (gamertag)

    # creates player and court selection self.screen
    def startGame(self):
        self.screen.fill('#00BF63')
        text = FONT.render('What background?', True, 'white', None)
        text_rect = text.get_rect(center=(self.width/2, 50))
        self.screen.blit(text, text_rect)
        text = FONT.render('1, 2 or 3', True, 'white', None)
        text_rect = text.get_rect(center=(self.width/2, 400))
        self.screen.blit(text, text_rect)
        img = pygame.image.load('bgs.png')
        img = pygame.transform.scale(img, (400, 100))
        self.screen.blit(img, (120, 200))
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
                        self.showMenu()
                    elif key in ['1', '2', '3']:
                        bg = 'bg_'+key+'.png'

        # creates player selection self.screen
        self.screen.fill('#00BF63')
        text = FONT.render('Which player?', True, 'white', None)
        text_rect = text.get_rect(center=(self.width/2, 50))
        self.screen.blit(text, text_rect)
        text = FONT.render('1, 2 or 3', True, 'white', None)
        text_rect = text.get_rect(center=(self.width/2, 400))
        self.screen.blit(text, text_rect)
        img = pygame.image.load('players.png')
        img = pygame.transform.scale(img, (400, 100))
        self.screen.blit(img, (120, 200))
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
                        self.showMenu()
                    elif key in ['1', '2', '3']:
                        player = 'player_'+key+'.png'
        # returns  the values back to the main progam
        return (bg, player)

    # displays the game over self.screen, saves score then returns to the menu
    def gameOver(self, winner):
        self.screen.fill('#00BF63')
        text = FONT.render('Game over', True, 'white', None)
        text_rect = text.get_rect(center=(self.width/2, 200))
        self.screen.blit(text, text_rect)
        text = FONT.render('{} won!'.format(winner), True, 'white', None)
        text_rect = text.get_rect(center=(self.width/2, 400))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        if winner != 'Computer':
            con = sqlite3.connect("scores_database.db")
            cursor = con.cursor()
            newscore = cursor.execute(
                "SELECT score FROM scores WHERE gamertag = ?", (winner,)).fetchall()
            newscore = int(newscore[0][0]) + 1
            cursor.execute(
                "UPDATE scores SET score = ? WHERE gamertag = ?", (newscore, winner,))
            con.commit()
            con.close()
        self.clock.tick(0.25)
        self.showMenu()

    # displays the pause screen
    def pauseScreen(self):
        paused = True
        while paused:
            self.screen.fill('#00BF63')
            text = FONT.render('Press "p" to unpause', True, 'white', None)
            text_rect = text.get_rect(center=(self.width/2, 300))
            self.screen.blit(text, text_rect)
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
    def waitForStart(self):
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
    def playGame(self, bg, player):
        bg = pygame.image.load(bg)
        player = pygame.image.load(player)
        comp = pygame.image.load('player_{}.png'.format(random.randint(1, 4)))
        ball = pygame.image.load('ball.png')
        ball = pygame.transform.scale(ball, (15, 15))

        # sets inital values for locations and velocities
        user_player = User(2, player, self.screen, POINTS, self.server)
        comp_player = Computer(2, comp, self.screen, POINTS, self.server)
        ball = Ball(15, 3, ball, self.screen)

        # initialise variables
        game_over = False
        self.server = True
        reset = False
        serving = False

        # displays inital screen dimensions
        self.screen.blit(bg, (0, 0))
        ball.display()
        user_player.display()
        comp_player.display()
        u_points = str(user_player.getPoints())
        c_points = str(comp_player.getPoints())
        text = SMALLFONT.render('{}: {}'.format(
            GAMERTAG, u_points[1:-4]), True, 'white', None)
        text_rect = text.get_rect(topleft=(5, 5))
        self.screen.blit(text, text_rect)
        text = SMALLFONT.render('Computer: {}'.format(
            c_points[1:-4]), True, 'white', None)
        text_rect = text.get_rect(topleft=(5, 30))
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, 'white', pygame.Rect(3, 2, 250, 48), 2)
        text = SMALLFONT.render('Press s to serve', True, 'white', None)
        text_rect = text.get_rect(center=(self.width/2, 300))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        self.waitForStart()

        # loop to update the game until the game is over
        while not game_over:
            self.clock.tick(60)
            for event in pygame.event.get():
                # checks for game quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)
                    if key == 'p':
                        self.pauseScreen()

            # if its the start of a new point locations are reset
            if reset:
                user_player.update(425, 525)
                comp_player.update(175, 75)
                ball.startPos(self.server)
                reset = False
                self.screen.blit(bg, (0, 0))
                ball.display()
                user_player.display()
                comp_player.display()
                ball.display()
                # shows score board
                u_points = str(user_player.getPoints())
                c_points = str(comp_player.getPoints())
                text = SMALLFONT.render('{}: {}'.format(
                    GAMERTAG, u_points[1:-4]), True, 'white', None)
                text_rect = text.get_rect(topleft=(5, 5))
                self.screen.blit(text, text_rect)
                text = SMALLFONT.render('Computer: {}'.format(
                    c_points[1:-4]), True, 'white', None)
                text_rect = text.get_rect(topleft=(5, 30))
                self.screen.blit(text, text_rect)
                pygame.draw.rect(self.screen, 'white',
                                 pygame.Rect(3, 2, 250, 48), 2)
                pygame.display.flip()
                # serve to the left
                serving = True
                if self.server:
                    self.waitForStart()
                    ball.direction = 1
                    ball.ypos = False
                    ball.updatePos(True)
                else:
                    ball.direction = 3
                    ball.ypos = True

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
                if ball.x > comp_player.playerRect.midtop[0] and not comp_player.flip:
                    comp_player.changeSide()
                    comp_player.flip = True
                elif ball.x < comp_player.playerRect.midtop[0] and comp_player.flip:
                    comp_player.changeSide()
                    comp_player.flip = False

                # checks for collision between either player or computer and updates accordingly
                if ball.ballRect.colliderect(user_player.playerRect) or ball.ballRect.colliderect(comp_player.playerRect):
                    ball.direction = random.randint(1, 3)
                    ball.updatePos(True)
                    user_player.updatePos()
                    comp_player.updatePos(
                        ball.ballRect.centerx, ball.ballRect.centery, ball.v)
                else:
                    ball.updatePos(False)
                    user_player.updatePos()
                    comp_player.updatePos(ball.x, ball.y, ball.v)

                # checks who won the point and checks which scoring attribute needs updating and then updates it
                if ball.checkPos() == 'player':
                    p_won, s_won, g_won, game_over = user_player.updateScore()
                    if game_over:
                        self.gameOver(GAMERTAG)
                    else:
                        reset = True
                        if s_won:
                            user_player.p = 0
                            comp_player.p = 0
                            ball.v += 1
                        elif g_won:
                            user_player.p = 0
                            comp_player.p = 0
                            user_player.s = 0
                            comp_player.s = 0

                        if s_won or g_won:
                            self.server = not self.server

                elif ball.checkPos() == 'computer':
                    p_won, s_won, g_won, game_over = comp_player.updateScore()
                    if game_over:
                        self.gameOver('Computer')
                    else:
                        reset = True
                        if s_won:
                            user_player.p = 0
                            comp_player.p = 0
                            ball.v += 1

                        elif g_won:
                            user_player.p = 0
                            comp_player.p = 0
                            user_player.s = 0
                            comp_player.s = 0

                        if s_won or g_won:
                            self.server = not self.server

            # displays the changes
            self.screen.blit(bg, (0, 0))
            ball.display()
            user_player.display()
            comp_player.display()

            # shows score board
            u_points = str(user_player.getPoints())
            c_points = str(comp_player.getPoints())
            text = SMALLFONT.render('{}: {}'.format(
                GAMERTAG, u_points[1:-4]), True, 'white', None)
            text_rect = text.get_rect(topleft=(5, 5))
            self.screen.blit(text, text_rect)
            text = SMALLFONT.render('Computer: {}'.format(
                c_points[1:-4]), True, 'white', None)
            text_rect = text.get_rect(topleft=(5, 30))
            self.screen.blit(text, text_rect)
            pygame.draw.rect(self.screen, 'white',
                             pygame.Rect(3, 2, 250, 48), 2)
            pygame.display.flip()

    # function to show instruction screen
    def showInstructions(self):
        in_instruction = True
        while in_instruction:
            instructions = pygame.image.load('instructions.png')
            self.screen.blit(instructions, (0, 0))
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
                        self.showMenu()

    # function to show the leaderboard
    def showBoard(self):
        in_board = True
        while in_board:
            self.screen.fill('#00BF63')
            text = FONT.render('Leaderboard', True, 'white', None)
            text_rect = text.get_rect(center=(self.width/2, 50))
            self.screen.blit(text, text_rect)

            # gets top 10 names and scores then displays them
            con = sqlite3.connect("scores_database.db")
            cursor = con.cursor()
            gts = cursor.execute(
                "SELECT gamertag FROM scores ORDER BY score DESC").fetchall()
            scores = cursor.execute(
                "SELECT score FROM scores ORDER BY score DESC").fetchall()
            con.commit()
            con.close()
            for x in range(10):
                text = FONT.render(gts[x][0], True, 'white', None)
                text_rect = text.get_rect(topleft=(50, 100 + (55*x)))
                self.screen.blit(text, text_rect)
                text = FONT.render(str(scores[x][0]), True, 'white', None)
                text_rect = text.get_rect(topright=(600, 100 + (55*x)))
                self.screen.blit(text, text_rect)
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
                        self.showMenu()

    # function to check how many trophys are earnt
    def checkScore(self, score):
        number = 0
        for x in range(16):
            if score >= TROPHIES[x]:
                number += 1
        return (number)

    # function to show trophy menu
    def showTrophies(self):
        in_instruction = True
        while in_instruction:
            self.screen.fill('#00BF63')
            text = FONT.render('Trophies', True, 'white', None)
            text_rect = text.get_rect(center=(self.width/2, 50))
            self.screen.blit(text, text_rect)
            # opens database and get score
            con = sqlite3.connect("scores_database.db")
            cursor = con.cursor()
            score = cursor.execute(
                "SELECT score FROM scores WHERE gamertag = ?", (GAMERTAG,)).fetchall()
            con.close()
            score = int(score[0][0])
            number = self.checkScore(score)
            # display correct trophies
            count = 1
            y = 80
            for i in range(4):
                x = 50
                for j in range(4):
                    if count <= number:
                        img = pygame.image.load('wtrophy.png')
                    else:
                        img = pygame.image.load('nwtrophy.png')
                    img = pygame.transform.scale(img, (100, 100))
                    self.screen.blit(img, (x, y))
                    text = SMALLFONT.render('{} points'.format(
                        TROPHIES[count - 1]), True, 'white', None)
                    text_rect = text.get_rect(topleft=(x, y + 100))
                    self.screen.blit(text, text_rect)
                    x += 150
                    count += 1
                y += 150
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
                        self.showMenu()

    # displays menu screen
    def showMenu(self):
        menu = pygame.image.load('menu.png')
        self.screen.blit(menu, (0, 0))
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
                # checks if a key has been pressed and will go to correct self.screen if so
                elif event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)
                    if key == 's':
                        bg_pick, comp_pick = self.startGame()
                        self.playGame(bg_pick, comp_pick)
                    elif key == 'i':
                        self.showInstructions()
                    elif key == 'l':
                        self.showBoard()
                    elif key == 't':
                        self.showTrophies()
                    elif key == 'escape':
                        self.showMenu()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pos[0] > 150 and pos[0] < 450:
                        if pos[1] > 130 and pos[1] < 210:
                            bg_pick, comp_pick = self.startGame()
                            self.playGame(bg_pick, comp_pick)
                        elif pos[1] > 250 and pos[1] < 330:
                            self.showInstructions()
                        elif pos[1] > 370 and pos[1] < 450:
                            self.showBoard()
                        elif pos[1] > 490 and pos[1] < 570:
                            self.showTrophies()
            # update the display to show the changes
            pygame.display.flip()


################################################################################################### main game############################################################################
if __name__ == "__main__":
    game = Game()
    game.showStartup()
    GAMERTAG = game.getGamertag()
    # calls show_menu function
    game.showMenu()





                # while serving:
                #     ball.updatePos(False)
                #     user_player.updatePos()
                #     comp_player.updatePos(ball.ballRect.centerx,ball.ballRect.centery,ball.v)
                #     if ball.ballRect.colliderect(comp_player.playerRect) and self.server:
                #         serving = False
                #     elif ball.ballRect.colliderect(user_player.playerRect) and not self.server:
                #         serving = False