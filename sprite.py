import pygame
from pygame.math import Vector2 as vector
import os

class Sprite(pygame.sprite.Sprite):
    def __init__(self,position,surface,group):
        super().__init__(group)
        self.image=surface
        self.rect=self.image.get_rect(topleft=position)
        self.hitbox=self.rect.inflate(0,-self.rect.height/2)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,position,surface,direction,group,bullet_speed):
        super().__init__(group)
        self.image=surface
        self.rect=self.image.get_rect(center=position)
        self.mask=pygame.mask.from_surface(self.image)
        
        # collisions
        self.hitbox=self.rect.inflate(0,-self.rect.width/2)
        self.position=vector(self.hitbox.center)
        self.speed=bullet_speed
        self.direction=direction
    
    def move(self,dt):
        self.position.x+=self.direction.x*self.speed*dt
        self.hitbox.centerx=round(self.position.x)
        self.rect.center=self.hitbox.center

        self.position.y+=self.direction.y*self.speed*dt
        self.hitbox.centery=round(self.position.y)
        self.rect.center=self.hitbox.center

    def update(self,dt):
        self.move(dt)


# Original author: Harbin Sela
# https://github.com/harbinsela