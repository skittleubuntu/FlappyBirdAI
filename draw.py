from settings import *
import pygame
import random as r


# --- Cloud class ---
class Cloud():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # draw one cloud
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, CLOUD_WIDTH, CLOUD_HEIHT))


# --- Generate random clouds ---
def generate_clouds():
    result = []
    step = 200

    # place clouds along the width
    for x in range(0, WIDTH, step):
        y = r.randint(10, 500)
        result.append(Cloud(x, y))

    return result



# --- Drawing manager ---
class Draw():
    def __init__(self, screen):
        self.screen = screen
        self._clouds = generate_clouds()
        self.number_of_clouds = len(self._clouds)

    # draw sky
    def background(self):
        pygame.draw.rect(self.screen, SKY_BLUE, (0, 0, WIDTH, HEIGHT))

    # draw clouds and move them
    def clouds(self):
        # add new cloud if one was removed
        if len(self._clouds) < self.number_of_clouds:
            self._clouds.append(Cloud(WIDTH, r.randint(10, 500)))

        # remove cloud if off-screen
        if self._clouds[0].x < -CLOUD_WIDTH:
            self._clouds.pop(0)

        # move clouds slowly
        for cloud in self._clouds:
            cloud.x -= 1
            cloud.draw(self.screen)

    # draw ground
    def floor(self):
        pygame.draw.rect(self.screen, BROWN, (0, HEIGHT - 200, WIDTH, HEIGHT - 500))
        pygame.draw.rect(self.screen, GREEN, (0, HEIGHT - 220, WIDTH, HEIGHT - 750))
        # TODO: add grass here