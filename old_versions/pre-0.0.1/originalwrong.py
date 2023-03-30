import pygame
import math
pygame.init()

display = pygame.display.set_mode((1000, 1000)) #w, h
click = pygame.time.Clock()
FPS = 50

def calculate_acceleration(m1, m2, sep):
    Fg = ((6.67 * (10 ** -11)) * (m1 * 100000) * (m2 * 100000))/((sep)**2)
    aform1 = Fg/m1
    aform2 = Fg/m2
    return [aform1, aform2]

def calculate_distance(x, y):
    xd = abs(x[0]-x[1])
    yd = abs(y[0]-y[1])
    r = math.sqrt(xd**2 + yd ** 2)
    return r



class Ball():
    def __init__(self, x, y, xvel, yvel, mass, color):
        self.position = x, y
        self.positionx = float(x)
        self.positiony = float(y)
        self.velocity = xvel, yvel
        self.velocityx = float(xvel)
        self.velocityy = float(yvel)
        self.color = pygame.Color(color)
        self.mass = mass
    
    def draw(self):
        pygame.draw.circle(display, self.color, (int(self.positionx), int(self.positiony)), 10)

def game():
    dotpos = []
    dotpos2 = []
    dotpos3 = []
    ball1 = Ball(200, 201, 0, 0, 10000, "White") #1000000
    ball2 = Ball(300, 400, 0, 0, 10000, "Red")
    ball3 = Ball(500, 200, 0, 0, 10000, "Green")
    while True:
        display.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
        
        

        acc = calculate_acceleration(ball1.mass, ball2.mass, calculate_distance(ball1.position, ball2.position))
        if ball1.positionx > ball2.positionx:
            ball1.velocityx -= acc[0]
            ball2.velocityx += acc[1]
        elif ball1.positionx == ball2.positionx:
            pass
        else:
            ball1.velocityx += acc[0]
            ball2.velocityx -= acc[1]
        
        if ball1.positiony > ball2.positiony:
            ball1.velocityy -= acc[0]
            ball2.velocityy += acc[1]
        elif ball1.positiony == ball2.positiony:
            pass
        else:
            ball1.velocityy += acc[0]
            ball2.velocityy -= acc[1]
        ###
        acc2 = calculate_acceleration(ball2.mass, ball3.mass, calculate_distance(ball2.position, ball3.position))
        if ball2.positionx > ball3.positionx:
            ball2.velocityx -= acc[0]
            ball3.velocityx += acc[1]
        elif ball2.positionx == ball3.positionx:
            pass
        else:
            ball2.velocityx += acc[0]
            ball3.velocityx -= acc[1]
        
        if ball2.positiony > ball3.positiony:
            ball2.velocityy -= acc[0]
            ball3.velocityy += acc[1]
        elif ball2.positiony == ball3.positiony:
            pass
        else:
            ball2.velocityy += acc[0]
            ball3.velocityy -= acc[1]
        ##
        acc3 = calculate_acceleration(ball1.mass, ball3.mass, calculate_distance(ball1.position, ball3.position))
        if ball2.positionx > ball3.positionx:
            ball1.velocityx -= acc[0]
            ball3.velocityx += acc[1]
        elif ball1.positionx == ball3.positionx:
            pass
        else:
            ball1.velocityx += acc[0]
            ball3.velocityx -= acc[1]
        
        if ball1.positiony > ball3.positiony:
            ball1.velocityy -= acc[0]
            ball3.velocityy += acc[1]
        elif ball1.positiony == ball3.positiony:
            pass
        else:
            ball1.velocityy += acc[0]
            ball3.velocityy -= acc[1]
        
        #movement
        ball1.positionx += ball1.velocityx/50
        ball2.positionx += ball2.velocityx/50
        ball1.positiony += ball1.velocityy/50
        ball2.positiony += ball2.velocityy/50
        ##
        ball2.positionx += ball2.velocityx/50
        ball3.positionx += ball3.velocityx/50
        ball2.positiony += ball2.velocityy/50
        ball3.positiony += ball3.velocityy/50

        ball1.positionx += ball1.velocityx/50
        ball3.positionx += ball3.velocityx/50
        ball1.positiony += ball1.velocityy/50
        ball3.positiony += ball3.velocityy/50


        ball1.draw()
        ball2.draw()
        ball3.draw()

        dotpos.append((ball1.positionx, ball1.positiony))
        for dots in dotpos:
            pygame.draw.circle(display, pygame.Color("White"), dots, 1)
        
        dotpos2.append((ball2.positionx, ball2.positiony))
        for dots in dotpos2:
            pygame.draw.circle(display, pygame.Color("Red"), dots, 1)

        dotpos3.append((ball3.positionx, ball3.positiony))
        for dots in dotpos3:
            pygame.draw.circle(display, pygame.Color("Green"), dots, 1)

        
        pygame.display.update()
        click.tick(FPS)
game()
pygame.quit()