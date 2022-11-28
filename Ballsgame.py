import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 120
screen = pygame.display.set_mode((1200, 900)) #creating game console
font_style = pygame.font.SysFont(None, 50)  # creating style of fonts
font_style_start = pygame.font.SysFont(None, 100)
font_style_finish = pygame.font.SysFont(None, 150)

RED = (255, 0, 0) #initiating colors
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN] #creating colors array

def new_ball():
    '''
    Creating new ball
    Randomly choosing coordinate on x-axes and y-axes
    r (radius of the ball), color (color of the ball). Returning list of the parameters
    '''
    x = randint(100, 700)
    y = randint(100, 500)
    r = randint(30, 50)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)
    parameters = [x, y, r, color]
    return parameters

def new_color_ball():
    '''
    Creating new color ball
    Randomly choosing coordinate on x-axes and y-axes
    r (radius of the ball), color (color of the ball). Returning list of the parameters
    '''
    x = randint(100, 700)
    y = randint(100, 500)
    r = randint(30, 50)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)
    parameterrs = [x, y, r, color]
    return parameterrs

def color_ball(parameterrs):
    '''
    Draw a color ball
    parameters[0] - coordinate on x-axis
    parameters[1] - coordinate on y-axis
    parameters[2] - radius of the ball
    parameters[3] - color of the ball
    '''
    x = parameterrs[0]
    y = parameterrs[1]
    r = parameterrs[2]
    circle(screen, COLORS[randint(0, 5)], (x, y), r)

def ball(parameters):
    '''
    Draw a ball
    parameters[0] - coordinate on x-axis
    parameters[1] - coordinate on y-axis
    parameters[2] - radius of the ball
    parameters[3] - color of the ball
    '''
    x = parameters[0]
    y = parameters[1]
    r = parameters[2]
    color = parameters[3]
    circle(screen, color, (x, y), r)

def speed():
    '''speed on the x-axis and y-axis'''
    x_speed = randint(-500, 500) / 100
    y_speed = randint(-500, 500) / 100
    return [x_speed, y_speed]

def score_message(msg, color):
    '''Current player rate on the screen'''
    mesg = font_style.render("Score: " + str(msg), True, color)
    screen.blit(mesg, [1000, 70])

def error_message(msg, color):
    '''Current count of errors on the screen'''
    mesg = font_style.render("Errors: " + str(msg), True, color)
    screen.blit(mesg, [1000, 120])

def win_message(color):
    '''Output winning message on the screen'''
    mesg = font_style_finish.render("YOU WIN!", True, color)
    screen.blit(mesg, [300, 400])

def lose_message(color):
    '''Output losing message on the screen'''
    mesg = font_style_finish.render("YOU LOSE!", True, color)
    screen.blit(mesg, [300, 400])

pygame.display.update()
clock = pygame.time.Clock() #Install clock
score = 0  # Starting count
score2 = 0 #backup of starting count
error_num = 0 #starting count
number_of_balls = 3
number_of_color_balls = 4
parameters_balls = []  #parameters of balls
speed_list_balls = []  #List of balls' speed
parameters_color_balls = []  #parameters color of balls
speed_list_color_balls = []  #List of color balls' speed
for _ in range(number_of_color_balls):  #fill list of color balls' speed and parameters
    parameters_color_balls.append(new_color_ball())
    speed_list_color_balls.append(speed())
for _ in range(number_of_balls):  # fill list of balls' speed and parameters
    parameters_balls.append(new_ball())
    speed_list_balls.append(speed())
finished = False
while not finished:
    clock.tick(FPS)
    screen.fill(BLACK)
    for num_of_ball in range(number_of_balls): #changing balls' speed
        parameters_balls[num_of_ball][0] += speed_list_balls[num_of_ball][0]
        parameters_balls[num_of_ball][1] += speed_list_balls[num_of_ball][1]
        if parameters_balls[num_of_ball][0] + parameters_balls[num_of_ball][2] >= 1200 or \
                parameters_balls[num_of_ball][0] - parameters_balls[num_of_ball][2] <= 0:
            speed_list_balls[num_of_ball][0] = -speed_list_balls[num_of_ball][0]
        if parameters_balls[num_of_ball][1] + parameters_balls[num_of_ball][2] >= 900 or \
                parameters_balls[num_of_ball][1] - parameters_balls[num_of_ball][2] <= 0:
            speed_list_balls[num_of_ball][1] = -speed_list_balls[num_of_ball][1]
    for num_of_ball in range(number_of_color_balls): #changing  color balls' speed
        parameters_color_balls[num_of_ball][0] += speed_list_color_balls[num_of_ball][0]
        parameters_color_balls[num_of_ball][1] += speed_list_color_balls[num_of_ball][1]
        if parameters_color_balls[num_of_ball][0] + parameters_color_balls[num_of_ball][2] >= 1200 or \
                parameters_color_balls[num_of_ball][0] - parameters_color_balls[num_of_ball][2] <= 0:
            parameters_color_balls[num_of_ball] = new_color_ball()
            speed_list_color_balls[num_of_ball] = speed()
        if parameters_color_balls[num_of_ball][1] + parameters_color_balls[num_of_ball][2] >= 900 or \
                parameters_color_balls[num_of_ball][1] - parameters_color_balls[num_of_ball][2] <= 0:
            parameters_color_balls[num_of_ball] = new_color_ball()
            speed_list_color_balls[num_of_ball] = speed()
    for num_of_ball in range(len(parameters_balls)):  #Drawing new balls' positions
        ball(parameters_balls[num_of_ball])
    for num_of_ball in range(len(parameters_color_balls)):  #Drawing new color balls' positions
        color_ball(parameters_color_balls[num_of_ball])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            score2 = score
            for num_of_ball, position in enumerate(parameters_balls):
                if (event.pos[0] - position[0]) ** 2 + (event.pos[1] - position[1]) ** 2 <= position[2] ** 2:
                    score += 1  # If mouse click fitting in the ball area, score of the player is raising
                    parameters_balls[num_of_ball] = new_ball()
                    speed_list_balls[num_of_ball] = speed()
            for num_of_ball, position in enumerate(parameters_color_balls):
                if (event.pos[0] - position[0]) ** 2 + (event.pos[1] - position[1]) ** 2 <= position[2] ** 2:
                    score += 3  # If mouse click fitting in the ball area, score of the player is raising
                    parameters_color_balls[num_of_ball] = new_color_ball()
                    speed_list_color_balls[num_of_ball] = speed()
            if score == score2: # If not, error number is raising
                error_num += 1
                if error_num >= 5: #If error number reach limit you lose the game
                    lose_message(GREEN)
                    finished = True
    score_message(str(score), MAGENTA)  # show score on the screen
    error_message(str(error_num), MAGENTA)  # show number of errors on the screen
    pygame.display.update()
    screen.fill(BLACK)
print('Final count', score)
pygame.quit()

