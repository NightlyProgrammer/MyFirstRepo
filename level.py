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
        temp_surf = pygame.Surface(screen.get_size())
        clock = pygame.time.Clock()

        font = pygame.font.SysFont(None,300)
        text = font.render(self.name,True,(255,255,255),(0,0,0))
        text_rect = text.get_rect(center=(screen.get_width()/2,screen.get_height()/2))
        pygame.time.set_timer(pygame.USEREVENT+1,intro_time*1000)
        run = True
        timestemp = pygame.time.get_ticks()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT+1:
                    run = False
            
            time = (pygame.time.get_ticks()-timestemp)*0.001

            self.camera.custom_draw(screen,self.player)

            screen.blit(text,text_rect,special_flags=pygame.BLEND_RGB_ADD)
            c = max(int(255/intro_time*(intro_time-time)),0)
            text = font.render(self.name,True,(c,c,c),(0,0,0))

            c = min(int(255/intro_time*time),255)
            temp_surf.fill((c,c,c))
            screen.blit(temp_surf,(0,0),special_flags=pygame.BLEND_RGB_MULT)

            pygame.display.flip()
            pygame.display.set_caption(str(round(clock.get_fps())))
            clock.tick(SETTINGS["FPS"])

    def outro(self,SETTINGS):
        outro_time = 3
        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT+1,outro_time*1000)
        run = True
        timestemp = pygame.time.get_ticks()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT+1:
                    run = False
            time = (pygame.time.get_ticks()-timestemp)*0.001
            self.camera.custom_draw(screen,self.player)
            pygame.draw.rect(screen,(0,0,0),pygame.Rect(0,0,screen.get_width(),screen.get_height()/outro_time*time))

            pygame.display.flip()
            pygame.display.set_caption(str(round(clock.get_fps())))
            clock.tick(SETTINGS["FPS"])

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
        self.player.no_input = 0.17*10#no input for the first 10 frames (meaning the palyer rect wont be updated due to weird high delta value when starting level)
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
        