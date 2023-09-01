import pygame
from sys import exit
import json
from tiles import Tile,load_tile_spritesheet
from player import Player
from camera import CameraGroup
from checkpoint import CheckPoint

class Level:
    def __init__(self,path):
        self.camera = CameraGroup(pygame.image.load("assets/graphics/ground.png").convert())
        self.name = path.split('/')[-1].split('.')[0]#get name from path,used for save data
        self.load_level(path)

    def load_level(self,path):
        with open(path,'r') as file:
            data = json.load(file)
        
            self.tiles = pygame.sprite.Group()
            self.checkpoints = pygame.sprite.Group()
            tile_spritesheet = dict(zip(["topleft","topmiddle","topright"],load_tile_spritesheet("assets/graphics/tiles_spritesheet.png",64)))#asign a surface to each type(topleft,topright etc.)
            for tile in data["Tiles"]:
                Tile([self.tiles,self.camera],tile_spritesheet[tile["Type"]],[x*64*((i==1)*-2+1) for i,x in enumerate(tile["Position"])])
            
            self.player = Player([self.camera],[x*64*((i==1)*-2+1) for i,x in enumerate(data["Player"]["Position"])])
            for checkpoint in data["Checkpoints"]:#if checkpoints possess "NextLevel" key in dict,player will progress to next level,but you will be able to have multiple of these for eg secret levels or level selection
                try:
                    purpose = checkpoint["NextLevel"]
                except:
                    purpose = "save"
                CheckPoint([self.camera,self.checkpoints],[x*64*((i==1)*-2+1) for i,x in enumerate(checkpoint["Position"])],purpose,self.name)

    def next_level(self,name,SETTINGS):
        self.running = False
        Level(f"assets/levels/{name}").run(SETTINGS)
        
    def run(self,SETTINGS):

        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()

        delta = 0
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()
            screen.fill((0,0,0))
            self.player.update(self.tiles,delta)
            self.checkpoints.update(self.next_level,self.player,SETTINGS)

            self.camera.custom_draw(screen,self.player)

            pygame.display.flip()
            pygame.display.set_caption(str(round(clock.get_fps())))
            delta = clock.tick(SETTINGS["FPS"])
        