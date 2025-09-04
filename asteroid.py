from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT
import pygame
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.copy_made = False

    def draw(self, screen):
        pygame.draw.circle(screen,color=(255,255,255),center=self.position,radius=self.radius,width=2)
    
    def update(self, dt):
        # Update position based on velocity and time
        self.position += dt*self.velocity

        # If we've already created a copy of this asteroid for wrapping,
        # don't create another one
        if self.copy_made:
            return

        # If the asteroid is completely inside the screen bounds,
        # no wrapping is needed
        if self.position.x >=0 and self.position.x <= SCREEN_WIDTH and self.position.y >=0 and self.position.y <= SCREEN_HEIGHT:
            return

        # Screen wrapping logic:
        # When an asteroid moves off one edge of the screen, we create a copy
        # that appears on the opposite edge. This creates a smooth transition
        # and maintains game continuity.

        # Conditions for creating wrapped copy:
        # 1. For X-axis: Create copy if asteroid is moving left and touching left edge,
        #    or moving right and touching right edge
        # 2. For Y-axis: Create copy if asteroid is moving up and touching top edge,
        #    or moving down and touching bottom edge
        new_x = self.position.x  # Copy's x position
        new_y = self.position.y  # Copy's y position

        if self.position.x - self.radius < 0:
            if self.velocity.x >=0:
                return
            new_x +=  SCREEN_WIDTH
        elif self.position.x + self.radius > SCREEN_WIDTH:
            if self.velocity.x <=0:
                return
            new_x -= SCREEN_WIDTH

        if self.position.y - self.radius < 0:
            if self.velocity.y >=0:
                return
            new_y +=  SCREEN_HEIGHT
        elif self.position.y + self.radius > SCREEN_HEIGHT:
            if self.velocity.y <=0:
                return
            new_y -= SCREEN_HEIGHT

        if new_x != self.position.x or new_y != self.position.y:
            self.copy_made = True
            asteroid_copy = Asteroid(new_x,new_y,self.radius)
            asteroid_copy.velocity = self.velocity
        else:
            return

        # Remove this asteroid once it's completely off screen
        # This happens after its copy has been created on the opposite side
        # This prevents duplicate asteroids and maintains game performance
        if self.position.x + self.radius < 0 or self.position.x - self.radius > SCREEN_WIDTH:
            self.kill()
        if self.position.y + self.radius < 0 or self.position.y - self.radius > SCREEN_HEIGHT:
            self.kill()

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




    