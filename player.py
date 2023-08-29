import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self,groups,position):
        super().__init__(groups)
        self.image = pygame.Surface((64,128))
        self.rect = self.image.get_rect(bottomleft=position)
        self.jump_height = -16

    def inputs(self):
        keys = pygame.keys.get_pressed()

        if keys[pygame.K_a]:
            self.dir.x = -1
        elif keys[pygame.K_d]:
            self.dir.x = 1

        if keys[pygame.K_w] or keys[pygame.K_SPACE]:
            self.dir.y = self.jump_height
        
        self.rect.x += self.dir.x*delta
        self.rect.y += self.dir.y*delta
        self.dir.y += 1
    def update(self):
        self.inputs()