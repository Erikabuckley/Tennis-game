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

# created the screen, its dimensions and caption and retreived the clock
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Tennis game")
clock = pygame.time.Clock()


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

# function to update players location acccording to user input
def update_player(x, y, v):
    img_width = 50
    img_height = 100
    for event in pygame.event.get():
        # checks if user pressed exit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # checks the key that has been presed and returns new x and y values
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > 0:
        x -= v
    elif keys[pygame.K_RIGHT] and x < (WIDTH - img_width):
        x += v
    elif keys[pygame.K_UP] and y > 325:
        y -= v
    elif keys[pygame.K_DOWN] and y < (HEIGHT - img_height):
        y += v
    return (x, y)

# function to update the computers location
def update_computer(x, y, v):
    img_width = 50
    img_height = 100
    for event in pygame.event.get():
        # checks if user pressed exit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # moves according to the user but will need to be updated with ai once ball has been created and moves
    if x < 550:
        x+=2*v
    return (x, y)

# function to move ball
def move_ball(x, y, v):
    x +=1
    y += 1
    return(x, y)

# function to check th side that the ball is on of the player
def check_side(x, ballx,img):
    if x > ballx:
        img = pygame.transform.flip(img,True,False)
        return(img,True)
    else:
        return(img,False)
def check_score():
     
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
    #sets inital values for locations and speeds
    x = 450
    y = 450
    cx = 50
    cy = 50
    bx = 50
    by = 40
    velocity = 1
    bvelocity = 2
    clock.tick(60)
    # displays players starting locations
    screen.blit(bg, (0, 0))
    screen.blit(player, (x, y))
    screen.blit(comp, (cx, cy))
    screen.blit(ball, (bx, by))
    pygame.display.flip()
    # loop to update the locations by calling the functions
    game_over = False
    pflipped = False
    cflipped = False
    while not game_over:
        x, y = update_player(x, y, velocity)
        cx, cy = update_computer(cx, cy, velocity)
        bx, by = move_ball(bx, by, bvelocity)
        player,pflipped = check_side(x,bx,player)
        comp,cflipped = check_side(cx,bx,comp)

        # displays the changes
        screen.blit(bg, (0, 0))
        screen.blit(player, (x, y))
        screen.blit(comp, (cx, cy))
        screen.blit(ball, (bx, by))
        pygame.display.flip()
        game_over = check_score()
    
    ####################################################
    # changes to game over screen
    screen.fill('#00BF63')
    text = FONT.render('Game over', True, 'white', None)
    text_rect = text.get_rect(center=(WIDTH/2, 300))
    screen.blit(text, text_rect)
    pygame.display.flip()
    show_menu()
    #''''''''''''''''''''''''''''''''''''''''''''''''''#'''

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
                    bg_pick, player_pick, gamertag = start_game()
                    play_game(bg_pick, player_pick, gamertag)
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