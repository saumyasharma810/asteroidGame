import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfields import AsteroidField
from shot import Shot
from explosion import Explosion




def main():
    pygame.init()
    pygame.font.init() 
    font = pygame.font.SysFont('Arial', 32)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image = pygame.image.load('img/background.png').convert()
    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    all_shots = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()
    Player.containers = (updatable,drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = {all_shots,drawable,updatable}
    

    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroidField = AsteroidField()


    # game loop
    # 1. Check for player inputs
    # 2. Update the game world
    # 3. Draw the game to the screen

    game_over = False
    player_score = 0
    
    while True:
        if not game_over:
            score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))
            lives_counter = font.render(f"Lives left: {player.lives}", True, (255, 255, 255))

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            # screen.fill(color=(0,0,0))
            screen.blit(background_image, (0, 0))
            for obj in drawable:
                obj.draw(screen)
            screen.blit(score_text, (10, 10))
            screen.blit(lives_counter, (1100, 10))
            updatable.update(dt)
            explosion_group.draw(screen)
            explosion_group.update()
            for obj in asteroids:
                if not player.collision(obj):
                    continue
                obj.kill()
                # player.position = pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
                player.lives -= 1
                if player.lives == 0:
                    game_over = True   
                    print(f"Game over! Your score is {player.score}")
                player_score = player.score
                break
                # exit(0)
            
            if game_over:
                continue
            for asteroid in asteroids:
                for shot in all_shots:
                    if asteroid.collision(shot):
                        explosion = Explosion(asteroid.position.x, asteroid.position.y)
                        explosion_group.add(explosion)
                        player.score += asteroid.split()
                        shot.kill()
            pygame.display.flip()
            dt = clock.tick(float(60))/1000

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            # screen.fill((0,0,0))
            screen.blit(background_image, (0, 0))
            score_text = font.render(f"Your Score: {player_score}", True, (255, 255, 255))
            screen.blit(score_text, ((SCREEN_WIDTH - score_text.get_width()) // 2, (SCREEN_HEIGHT - score_text.get_height()) // 2))
            pygame.display.flip()
            clock.tick(30)

    



if __name__ == "__main__":
    main()
