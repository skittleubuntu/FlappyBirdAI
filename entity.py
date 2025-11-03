from settings import *
import pygame
import random as r


def crossover(p1, p2):
    child = Neuron(Bird(r.randint(100, 400)))

    child.w1 = r.choice([p1.w1, p2.w1])
    child.w2 = r.choice([p1.w2, p2.w2])
    child.w3 = r.choice([p1.w3, p2.w3])
    child.w4 = r.choice([p1.w4, p2.w4])



    mutate(child)

    return child

def mutate(neuron, rate=0.05, strength=0.2):
    if r.random() < rate:
        neuron.w1 += r.uniform(-strength, strength)
    if r.random() < rate:
        neuron.w2 += r.uniform(-strength, strength)
    if r.random() < rate:
        neuron.w3 += r.uniform(-strength, strength)
    if r.random() < rate:
        neuron.w4 += r.uniform(-strength, strength)



def sigmoid(a):
    return 1 / (1 + pow(2.71828, -a))

class Neuron():
    def __init__(self,bird):
        self.bird = bird
        self.w1 = r.uniform(-1, 1)
        self.w2 = r.uniform(-1, 1)
        self.w3 = r.uniform(-1, 1)
        self.w4 = r.uniform(-1, 1)

        self.x1 = 0
        self.x2 = 0
        self.x3 = 0
        self.x4 = 0


    def update(self, tubes):

        self.bird.update()

        next_tube = None
        for tube in tubes:
            if tube.x + TUBE_WIDTH > self.bird.x:
                next_tube = tube
                break
        if not next_tube:
            next_tube = tubes[0]

        #bird Y
        self.x1 = self.bird.y / HEIGHT
        #bird vy
        self.x2 = self.bird.vy / 10
        #tube x
        self.x3 = (next_tube.x - self.bird.x) / WIDTH
        #tube space
        self.x4 = (next_tube.space + SPACE / 2) / HEIGHT


    def value(self):
        return self.x1 * self.w1 + self.x2 * self.w2 + self.x3 * self.w3 + self.x4 * self.w4

class Bird():
    def __init__(self,y):
        self.x = WIDTH // 4
        self.y = y
        self.vy = 0
        self.live = True
        self.color = YELLOW
        self.fitness = 0




    def update(self):
        self.vy += GRAVITY
        self.y += self.vy
        self.fitness += 0.01



    def jump(self):
        self.vy = JUMP_STRENGTH

    def check(self, tubes):
        bird_rect = pygame.Rect(self.x, self.y, BIRD_SIZE, BIRD_SIZE)


        if self.y <= 0 or self.y + BIRD_SIZE >= HEIGHT  - 220:
            return True


        for tube in tubes:
            top_rect = pygame.Rect(tube.x, tube.y, TUBE_WIDTH, tube.space)
            bottom_rect = pygame.Rect(
                tube.x,
                tube.y + tube.space + SPACE,
                TUBE_WIDTH,
                TUBE_HEIGHT - (tube.y + tube.space + SPACE)
            )

            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                return True

        return False

    def draw(self, screen):
        cx = int(self.x + BIRD_SIZE / 2)
        cy = int(self.y + BIRD_SIZE / 2)


        bird_surface = pygame.Surface((60, 40), pygame.SRCALPHA)


        body_color = self.color
        pygame.draw.ellipse(bird_surface, body_color, (10, 5, 40, 30))


        wing_color = (230, 170, 0)
        wing_rect = pygame.Rect(18, 15, 24, 10)
        pygame.draw.ellipse(bird_surface, wing_color, wing_rect)


        beak_color = ORANGE
        beak_points = [
            (50, 15),
            (60, 18),
            (50, 21)
        ]
        pygame.draw.polygon(bird_surface, beak_color, beak_points)


        eye_color = WHITE
        pupil_color = (0, 0, 0)
        pygame.draw.circle(bird_surface, eye_color, (40, 12), 5)
        pygame.draw.circle(bird_surface, pupil_color, (42, 12), 2)


        pygame.draw.ellipse(bird_surface, (0, 0, 0), (10, 5, 40, 30), 2)


        angle = max(-60, min(60, -self.vy * 3))

        rotated_bird = pygame.transform.rotate(bird_surface, angle)


        rect = rotated_bird.get_rect(center=(self.x + 20, self.y + 20))


        screen.blit(rotated_bird, rect.topleft)


        font = pygame.font.SysFont("Arial", 16, bold=True)
        fitness_text = font.render(f"F: {round(self.fitness, 2)}", True, (0, 0, 0))
        screen.blit(fitness_text, (self.x + 45, self.y + 15))


class Tube():
    def __init__(self,x):
        self.x = x
        self.y = 0
        #space its a distance from TOP
        #space for bird always 100
        self.space = r.randint(100,300)



    def draw(self,screen):
        pygame.draw.rect(screen,DARK_GREEN, (self.x, self.y, TUBE_WIDTH, self.space))
        pygame.draw.rect(screen,DARK_GREEN, (self.x, self.y + self.space + SPACE, TUBE_WIDTH, TUBE_HEIGHT - self.y - SPACE - self.space ))
