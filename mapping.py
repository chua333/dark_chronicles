import os
import pygame
os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the window on the screen

from pygame.locals import *


class GameState():
    def __init__(self):
        self.spritePos = pygame.math.Vector2(120, 120)

    def update(self, vel, dt):
        self.spritePos += vel * dt


class UserInterface:
    def __init__(self):
        pygame.init()
        self.running = True
        self.window = pygame.display.set_mode((640, 640), vsync=1)
        self.gameState = GameState()
        self.clock = pygame.time.Clock()

        self.iconImage = pygame.image.load("F_sWcSIbQAAog2U.png").convert_alpha()
        self.captionName = "Simple Pygame App"
        pygame.display.set_caption(self.captionName)
        pygame.display.set_icon(self.iconImage)

        self.unitsTexture = pygame.image.load(
            "ground_shaker_asset/Red/Bodies/body_tracks.png"
            ).convert_alpha()
        self.unitsTexture = pygame.transform.scale(
            self.unitsTexture, (64, 64))
        # # convert via scale
        # scale_factor = 0.5
        # w, h = self.unitsTexture.get_size()
        # self.unitsTexture = pygame.transform.scale(
        #     self.unitsTexture, (int(w * scale_factor), int(h * scale_factor)))
        
        self.backgroundTexture = pygame.image.load(
            "ground_shaker_asset/map_preview.png"
            ).convert_alpha()
        # self.backgroundTexture = pygame.transform.scale(
        #     self.backgroundTexture, (640, 640))
        # # convert via scale
        scale_factor = 2
        bg_w, bg_h = self.backgroundTexture.get_size()
        self.backgroundTexture = pygame.transform.scale(
            self.backgroundTexture, (int(bg_w * scale_factor), int(bg_h * scale_factor)))
        
        self.win_w, self.win_h = self.window.get_size()
        self.world_w, self.world_h = self.backgroundTexture.get_size()

        # sprite source rect (adjust if the sprite size is different)
        self.sprite_w, self.sprite_h = self.unitsTexture.get_size()
        self.spriteRect = None

        # movement in pixels per second
        self.speed = 300

    def process_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    self.running = False

    def get_input_velocity(self):
        keys = pygame.key.get_pressed()
        vx = (keys[K_d] or keys[K_RIGHT]) - (keys[K_a] or keys[K_LEFT])
        vy = (keys[K_s] or keys[K_DOWN]) - (keys[K_w] or keys[K_UP])
        vel = pygame.math.Vector2(vx, vy)
        if vel.length_squared() > 0:
            vel = vel.normalize() * self.speed
        return vel

    def update(self, dt):
        vel = self.get_input_velocity()
        self.gameState.update(vel, dt)

        # clamp tank to the world so it doesn't go out of bounds
        max_x = self.world_w - self.sprite_w
        max_y = self.world_h - self.sprite_h
        self.gameState.spritePos.x = self._clamp(self.gameState.spritePos.x, 0, max(0, max_x))
        self.gameState.spritePos.y = self._clamp(self.gameState.spritePos.y, 0, max(0, max_y))

    def render(self):
        camera = self._get_camera_rect()
        self.window.blit(self.backgroundTexture, (0, 0), camera)

        # tank screen position = world pos - camera top-left, then centre it
        screen_x = self.win_w // 2 - self.sprite_w // 2
        screen_y = self.win_h // 2 - self.sprite_h // 2

        # if not using spritesheet, omit the 3rd arg
        if self.spriteRect:
            self.window.blit(self.unitsTexture, (screen_x, screen_y), self.spriteRect)
        else:
            self.window.blit(self.unitsTexture, (screen_x, screen_y))

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def _clamp(self, v, lo, hi):
        return lo if v < lo else hi if v > hi else v
    
    def _get_camera_rect(self):
        # center the camera on the sprite
        cx = int(self.gameState.spritePos.x - self.win_w // 2)
        cy = int(self.gameState.spritePos.y - self.win_h // 2)

        # clamp the camera to the world bounds
        cx = self._clamp(cx, 0, max(0, self.world_w - self.win_w))
        cy = self._clamp(cy, 0, max(0, self.world_h - self.win_h))

        return pygame.Rect(cx, cy, self.win_w, self.win_h)

    def run(self):
        while (self.running):
            dt = self.clock.tick(60) / 1000.0
            event = pygame.event.poll()
            self.process_events()
            self.update(dt)
            self.render()
            # # to debug output, throttle it
            if int(pygame.time.get_ticks()) % 500 == 0:
                print(f"spritePos={self.gameState.spritePos}")


if __name__ == "__main__":
    ui = UserInterface()
    ui.run()
    pygame.quit()
