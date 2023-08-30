import pygame

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = [0,0]
    
    def custom_draw(self,screen,player):
        self.offset = [screen.get_width()/2-player.rect.centerx,screen.get_height()/2-player.rect.centery]
        for sprite in self.sprites():
            screen.blit(sprite.image,(sprite.rect.x+self.offset[0],sprite.rect.y+self.offset[1]))