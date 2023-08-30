import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self,groups,position):
        super().__init__(groups)
        self.image = pygame.Surface((64,64))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect(topleft=position)
