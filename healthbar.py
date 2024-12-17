import pygame
import os


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, position, max_health):
        super().__init__()
        self.position = position
        self.max_health = max_health
        self.health = max_health
        self.image = pygame.image.load(os.path.join('graphics', 'healthbar', 'healthbar.png')).convert_alpha()  # Updated path
        self.rect = self.image.get_rect(topleft=self.position)

    def update(self, health):
        self.health = health
        # Resize the health bar based on health
        self.image = pygame.image.load(os.path.join('graphics', 'healthbar', 'healthbar.png')).convert_alpha()  # Updated path
        # Crop or scale the health bar to show only a portion corresponding to the player's current health
        health_width = int(self.rect.width * (self.health / self.max_health))
        self.image = pygame.transform.scale(self.image, (health_width, self.rect.height))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

# Original author: Harbin Sela
# https://github.com/harbinsela