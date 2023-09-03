import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self,groups,position):
        super().__init__(groups)
        self.image = pygame.Surface((64,128)) 
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(bottomleft=position)

        self.dir = pygame.math.Vector2(0,0)
        self.jump_height = -1.3
        self.jump_button_pressed = False
        self.gravity = 0.008*0.8
        self.speed = 0.5
        self.on_ground = False

    def collision(self,sprites,x=False,y=False):
        if y:
            if self.rect.bottom > 0:#check if player is colliding with the ground
                self.rect.bottom = 0
                self.dir.y = 0
                self.on_ground = True
                return
        for sprite in sprites:
            if sprite.rect.colliderect(self.rect):
                if x:
                    if self.dir.x < 0:
                        self.rect.left = sprite.rect.right
                    elif self.dir.x > 0:
                        self.rect.right = sprite.rect.left
                elif y:
                    if self.dir.y < 0:
                        self.rect.top = sprite.rect.bottom
                    elif self.dir.y > 0:
                        self.rect.bottom = sprite.rect.top
                        self.dir.y = 0
                        self.on_ground = True
                    
    def inputs(self,sprites,delta):
        keys = pygame.key.get_pressed()

        self.dir.x = 0
        if keys[pygame.K_a]:
            self.dir.x = -1
        elif keys[pygame.K_d]:
            self.dir.x = 1

        if (keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground and not self.jump_button_pressed:
            self.dir.y = self.jump_height
            self.on_ground = False
            self.jump_button_pressed = True
        elif not(keys[pygame.K_w] or keys[pygame.K_SPACE]):
            self.jump_button_pressed = False
        
        self.rect.x += self.dir.x*self.speed*delta
        self.collision(sprites,x=True)
        self.rect.y += self.dir.y*delta
        self.collision(sprites,y=True)
        self.dir.y += delta*self.gravity

    def update(self,sprites,delta):
        self.inputs(sprites,delta)
    def just_collision_updates(self,sprites,delta):
        self.collision(sprites,x=True)
        self.collision(sprites,y=True)