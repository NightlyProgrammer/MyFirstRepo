import pygame

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = [0,0]
     
    def custom_draw(self,screen,player):
        self.offset = [self.offset[0]+(screen.get_width()/2-(player.rect.centerx+self.offset[0]))*0.03,self.offset[1]+(screen.get_height()/2-(player.rect.centery+self.offset[1]))*0.03]

        #draw ground
        pygame.draw.rect(screen,(0,255,0),pygame.Rect(0,self.offset[1],screen.get_width(),screen.get_height()-self.offset[1]))
        #draw sprites
        for sprite in self.sprites():
            screen.blit(sprite.image,(sprite.rect.x+self.offset[0],sprite.rect.y+self.offset[1]))