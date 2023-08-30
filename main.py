import pygame
import json
from player import Player
from camera import CameraGroup
from tiles import Tile

def load_settings(path):
    with open(path,'r') as file:
        return json.load(file)
        

def main():
    #Load all the constants from a json file
    SETTINGS = load_settings("settings.json")
    screen = pygame.display.set_mode(SETTINGS["SCREEN_SIZE"])
    clock = pygame.time.Clock()

    camera = CameraGroup()#Group for drawing sprites with an offset to follow player
    tiles = pygame.sprite.Group()#sprite group for tiles player may collide with
    player = Player([camera],[0,0])

    for x in range(10):
        Tile([camera,tiles],[x*64,0])

    delta = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
        screen.fill((0,0,0))
        player.update(tiles,delta)

        camera.custom_draw(screen,player)

        pygame.display.flip()
        pygame.display.set_caption(str(round(clock.get_fps())))
        delta = clock.tick(SETTINGS["FPS"])

if __name__ == '__main__':
    pygame.init()
    main()