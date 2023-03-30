import pygame
import math
import random
import itertools

v = "0.0.1"


pygame.init()

display = pygame.display.set_mode((800, 800)) #w, h
click = pygame.time.Clock()
FPS = 100

def calculate_acceleration(m1, m2, sep):
    if sep == 0:
        return [0, 0]
    Fg = ((6.67 * (10 ** -11)) * ((m1 * 100000) * (m2 * 100000))/((sep)**2))
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
    return [round(forx, 10), round(fory, 10)]

def credits(screen):
    font=pygame.font.Font(None,30)
    txt=font.render("Alpha 0.0.1", 1,(255,255,255))
    txt.set_alpha(50)
    screen.blit(txt, (10, 10))

class Ball():
    def __init__(self, x, y, xvel, yvel, mass, color):
        self.positionx = float(x)
        self.positiony = float(y)
        self.velocityx = float(xvel)
        self.velocityy = float(yvel)
        self.color = pygame.Color(color)
        self.velocity = self.velocityx, self.velocityy
        self.mass = mass
        self.radius = 10
        self.dotpos = []
    
    def draw(self):
        pygame.draw.circle(display, self.color, (int(self.positionx), int(self.positiony)), self.radius)

def game():
    #balls = [Ball(400, 500, 200, 0, 100000, "White"), Ball(400, 300, -200, 0, 100000, "Red"), Ball(500, 400, 0, -200, 100000, "Green"), Ball(300, 400, 0, 200, 100000, "Blue")]
    #balls = [Ball(400, 500, 0, 0, 100000, "White"), Ball(400, 300, 0, 0, 100000, "Green"), Ball(300, 400, 0, 0, 100000, "Red"), Ball(500, 400, 10, 0, 100000, "Yellow")]
    #balls = [Ball(400, 300, 200, 0, 100000, "White"), Ball(400, 400, 0, -0.1, 200000, "Red"), Ball(400, 500, -200, 0, 100000, "Green")]
    #balls = [Ball(400, 400, 0.5, 0, 100000, "White"), Ball(400, 100, -50, 0, 1000, "Green"), Ball(400, 700, 50, 0, 1000, "Yellow")]
    balls = []
    threshold = 1000
    paused = False

    newbdata = []
    
    while True:
        

        display.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                newbdata = [pos[0], pos[1]]
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                balls.append(Ball(newbdata[0], newbdata[1], pos[0]-newbdata[0], pos[1]-newbdata[1], 100000, (0, 255, 0)))
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_BACKSPACE:
                    balls = []

        
        
        for i1 in balls:
            for j1 in balls:
                i, j = balls.index(i1), balls.index(j1)
                if i < j:
                    acc = calculate_acceleration(i1.mass, j1.mass, calculate_distance((i1.positionx, i1.positiony), (j1.positionx, j1.positiony)))
                    if i1.positionx > j1.positionx:
                        i1.velocityx -= acc[0] * calculate_fractions((i1.positionx, i1.positiony), (j1.positionx, j1.positiony))[0]
                        j1.velocityx += acc[1] * calculate_fractions((i1.positionx, i1.positiony), (j1.positionx, j1.positiony))[0]
                    elif i1.positionx == j1.positionx:
                        pass
                    else:
                        i1.velocityx += acc[0] * calculate_fractions((i1.positionx, i1.positiony), (j1.positionx, j1.positiony))[0]
                        j1.velocityx -= acc[1] * calculate_fractions((i1.positionx, i1.positiony), (j1.positionx, j1.positiony))[0]
                    if i1.positiony > j1.positiony:
                        i1.velocityy -= acc[0] * calculate_fractions((i1.positionx, i1.positiony), (j1.positionx, j1.positiony))[1]
                        j1.velocityy += acc[1] * calculate_fractions((i1.positionx, i1.positiony), (j1.positionx, j1.positiony))[1]
                    elif i1.positiony == j1.positiony:
                        pass
                    else:
                        i1.velocityy += acc[0] * calculate_fractions((i1.positionx, i1.positiony), (j1.positionx, j1.positiony))[1]
                        j1.velocityy -= acc[1] * calculate_fractions((i1.positionx, i1.positiony), (j1.positionx, j1.positiony))[1]
                
                    
        for m1 in balls[:]:
            for n1 in balls[:]:
                if m1 in balls and n1 in balls:
                    if balls.index(m1) < balls.index(n1):
                        if calculate_distance([m1.positionx, m1.positiony], [n1.positionx, n1.positiony]) <= (n1.radius + m1.radius):
                            v1 = m1.velocityx * m1.mass/(m1.mass + n1.mass) + n1.velocityx * n1.mass/(m1.mass + n1.mass)
                            v2 = m1.velocityy * m1.mass/(m1.mass + n1.mass) + n1.velocityy * n1.mass/(m1.mass + n1.mass)
                            bcolor = pygame.Color(((m1.color[0]+n1.color[0])/2, (m1.color[1]+n1.color[1])/2, (m1.color[2]+n1.color[2])/2))
                            newball = Ball((m1.positionx+n1.positionx)/2, (m1.positiony+n1.positiony)/2, v1, v2, m1.mass+n1.mass, bcolor)
                            newball.radius = n1.radius+m1.radius-5
                            balls.append(newball)
                            balls.remove(n1)
                            balls.remove(m1)
        


        for b in balls[:]:
            if b.positionx > 2000 or b.positionx < -1200 or b.positiony > 2000 or b.positiony < -1200:
                balls.remove(b)
                continue
            b.positionx += round(b.velocityx/100, 8)
            b.positiony += round(b.velocityy/100, 8)
            b.draw()
        
        for k in balls:
            if len(k.dotpos) >= threshold:
                k.dotpos = k.dotpos[2:]
        
            k.dotpos.append((k.positionx, k.positiony))
            for dots in k.dotpos:
                pygame.draw.circle(display, pygame.Color(k.color), dots, 1)
        
        #balls.append(Ball(random.randint(100, 700), random.randint(100, 700), 0, 0, 100000, (66, 245, 170)))
        credits(display)
        pygame.display.update()
        click.tick(FPS)
if __name__ == "__main__":
    game()
    pygame.quit()