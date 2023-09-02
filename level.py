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
    

    def outro(self,SETTINGS):
        screen = pygame.display.get_surface()
        outro_time = 3#1 seconds
        circle_factor = screen.get_width()/1.5/outro_time#factor to mutiple so that the circle starts as big as the screen
        outro_surf = pygame.Surface(screen.get_size())
        time_stamp = pygame.time.get_ticks()
        while True:#loop where the screen get black(like in tom&jerry)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()
                time = (pygame.time.get_ticks()-time_stamp)*0.001
                if time >= outro_time:
                    break
                screen.fill((0,0,0))
                outro_surf.fill((0,0,0))
                self.camera.custom_draw(screen,self.player)

                pygame.draw.circle(outro_surf,(255,255,255),[self.player.rect.centerx+self.camera.offset[0],self.player.rect.centery+self.camera.offset[1]],(outro_time-time)*circle_factor)
                screen.blit(outro_surf,(0,0),special_flags=pygame.BLEND_RGB_MULT)
                pygame.display.flip()
                pygame.display.set_caption(str(round(self.clock.get_fps())))
                self.clock.tick(60)
                
    def intro(self,SETTINGS):
        screen = pygame.display.get_surface()
        intro_ticks = 100
        intro_surf = pygame.Surface(screen.get_size())
        font = pygame.font.SysFont(None,300)
        text = font.render(str(self.name),True,(255,255,255))
        text_rect = text.get_rect(center=(screen.get_width()/2,screen.get_height()/2))

        run = True
        while run:#loop where the screen get black(like in tom&jerry)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()
                intro_ticks -= 1
                if intro_ticks <= 0:
                    run = False

                c = int(255/100*(100-intro_ticks))
                intro_surf.fill((c,c,c))

                self.camera.custom_draw(screen,self.player)
                c = int(255/100*intro_ticks)
                text = font.render(self.name,True,(c,c,c),(0,0,0))
                screen.blit(text,text_rect,special_flags=pygame.BLEND_RGB_ADD)
                screen.blit(intro_surf,(0,0),special_flags=pygame.BLEND_RGB_MULT)
                pygame.display.flip()
                self.clock.tick(60)

    def next_level(self,name,SETTINGS,spritesheet):
        self.running = False
        #self.outro(SETTINGS)
        Level(f"assets/levels/{name}",spritesheet).run(SETTINGS,spritesheet)

    def run(self,SETTINGS,spritesheet):

        screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        #self.intro(SETTINGS)
        delta = 0
        self.running = True

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
            pygame.display.set_caption(str(round(self.clock.get_fps())))
            delta = self.clock.tick(SETTINGS["FPS"])
        