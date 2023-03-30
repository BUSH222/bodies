import pygame
pygame.init()

display = pygame.display.set_mode((1000, 1000)) #w, h
click = pygame.time.Clock()
FPS = 50


def game():
    while True:
        display.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
    
        pygame.display.update()
        click.tick(FPS)
game()
pygame.quit()