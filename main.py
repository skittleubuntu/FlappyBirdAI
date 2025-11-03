import pygame
from settings import *
from draw import Draw
from entity import *
import random

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
draw = Draw(screen)
player = Bird(HEIGHT // 2)
tubes = [Tube(600), Tube(900), Tube(1200)]

neurons = [Neuron(Bird(i + 100)) for i in range(NEURON_NUMBER)]


death = 0
generation = 1
mode = 1
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        mode = 1
    if keys[pygame.K_2]:
        mode = 2
    if keys[pygame.K_3]:
        mode = 3

    draw.background()
    draw.clouds()
    draw.floor()

    if mode == 1:
        if keys[pygame.K_r]:
            tubes = [Tube(600), Tube(900), Tube(1200)]
            player.live = True
            player.fitness = 0
            player.vy = 0
        if keys[pygame.K_SPACE] and player.live:
            player.jump()
        if player.live:
            player.update()
        if player.check(tubes):
            player.live = False
        player.draw(screen)
        for tube in tubes:
            tube.draw(screen)
            if player.live:
                tube.x -= 5
        if tubes[0].x <= 300 and len(tubes) != 4:
            tubes.append(Tube(1200))
        if tubes[0].x < -TUBE_WIDTH:
            last_tube_x = tubes[-1].x
            tubes.pop(0)
            tubes.append(Tube(last_tube_x + TUBE_SPACING))
        clock.tick(FPS)

    elif mode in [2, 3]:
        for neuron in neurons:
            if neuron.bird.live:
                neuron.update(tubes)
                if draw_speed:
                    neuron.bird.draw(screen)
                if neuron.bird.check(tubes):
                    neuron.bird.live = False
                    death += 1
                if sigmoid(neuron.value()) > 0.5 and neuron.bird.live:
                    neuron.bird.jump()
        for tube in tubes:
            tube.draw(screen)
            tube.x -= 5
        if tubes[0].x <= 300 and len(tubes) != 4:
            tubes.append(Tube(1200))
        if tubes[0].x < -TUBE_WIDTH:
            last_tube_x = tubes[-1].x
            tubes.pop(0)
            tubes.append(Tube(last_tube_x + TUBE_SPACING))
        if death == NEURON_NUMBER:
            tubes = [Tube(600), Tube(900), Tube(1200)]
            neurons.sort(key=lambda n: n.bird.fitness, reverse=True)
            best = neurons[:10]
            thebest = neurons[0]
            generation += 1
            new_neurons = []
            for _ in range(90):
                parent_a = random.choice(best)
                parent_b = random.choice(best)
                new_neurons.append(crossover(parent_a, parent_b))
            neurons = best + new_neurons
            death = 0
            for n in neurons:
                n.bird = Bird(random.randint(100, 400))
        if draw_speed:
            clock.tick(FPS)

    pygame.display.flip()

pygame.quit()
