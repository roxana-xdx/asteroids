import sys
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    Shot.containers = (shots, updatable, drawable)
    
    pygame.font.init()
    arial_font_path = pygame.font.match_font("arial")
    if arial_font_path:
        font = pygame.font.Font(arial_font_path, 30)
    else:
        font = pygame.font.Font(None, 36)
    score = 0

    while(True):
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")

        for object in drawable:
            object.draw(screen)

        updatable.update(dt)

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                print(f"Score: {score}")
                sys.exit()

            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")

                    if asteroid.radius == ASTEROID_MIN_RADIUS:
                        score += 15
                    elif asteroid.radius == ASTEROID_MAX_RADIUS:
                        score += 5
                    else:
                        score += 10

                    asteroid.split()
                    shot.kill()
        
        score_text = font.render(f"Score: {score}", True, "white")
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        # limit framerate to 60 FPS
        dt = clock.tick(60) / 1000



if __name__ == "__main__":
    main()
