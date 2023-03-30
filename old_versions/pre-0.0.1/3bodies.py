import pygame
import math
import random
pygame.init()

display = pygame.display.set_mode((800, 800)) #w, h
click = pygame.time.Clock()
FPS = 50

def calculate_acceleration(m1, m2, sep):
    Fg = ((6.67 * (10 ** -11)) * (m1 * 100000) * (m2 * 100000))/((sep)**2)
    aform1 = Fg/m1
    aform2 = Fg/m2
    return [aform1, aform2]

def calculate_distance(x, y):
    xd = abs(x[0]-y[0])
    yd = abs(x[1]-y[1])
    r = math.sqrt(xd**2 + yd ** 2)
    return r

def calculate_fractions(p1, p2):
    #ac = F * AC/(BC+AC)
    ac = abs(p1[0] - p2[0])
    bc = abs(p1[1] - p2[1])
    forx = ac/(bc+ac)
    fory = bc/(bc+ac)
    return [forx, fory]
    


class Ball():
    def __init__(self, x, y, xvel, yvel, mass, color):
        self.positionx = float(x)
        self.positiony = float(y)
        self.velocityx = float(xvel)
        self.velocityy = float(yvel)
        self.color = pygame.Color(color)
        self.velocity = self.velocityx, self.velocityy
        self.mass = mass
    
    def draw(self):
        pygame.draw.circle(display, self.color, (int(self.positionx), int(self.positiony)), 10)

def game():
    dotpos = []
    dotpos2 = []
    dotpos3 = []
    ball1 = Ball(400, 300, 200, 0, 100000, "White") #edit values here (positionx, positiony, velocityx, velocityy, mass, color)
    ball2 = Ball(400, 400, 0, -0.1, 200000, "Red")
    ball3 = Ball(400, 500, -200, 0, 100000, "Green")
    threshold = 1000 #amount of dots showing the orbit per body (1+)
    #ball1 = Ball(random.randint(100, 500), random.randint(100, 500), random.randint(-200, 200), random.randint(-200, 200), random.randint(100000, 1000000), "White")
    #ball2 = Ball(random.randint(100, 500), random.randint(100, 500), random.randint(-200, 200), random.randint(-200, 200), random.randint(100000, 1000000), "Red")
    #ball3 = Ball(random.randint(100, 500), random.randint(100, 500), random.randint(-200, 200), random.randint(-200, 200), random.randint(100000, 1000000), "Green")
    
    while True:
        x, y = pygame.mouse.get_pos()
        display.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
        

        acc = calculate_acceleration(ball1.mass, ball2.mass, calculate_distance((ball1.positionx, ball1.positiony), (ball2.positionx, ball2.positiony)))
        if ball1.positionx > ball2.positionx:
            ball1.velocityx -= acc[0] * calculate_fractions((ball1.positionx, ball1.positiony), (ball2.positionx, ball2.positiony))[0]
            ball2.velocityx += acc[1] * calculate_fractions((ball1.positionx, ball1.positiony), (ball2.positionx, ball2.positiony))[0]
        elif ball1.positionx == ball2.positionx:
            pass
        else:
            ball1.velocityx += acc[0] * calculate_fractions((ball1.positionx, ball1.positiony), (ball2.positionx, ball2.positiony))[0]
            ball2.velocityx -= acc[1] * calculate_fractions((ball1.positionx, ball1.positiony), (ball2.positionx, ball2.positiony))[0]
        
        if ball1.positiony > ball2.positiony:
            ball1.velocityy -= acc[0] * calculate_fractions((ball1.positionx, ball1.positiony), (ball2.positionx, ball2.positiony))[1]
            ball2.velocityy += acc[1] * calculate_fractions((ball1.positionx, ball1.positiony), (ball2.positionx, ball2.positiony))[1]
        elif ball1.positiony == ball2.positiony:
            pass
        else:
            ball1.velocityy += acc[0] * calculate_fractions((ball1.positionx, ball1.positiony), (ball2.positionx, ball2.positiony))[1]
            ball2.velocityy -= acc[1] * calculate_fractions((ball1.positionx, ball1.positiony), (ball2.positionx, ball2.positiony))[1]

        ##
        acc2 = calculate_acceleration(ball3.mass, ball2.mass, calculate_distance((ball3.positionx, ball3.positiony), (ball2.positionx, ball2.positiony)))
        if ball3.positionx > ball2.positionx:
            ball3.velocityx -= acc2[0] * calculate_fractions((ball3.positionx, ball3.positiony), (ball2.positionx, ball2.positiony))[0]
            ball2.velocityx += acc2[1] * calculate_fractions((ball3.positionx, ball3.positiony), (ball2.positionx, ball2.positiony))[0]
        elif ball3.positionx == ball2.positionx:
            pass
        else:
            ball3.velocityx += acc2[0] * calculate_fractions((ball3.positionx, ball3.positiony), (ball2.positionx, ball2.positiony))[0]
            ball2.velocityx -= acc2[1] * calculate_fractions((ball3.positionx, ball3.positiony), (ball2.positionx, ball2.positiony))[0]
        
        if ball3.positiony > ball2.positiony:
            ball3.velocityy -= acc2[0] * calculate_fractions((ball3.positionx, ball3.positiony), (ball2.positionx, ball2.positiony))[1]
            ball2.velocityy += acc2[1] * calculate_fractions((ball3.positionx, ball3.positiony), (ball2.positionx, ball2.positiony))[1]
        elif ball3.positiony == ball2.positiony:
            pass
        else:
            ball3.velocityy += acc2[0] * calculate_fractions((ball3.positionx, ball3.positiony), (ball2.positionx, ball2.positiony))[1]
            ball2.velocityy -= acc2[1] * calculate_fractions((ball3.positionx, ball3.positiony), (ball2.positionx, ball2.positiony))[1]
        ##
        acc3 = calculate_acceleration(ball1.mass, ball3.mass, calculate_distance((ball1.positionx, ball1.positiony), (ball3.positionx, ball3.positiony)))
        if ball1.positionx > ball3.positionx:
            ball1.velocityx -= acc3[0] * calculate_fractions((ball1.positionx, ball1.positiony), (ball3.positionx, ball3.positiony))[0]
            ball3.velocityx += acc3[1] * calculate_fractions((ball1.positionx, ball1.positiony), (ball3.positionx, ball3.positiony))[0]
        elif ball1.positionx == ball3.positionx:
            pass
        else:
            ball1.velocityx += acc3[0] * calculate_fractions((ball1.positionx, ball1.positiony), (ball3.positionx, ball3.positiony))[0]
            ball3.velocityx -= acc3[1] * calculate_fractions((ball1.positionx, ball1.positiony), (ball3.positionx, ball3.positiony))[0]
        
        if ball1.positiony > ball3.positiony:
            ball1.velocityy -= acc3[0] * calculate_fractions((ball1.positionx, ball1.positiony), (ball3.positionx, ball3.positiony))[1]
            ball3.velocityy += acc3[1] * calculate_fractions((ball1.positionx, ball1.positiony), (ball3.positionx, ball3.positiony))[1]
        elif ball1.positiony == ball3.positiony:
            pass
        else:
            ball1.velocityy += acc3[0] * calculate_fractions((ball1.positionx, ball1.positiony), (ball3.positionx, ball3.positiony))[1]
            ball3.velocityy -= acc3[1] * calculate_fractions((ball1.positionx, ball1.positiony), (ball3.positionx, ball3.positiony))[1]
        #movement
        ball1.positionx += ball1.velocityx/50
        ball2.positionx += ball2.velocityx/50
        ball3.positionx += ball3.velocityx/50
        ball1.positiony += ball1.velocityy/50
        ball2.positiony += ball2.velocityy/50
        ball3.positiony += ball3.velocityy/50

        ball1.draw()
        ball2.draw()
        ball3.draw()

        
        
        if len(dotpos) >= threshold:
            del dotpos[0]
        if len(dotpos2) >= threshold:
            del dotpos2[0]
        if len(dotpos3) >= threshold:
            del dotpos3[0]
        
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