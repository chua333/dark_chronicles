import os
import pygame
os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the window on the screen

from pygame.locals import *


class GameState():
    def __init__(self):
        self.x = 120
        self.y = 120

    def update(self, moveCommandX, moveCommandY):
        self.x += moveCommandX
        self.y += moveCommandY


class UserInterface:
    def __init__(self):
        pygame.init()
        self.running = True
        self.window = pygame.display.set_mode((640, 600), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.size = self.width, self.height = 640, 600
        self.gameState = GameState()
        self.clock = pygame.time.Clock()
        self.moveCommandX = 0
        self.moveCommandY = 0

        self.iconImage = pygame.image.load("F_sWcSIbQAAog2U.png")
        self.captionName = "Simple Pygame App"
        pygame.display.set_caption(self.captionName)
        pygame.display.set_icon(self.iconImage)

    def processInput(self):
        self.moveCommandX = 0
        self.moveCommandY = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    break
                elif event.key == K_RIGHT or event.key == K_d:
                    self.moveCommandX += 8
                elif event.key == K_LEFT or event.key == K_a:
                    self.moveCommandX -= 8
                elif event.key == K_DOWN or event.key == K_s:
                    self.moveCommandY += 8
                elif event.key == K_UP or event.key == K_w:
                    self.moveCommandY -= 8

    def update(self):
        self.gameState.update(self.moveCommandX, self.moveCommandY)

    def render(self):
        self.window.fill((0, 0, 0))
        x = self.gameState.x
        y = self.gameState.y
        pygame.draw.rect(self.window, (255, 0, 0), (x, y, 400, 240))
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def run(self):
        while (self.running):
            self.processInput()
            self.update()
            self.render()        
            self.clock.tick(60)


if __name__ == "__main__":
    userInterface = UserInterface()
    userInterface.run()
    pygame.quit()
