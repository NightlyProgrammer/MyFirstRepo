import pygame

def load_tile_spritesheet(path,tile_size):
    spritesheet = pygame.image.load(path).convert()
    temp = pygame.Surface((tile_size,tile_size))
    sprites = []
    for i in range(spritesheet.get_width()//tile_size):
        temp.blit(spritesheet,(0,0),pygame.Rect(i*tile_size,0,tile_size,tile_size))
        sprites.append(temp.copy())
    return sprites

class Tile(pygame.sprite.Sprite):
    def __init__(self,groups,image,position):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
