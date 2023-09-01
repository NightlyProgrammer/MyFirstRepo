import pygame

class CameraGroup(pygame.sprite.Group):
    def __init__(self,ground_image=None,bg_imgs=[]):
        super().__init__()
        self.offset = [0,0]
        self.ground_surface = ground_image
        self.bg_images = bg_imgs#sorted from furthest to nearest

    def custom_draw(self,screen,player):
        self.offset = [self.offset[0]+(screen.get_width()/2-(player.rect.centerx+self.offset[0]))*0.03,self.offset[1]+(screen.get_height()/2-(player.rect.centery+self.offset[1]))*0.03]

        #draw background with offsets
        for i,img in enumerate(self.bg_images):
            offset_factor = i/(len(self.bg_images)-1)#-1 cuz the last bg img shouldnt move at all
            if i!=0:
                screen.blit(img,((self.offset[0]*offset_factor)%screen.get_width()-screen.get_width(),(self.offset[1]-img.get_height())*offset_factor))
            screen.blit(img,((self.offset[0]*offset_factor)%screen.get_width(),(self.offset[1]-img.get_height())*offset_factor))

        #draw ground
        if self.ground_surface is not None:
            #draws the ground surface two times to make sure you dont see a void when scrolling
            screen.blit(self.ground_surface,(self.offset[0]%self.ground_surface.get_width()-self.ground_surface.get_width(),self.offset[1]),pygame.Rect(0,0,screen.get_width(),screen.get_height()-self.offset[1]))
            screen.blit(self.ground_surface,(self.offset[0]%self.ground_surface.get_width(),self.offset[1]),pygame.Rect(0,0,screen.get_width(),screen.get_height()-self.offset[1]))#the rect is the area of the ground surface that is drawn
        else:
            pygame.draw.rect(screen,(0,255,0),pygame.Rect(0,self.offset[1],screen.get_width(),screen.get_height()-self.offset[1]))

        #draw sprites
        for sprite in self.sprites():
            screen.blit(sprite.image,(sprite.rect.x+self.offset[0],sprite.rect.y+self.offset[1]))