import pygame

def load_tile_spritesheet(path,tile_size,tile_names,tile_types):
    #tile_names are the different tiles like wood grass etc
    #tile_types are the different orientation of the tiles like topleft,center etc
    spritesheet = pygame.image.load(path).convert_alpha()
    temp = pygame.Surface((tile_size,tile_size),pygame.SRCALPHA)
    sprites = {}
    for j,name in enumerate(tile_names):
        sprites_per_row = {}
        for i,typ in enumerate(tile_types):
            temp.fill((0,0,0,0))
            temp.blit(spritesheet,(0,0),pygame.Rect(i*tile_size,j*tile_size,tile_size,tile_size))
            sprites_per_row[typ] = temp.copy()
        sprites[name] = sprites_per_row
    return sprites

class Tile(pygame.sprite.Sprite):
    def __init__(self,groups,image,position):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
