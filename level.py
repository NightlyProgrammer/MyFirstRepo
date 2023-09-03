import pygame
from sys import exit
import json
from tiles import Tile,load_tile_spritesheet
from player import Player
from camera import CameraGroup
from checkpoint import CheckPoint
from os import listdir

class Level:
    def __init__(self,path,tile_spritesheet):
        self.camera = CameraGroup(pygame.image.load("assets/graphics/ground.png").convert_alpha(),[pygame.transform.scale(pygame.image.load("assets/graphics/bg/"+img).convert(),(1280,720)) if i==0 else pygame.transform.scale(pygame.image.load("assets/graphics/bg/"+img).convert_alpha(),(1280,720)) for i,img in enumerate(listdir("assets/graphics/bg"))])#i know this looks extremly messy,this is just a temporary solution until i will just read them out of a game settings file
        self.name = path.split('/')[-1].split('.')[0]#get name from path,used for save data
        self.load_level(path,tile_spritesheet)

    def load_level(self,path,tile_spritesheet):
        with open(path,'r') as file:
            data = json.load(file)
        
            self.tiles = pygame.sprite.Group()
            self.checkpoints = pygame.sprite.Group()
            
            for tile in data["Tiles"]:
                Tile([self.tiles,self.camera],tile_spritesheet[tile["Name"]][tile["Type"]],[x*64*((i==1)*-2+1) for i,x in enumerate(tile["Position"])])
            
            self.player = Player([self.camera],[x*64*((i==1)*-2+1) for i,x in enumerate(data["Player"]["Position"])])
            for checkpoint in data["Checkpoints"]:#if checkpoints possess "NextLevel" key in dict,player will progress to next level,but you will be able to have multiple of these for eg secret levels or level selection
                try:
                    purpose = checkpoint["NextLevel"]
                except:
                    purpose = "save"
                CheckPoint([self.camera,self.checkpoints],[x*64*((i==1)*-2+1) for i,x in enumerate(checkpoint["Position"])],purpose,self.name)

    def intro(self,SETTINGS):
        intro_time = 3
        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT+1,intro_time*1000)
        run = True
        timestemp = pygame.time.get_ticks()
        delta = 0
        while run:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT+1:
                    run = False
            time = (pygame.time.get_ticks()-timestemp)*0.001
            self.player.just_collision_updates(self.tiles,delta)
            self.camera.custom_draw(screen,self.player)
            pygame.draw.rect(screen,(0,0,0),pygame.Rect(0,screen.get_height()-(screen.get_height()/intro_time*(intro_time-time)),screen.get_width(),screen.get_height()/intro_time*(intro_time-time)))

            pygame.display.flip()
            pygame.display.set_caption(str(round(clock.get_fps())))
            delta = clock.tick(SETTINGS["FPS"])

    def outro(self,SETTINGS):
        outro_time = 3
        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT+1,outro_time*1000)
        run = True
        timestemp = pygame.time.get_ticks()
        delta = 0
        while run:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT+1:
                    run = False
            time = (pygame.time.get_ticks()-timestemp)*0.001
            self.player.just_collision_updates(self.tiles,delta)
            self.camera.custom_draw(screen,self.player)
            pygame.draw.rect(screen,(0,0,0),pygame.Rect(0,0,screen.get_width(),screen.get_height()/outro_time*time))

            pygame.display.flip()
            pygame.display.set_caption(str(round(clock.get_fps())))
            delta = clock.tick(SETTINGS["FPS"])

    def next_level(self,name,SETTINGS,spritesheet):
        self.running = False
        self.outro(SETTINGS)
        Level(f"assets/levels/{name}",spritesheet).run(SETTINGS,spritesheet)

    def run(self,SETTINGS,spritesheet):
        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()
        delta = 0
        self.running = True
        self.intro(SETTINGS)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()
            screen.fill((0,0,0))
            self.player.update(self.tiles,delta)
            self.checkpoints.update(self.next_level,self.player,SETTINGS,spritesheet)

            self.camera.custom_draw(screen,self.player)

            pygame.display.flip()
            pygame.display.set_caption(str(round(clock.get_fps())))
            delta = clock.tick(SETTINGS["FPS"])
        