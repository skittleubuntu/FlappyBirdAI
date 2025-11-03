import pygame
from settings import *
from draw import Draw
from entity import *
import random


#skittle inc.

# --- Initialize pygame ---
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

draw = Draw(screen)
player = Bird(HEIGHT // 2)
tubes = [Tube(600), Tube(900), Tube(1200)]

# create list of neurons
neurons = [Neuron(Bird(i + 100)) for i in range(NEURON_NUMBER)]


# --- Game variables ---
death = 0
generation = 1
mode = 1
running = True


# --- Main game loop ---
while running:

    # check for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # check keyboard keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        mode = 1
    if keys[pygame.K_2]:
        mode = 2
    if keys[pygame.K_3]:
        mode = 3


    # --- Draw background ---
    draw.background()
    draw.clouds()
    draw.floor()


    # --- MODE 1: player control ---
    if mode == 1:

        # reset game
        if keys[pygame.K_r]:
            tubes = [Tube(600), Tube(900), Tube(1200)]
            player.live = True
            player.fitness = 0
            player.vy = 0

        # jump
        if keys[pygame.K_SPACE] and player.live:
            player.jump()

        # update bird
        if player.live:
            player.update()

        # check collision
        if player.check(tubes):
            player.live = False

        # draw bird and tubes
        player.draw(screen)
        for tube in tubes:
            tube.draw(screen)
            if player.live:
                tube.x -= 5

        # generate new tubes
        if tubes[0].x <= 300 and len(tubes) != 4:
            tubes.append(Tube(1200))
        if tubes[0].x < -TUBE_WIDTH:
            last_tube_x = tubes[-1].x
            tubes.pop(0)
            tubes.append(Tube(last_tube_x + TUBE_SPACING))

        clock.tick(FPS)


    # --- MODE 2 or 3: AI training ---
    elif mode in [2, 3]:

        draw_speed = (mode == 2)

        # update all neurons (birds)
        for neuron in neurons:
            if neuron.bird.live:
                neuron.update(tubes)

                if draw_speed:
                    neuron.bird.draw(screen)

                # check collision
                if neuron.bird.check(tubes):
                    neuron.bird.live = False
                    death += 1

                # neuron decides when to jump
                if sigmoid(neuron.value()) > 0.5 and neuron.bird.live:
                    neuron.bird.jump()

        # draw and move tubes
        for tube in tubes:
            tube.draw(screen)
            tube.x -= 5

        # add new tubes
        if tubes[0].x <= 300 and len(tubes) != 4:
            tubes.append(Tube(1200))
        if tubes[0].x < -TUBE_WIDTH:
            last_tube_x = tubes[-1].x
            tubes.pop(0)
            tubes.append(Tube(last_tube_x + TUBE_SPACING))

        # all birds dead → next generation
        if death == NEURON_NUMBER:
            tubes = [Tube(600), Tube(900), Tube(1200)]

            # sort by best fitness
            neurons.sort(key=lambda n: n.bird.fitness, reverse=True)
            best = neurons[:10]
            thebest = neurons[0]

            pygame.display.set_caption(
                f"GENERATION {generation} "
                f"Weight: w1:{thebest.w1} w2:{thebest.w2} w3:{thebest.w3} w4:{thebest.w4} "
                f"BEST FITNESS: {round(thebest.bird.fitness, 2)}"
            )

            generation += 1
            new_neurons = []

            # create children from best parents
            for _ in range(90):
                parent_a = random.choice(best)
                parent_b = random.choice(best)
                new_neurons.append(crossover(parent_a, parent_b))

            neurons = best + new_neurons
            death = 0

            # reset birds
            for n in neurons:
                n.bird = Bird(random.randint(100, 400))

        if draw_speed:
            clock.tick(FPS)


    # --- Update screen ---
    pygame.display.flip()


pygame.quit()

