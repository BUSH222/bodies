import pygame
import math
import random
import os, sys
import time
import resource
v = "0.0.3"


pygame.init()

SCREENW = 1000
SCREENH = 800

display = pygame.display.set_mode((SCREENW, SCREENH)) #w, h
click = pygame.time.Clock()
FPS = 50
fun_mode = False

globaloffset = [0, 0]
density = 10000

settingsopen = False

threshold = 10
paused = False
focus = None

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
    global v
    font=pygame.font.Font(None,30)
    txt=font.render(v, 1,(255,255,255))
    txt.set_alpha(50)
    screen.blit(txt, (10, 10))

def displaydata(screen, *args):
    font=pygame.font.Font(None,20)
    for k in args:
        txt=font.render(k, 1,(255,255,255))
        screen.blit(txt, (10, 40 + args.index(k) * 20))

def display_settings(screen):
    global settingsopen, paused
    print('Settings menu opened')
    settingsopen = not settingsopen
    paused = True
    
    


class Ball():
    def __init__(self, x, y, xvel, yvel, mass, color):
        self.positionx = float(x)
        self.positiony = float(y)
        self.velocityx = float(xvel)
        self.velocityy = float(yvel)
        self.color = pygame.Color(color)
        self.velocity = self.velocityx, self.velocityy
        self.mass = mass
        self.radius = (3*(5*self.mass/density)/4*math.pi)**(1/2)
    
    def draw(self):
        pygame.draw.circle(display, self.color, (int(self.positionx + globaloffset[0]), int(self.positiony + globaloffset[1])), self.radius)

class Ship():
    def __init__(self, x, y, xvel, yvel):
        self.positionx = float(x)
        self.positiony = float(y)
        self.velocityx = float(xvel)
        self.velocityy = float(yvel)
        self.rotation = 0
        self.mass = 100000
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "ship.png"))
    
    def draw(self, surf):
        rotated_image = pygame.transform.rotate(self.image, self.rotation)
        new_rect = rotated_image.get_rect(center = self.image.get_rect(center = (self.positionx, self.positiony)).center)
        new_rect.move_ip(globaloffset[0], globaloffset[1])
        surf.blit(rotated_image, new_rect)


    
    

def game():
    global globaloffset, threshold, paused, focus
    #balls = [Ball(400, 500, 250, 0, 100000, "White"), Ball(400, 300, -250, 0, 100000, "Red"), Ball(500, 400, 0, -250, 100000, "Green"), Ball(300, 400, 0, 250, 100000, "Blue")]
    #balls = [Ball(400, 500, 0, 0, 100000, "White"), Ball(400, 300, 0, 0, 100000, "Green"), Ball(300, 400, 0, 0, 100000, "Red"), Ball(500, 400, 0, 0, 100000, "Yellow")]
    #balls = [Ball(400, 300, 200, 0, 100000, "White"), Ball(400, 400, 0, 0, 200000, "Red"), Ball(400, 500, -200, 0, 100000, "Green")]
    #balls = [Ball(400, 400, 0.5, 0, 100000, "White"), Ball(400, 100, -50, 0, 1000, "Green"), Ball(400, 700, 50, 0, 1000, "Yellow")]
    #balls = [Ball(500, 700, -400, 0, 10000, "Green"), Ball(500, 400, 4, 0, 1000000, "Yellow")] #solar system
    balls = []

    trails = []
    initialspos = (500, 400)
    s = Ship(initialspos[0], initialspos[1], 0, 0)

    for ball in balls:
        trails.append([[time.time(), ball, ball.color], []])
    
    
    
    while True:
        intercnt = 0
        tstart = time.time()
        display.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if 960 < pos[0] <= 1000 and 0 < pos[1] < 40:
                    display_settings(display)
                    newbdata = None
                newbdata = [pos[0], pos[1]]
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and newbdata is not None:
                pos = pygame.mouse.get_pos()
                nb = Ball(newbdata[0]-globaloffset[0], newbdata[1]-globaloffset[1], pos[0]-newbdata[0], pos[1]-newbdata[1], 100000, (0, 255, 0))
                balls.append(nb)
                trails.append([[time.time(), nb, nb.color], []])
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_BACKSPACE:
                    balls = []
                    trails = []
                    globaloffset = [0, 0]
                    focus = None
                    s = Ship(initialspos[0], initialspos[1], 0, 0)
                elif event.key == pygame.K_PERIOD and len(balls) > 0:
                    if focus is None:
                        focus = s
                    elif focus not in balls:
                        focus = balls[0]
                    else:
                        if balls.index(focus) + 1 < len(balls):
                            focus = balls[balls.index(focus) + 1]
                        else:
                            focus = s
                elif event.key == pygame.K_ESCAPE:
                    paused = not paused

        keyspressed = pygame.key.get_pressed()
        if keyspressed[pygame.K_UP]: 
            focus = None
            globaloffset[1] += 10
        if keyspressed[pygame.K_DOWN]: 
            focus = None
            globaloffset[1] += -10
        if keyspressed[pygame.K_LEFT]:
            focus = None
            globaloffset[0] += 10
        if keyspressed[pygame.K_RIGHT]:
            focus = None
            globaloffset[0] += -10
        if not paused:
            if keyspressed[pygame.K_w]: 
                s.velocityx += -math.sin(math.radians(s.rotation))*10
                s.velocityy += -math.cos(math.radians(s.rotation))*10
            if keyspressed[pygame.K_a]: 
                s.rotation += 3
                if s.rotation == 360:
                    s.rotation = 0
            if keyspressed[pygame.K_d]: 
                s.rotation -= 3
                if s.rotation == -360:
                    s.rotation = 0


        if focus is not None:
            globaloffset = [-focus.positionx+500, -focus.positiony+400]
        if not paused:
            for i1 in balls:
                for j1 in balls:
                    i, j = balls.index(i1), balls.index(j1)
                    if i < j and calculate_distance((i1.positionx, i1.positiony), (j1.positionx, j1.positiony)) <= 10000:
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
                        intercnt += 1



                acc = calculate_acceleration(i1.mass, s.mass, calculate_distance((i1.positionx, i1.positiony), (s.positionx, s.positiony)))
                if i1.positionx - 10 <= s.positionx <= i1.positionx + 10:
                    pass
                elif i1.positionx > s.positionx:
                    s.velocityx += acc[1] * calculate_fractions((i1.positionx, i1.positiony), (s.positionx, s.positiony))[0]
                
                else:
                    s.velocityx -= acc[1] * calculate_fractions((i1.positionx, i1.positiony), (s.positionx, s.positiony))[0]

                if i1.positiony - 10 <= s.positiony <= i1.positiony + 10:
                    pass
                elif i1.positiony > s.positiony:
                    s.velocityy += acc[1] * calculate_fractions((i1.positionx, i1.positiony), (s.positionx, s.positiony))[1]
                else:
                    s.velocityy -= acc[1] * calculate_fractions((i1.positionx, i1.positiony), (s.positionx, s.positiony))[1]
                



            for m1 in balls[:]:
                for n1 in balls[:]:
                    if m1 in balls and n1 in balls:
                        if balls.index(m1) < balls.index(n1):
                            if calculate_distance([m1.positionx, m1.positiony], [n1.positionx, n1.positiony]) <= (n1.radius + m1.radius):
                                v1 = m1.velocityx * m1.mass/(m1.mass + n1.mass) + n1.velocityx * n1.mass/(m1.mass + n1.mass)
                                v2 = m1.velocityy * m1.mass/(m1.mass + n1.mass) + n1.velocityy * n1.mass/(m1.mass + n1.mass)
                                bcolor = pygame.Color(((m1.color[0]+n1.color[0])/2, (m1.color[1]+n1.color[1])/2, (m1.color[2]+n1.color[2])/2))
                                newball = Ball((m1.positionx+n1.positionx)/2, (m1.positiony+n1.positiony)/2, v1, v2, m1.mass+n1.mass, bcolor)
                                if focus == n1 or focus == m1:
                                    focus = newball
                                balls.append(newball)
                                trails.append([[time.time(), newball, bcolor], []])
                                balls.remove(n1)
                                balls.remove(m1)
        
            for t in trails:
                if t[0][1] in balls:
                    t[1].append((t[0][1].positionx, t[0][1].positiony))
                if t[0][0] + threshold <= time.time():
                    if len(t[1]) > 1:
                        t[1] = t[1][1:]
                    else:
                        trails.remove(t)


            s.positionx += round(s.velocityx/100, 8)
            s.positiony += round(s.velocityy/100, 8)

        tcalc2 = time.time()
        ###Displaying Objects
        trender1 = time.time()

        

        for t in trails:
            for o in t[1]:
                pygame.draw.circle(display, t[0][2], (o[0] + globaloffset[0], o[1] + globaloffset[1]), 1)
        
        for b in balls[:]:
            if len(balls) >= 50 and (not fun_mode):
                if b.positionx > 2000 or b.positionx < -1200 or b.positiony > 2000 or b.positiony < -1200:
                    balls.remove(b)
                    continue
            if not paused:
                b.positionx += round(b.velocityx/100, 8)
                b.positiony += round(b.velocityy/100, 8)
            if b.positionx - 600 <= -globaloffset[0]+500 <= b.positionx + 600 and b.positiony - 500 <= -globaloffset[1]+400 <= b.positiony + 500:
                b.draw()
        


        if s.positionx - 600 <= -globaloffset[0]+500 <= s.positionx + 600 and s.positiony - 500 <= -globaloffset[1]+400 <= s.positiony + 500:
            #s.draw(display)
            pass
            

        
        
        
        credits(display)

        img = pygame.image.load(os.path.join(os.path.dirname(__file__), "settings.png"))
        display.blit(img, (968, 0))
        trender2 = time.time()
        displaydata(display, f"Coords: {int(globaloffset[0])}, {int(globaloffset[1])}", f'Objects: {len(balls)}', f'FPS: {round(click.get_fps())}',
            f'Calculation time: {round((tcalc2-tstart)*1000, 1)} ms', f'Rendering time: {round((trender2-trender1)*1000, 1)} ms', f'Interactions: {intercnt}', f'Peak memory usage: {round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/2**20, 2)}MB')
            
        if settingsopen:
            rect = (0, 0, 1000, 800)
            shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
            pygame.draw.rect(shape_surf, (0, 0, 0, 127), shape_surf.get_rect())
            display.blit(shape_surf, rect)
        pygame.display.update()
        if fun_mode:
            balls.append(Ball(random.randint(-10000, 10000), random.randint(-10000, 10000), 0, 0, 100000, (66, 245, 170)))
        click.tick(FPS)

if __name__ == "__main__":
    game()
    pygame.quit()