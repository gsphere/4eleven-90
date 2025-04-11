""" MEDITATIONS

PURPOSE OF PROJECT
    USE 90 MINUTES TO MAKE SOMETHING INTERESTING

AFTER 30 MINUTES I COULDN'T THINK OF ANYTHING.
JUST FUCK AROUND WITH PYGAME

"""
import math

import pygame as pg

SCREEN_SIZE = pg.Vector2(1200,900)
pg.init()
screen = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock()
things = []
lower_limit = 65
limit = 100


def distance(thing, neighbor):
    dx = abs(thing[0] - neighbor[0])
    dy = abs(thing[1] - neighbor[1])
    return math.sqrt(dx**2 + dy**2)


def midpoint(thing, neighbor):
    return (thing[0] + neighbor[0]) / 2, (thing[1] + neighbor[1]) / 2


def step():
    to_add = []
    global things
    for thing in things:
        for other_thing in things:
            if other_thing == thing:
                continue
            else:
                if lower_limit < distance(thing, other_thing) < limit:
                    to_add.append(midpoint(thing, other_thing))
                    print(f"created {midpoint(thing, other_thing)} for {other_thing}")

                    # this shit is broken

    things = things + to_add

def main():
    running = True
    red = 0
    green = 0
    blue = 0

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.MOUSEBUTTONUP:
                target_position = pg.mouse.get_pos()
                things.append(target_position)

            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    running = False

                if event.key == pg.K_q:
                    red += 10
                if event.key == pg.K_w:
                    green += 10
                if event.key == pg.K_e:
                    blue += 10
                if event.key == pg.K_a:
                    red -= 10
                if event.key == pg.K_s:
                    green -= 10
                if event.key == pg.K_d:
                    blue -= 10

        step()

        # drawing

        screen.fill((red, green, blue))
        for thing in things:
            pg.draw.circle(screen, (255-red, 255-green, 255-blue), thing,
                           5)


        pg.display.flip()
        delta_time = clock.tick(60)
    pg.quit()

if __name__ == '__main__':
    main()
