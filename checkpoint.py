import pygame
import json

class CheckPoint(pygame.sprite.Sprite):
    def __init__(self,groups,position,purpose="save",level="level0"):
        super().__init__(groups)
        self.image = pygame.Surface((64,64))
        self.image.fill((0,255,240))
        self.rect = self.image.get_rect(bottomleft=position)
        self.purpose = purpose#wether its a checkpoint to save the progress or to go to the next level
        self.level_name = level

    def update(self,nextlevel,player,settings,spritesheet):
        if self.rect.colliderect(player.rect):
            if self.purpose == "save":
                data = {self.level_name:[x/(64*((i==1)*-2+1)) for i,x in enumerate(self.rect.bottomleft)]}
                with open("game data/level_progress.json","r+") as file:
                    json.dump(data,file)
            else:#load next level
                nextlevel(self.purpose,settings,spritesheet)#self.purpse = next level file name,settings is a constant with fps,screensize etc..