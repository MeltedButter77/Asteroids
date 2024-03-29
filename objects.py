import math
import random
from copy import copy
import pygame
from pygame.sprite import Group as _Group


def rot_center(image, angle, center):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=center).center)
    return rotated_image, new_rect


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, location, size, *groups: _Group):
        super().__init__(*groups)

        self.speed = pygame.Vector2(random.randint(-100, 100)/100, random.randint(-100, 100)/100)

        self.size = size
        if self.size == 1:
            self.image = pygame.image.load("asteroid1.png")
            self.speed.scale_to_length(random.randint(5, 10) / 3)
        elif self.size == 2:
            self.image = pygame.image.load("asteroid2.png")
            self.speed.scale_to_length(random.randint(5, 10) / 5)
        elif self.size == 3:
            self.image = pygame.image.load("asteroid3.png")
            self.speed.scale_to_length(random.randint(5, 10) / 8)

        self.image = pygame.transform.rotate(self.image, random.randint(0, 360))
        self.rect = self.image.get_rect()

        self.position = location
        self.rect.center = self.position

    def update(self):
        self.position += self.speed
        self.rect.center = self.position

        # wrap around screen edges
        if self.position.x > 1024:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = 1024
        if self.position.y > 768:
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = 768


class Bullet(pygame.sprite.Sprite):

    def __init__(self, player, *groups: _Group):
        super().__init__(*groups)
        self.image = pygame.image.load("bullet.png")
        self.rect = self.image.get_rect()
        self.position = copy(player.position)
        self.rect.center = self.position

        bullet_speed = 3
        self.speed = pygame.Vector2(bullet_speed * math.cos(player.angle), bullet_speed * math.sin(player.angle)) + player.speed

    def update(self, asteroids, *groups: _Group):
        self.position += self.speed
        self.rect.center = self.position

        # wrap around screen edges
        if self.position.x > 1024:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = 1024
        if self.position.y > 768:
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = 768

        for asteroid in asteroids:
            if self.rect.colliderect(asteroid.rect):
                self.kill()
                for i in range(2):
                    Asteroid(asteroid.position, asteroid.size - 1, asteroid.groups())
                asteroid.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, location, *groups: _Group):
        super().__init__(*groups)

        # Fixed Values
        self.max_speed = 3
        self.r_speed = 0.05
        self.acceleration = 0.08

        # Altered Values
        self.angle = 0
        self.angle_old = 0
        self.speed = pygame.Vector2(0, 0)
        self.angle = 0
        self.position = pygame.Vector2(location)

        # Image and Rect
        self.image = pygame.image.load("player.png")
        self.image_original = self.image.copy()
        self.rect = self.image.get_rect()

    def update(self, keys_pressed):
        # copy angle
        self.angle_old = copy(self.angle)

        # Set speed by acceleration
        if keys_pressed[pygame.K_LEFT]:
            self.angle -= self.r_speed
        if keys_pressed[pygame.K_RIGHT]:
            self.angle += self.r_speed
        if keys_pressed[pygame.K_UP]:
            self.speed.x += self.acceleration * math.cos(self.angle)
            self.speed.y += self.acceleration * math.sin(self.angle)

        # Move the player by speed with max speed
        if self.speed.length() > self.max_speed:
            self.speed.scale_to_length(self.max_speed)
        self.position += self.speed

        # rotate image according to angle (rotate func is opposite to unit circle)
        self.image, self.rect = rot_center(self.image_original, -math.degrees(self.angle), self.position)

        # wrap position around edges of screen
        if self.position.x > 1024:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = 1024
        if self.position.y > 768:
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = 768

        # update rect
        self.rect.center = self.position
