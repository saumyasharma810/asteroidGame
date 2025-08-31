from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS
import pygame
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen,color=(255,255,255),center=self.position,radius=self.radius,width=2)
    
    def update(self, dt):
        self.position += dt*self.velocity

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return 3
        angle = random.uniform(20,50)
        asteroid1 = Asteroid(self.position.x,self.position.y,self.radius-ASTEROID_MIN_RADIUS)
        asteroid2 = Asteroid(self.position.x,self.position.y,self.radius-ASTEROID_MIN_RADIUS)

        asteroid1.velocity = pygame.math.Vector2.rotate(self.velocity, angle)*1.2
        asteroid2.velocity = pygame.math.Vector2.rotate(self.velocity, -angle)*1.2
        return 1




    