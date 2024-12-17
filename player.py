import pygame
import os
from pygame.math import Vector2 as vector
from entity import Entity
import sys

class Player(Entity):
    def __init__(self, position, group, collision_sprite, path, create_bullet):
        super().__init__(position, group, collision_sprite, path)
        self.create_bullet = create_bullet
        self.bullet_shot = False
        self.health = 100
        self.bullet_direction = vector()
        self.is_vulnerable = True  # Ensure the player can take damage initially
        self.attack_time = 0
        self.hit_sound = pygame.mixer.Sound(os.path.join('sound', 'hit.mp3'))  # Example hit sound
        self.last_shot_time = 0  # Timer for the shooting cooldown
        self.shoot_cooldown = 1  # Cooldown in milliseconds (lower value = faster shooting)

    def animate(self, dt):
        self.frameidx += 7 * dt
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds

        # Shoot only if enough time has passed since the last shot
        if int(self.frameidx) == 2 and self.attacking and not self.bullet_shot:
            if current_time - self.last_shot_time > self.shoot_cooldown:
                self.create_bullet(self.rect.center + self.bullet_direction * 80, self.bullet_direction, 800)
                self.bullet_shot = True
                self.bullet_sound.play()
                self.last_shot_time = current_time  # Update the last shot time

        if self.frameidx >= len(self.animations[self.status]):
            self.frameidx = 0
            if self.attacking:
                self.attacking = False
        self.image = self.animations[self.status][int(self.frameidx)]
        self.mask = pygame.mask.from_surface(self.image)

    def damage(self):
        if self.is_vulnerable:
            self.health -= 20  # Decrease health by 20
            self.hit_sound.play()  # Play hit sound
            self.is_vulnerable = False  # Make the player temporarily invulnerable
            self.attack_time = pygame.time.get_ticks()  # Record the time of the last hit
            if self.health <= 0:
                self.check_death()

    def check_death(self):
        if self.health <= 0:
            print("Player has died!")
            pygame.quit()
            sys.exit()

    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.attacking:
            # vertical movement
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            # horizontal movement
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # attacking (shooting)
            current_time = pygame.time.get_ticks()
            if keys[pygame.K_SPACE] and current_time - self.last_shot_time > self.shoot_cooldown:
                self.attacking = True
                self.direction = vector()
                self.frameidx = 0
                self.bullet_shot = False
                self.last_shot_time = current_time  # Update the last shot time
                if self.status.split('_')[0] == 'left':
                    self.bullet_direction = vector(-1, 0)
                elif self.status.split('_')[0] == 'right':
                    self.bullet_direction = vector(1, 0)
                elif self.status.split('_')[0] == 'up':
                    self.bullet_direction = vector(0, -1)
                elif self.status.split('_')[0] == 'down':
                    self.bullet_direction = vector(0, 1)

    def update(self, dt):
        self.input()
        self.get_status()
        self.invincibility_timer()  # Ensure this method exists or remove it
        self.animate(dt)
        self.blink()  # Ensure this method exists or remove it
        self.move(dt)
        self.check_death()


# Original author: Harbin Sela
# https://github.com/harbinsela