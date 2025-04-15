""" MEDITATIONS

PURPOSE OF PROJECT
    USE 90 MINUTES TO MAKE SOMETHING INTERESTING

AFTER 30 MINUTES I COULDN'T THINK OF ANYTHING.
JUST FUCK AROUND WITH PYGAME

2025-04-15 PHASE 2
MY INITIAL IDEA WAS ILL FORMED

TRY TO DO A BASIC GRAVITATIONAL SIMULATION.
CLICK ONCE TO START TO CREATE A NEW BODY
CLICK AGAIN TO INDICATE THE DIRECTION AND VELOCITY OF THE NEW BODY

IGNORE COLLISIONS

USE + AND - TO CHANGE THE STARTING SIZE (MASS) OF THE BODY

BODY NEEDS
    POSITION 2D
    VELOCITY 2D

ACCELERATION CALCULATION
    D = DISTANCE BETWEEN BODIES
    FORCE = <SOME CONSTANT> * (M1*M2) / D^2
    ACCELERATION = FORCE / MASS
    VEL CHANGE =
        ACCELERATION APPLIED IN THE VECTOR BETWEEN THE MASSES
        ANGLE BETWEEN X AXIS AND ACCEL VECTOR =
            Atan2( y2 - y1 / x2 - x1 )
        ACCELERATION COMPONENTS
            AY = A SIN(THETA)
            AX = A COS(THETA)
    AND SO ON
"""
import itertools
import math

import pygame as pg

WIDTH = 1200
HEIGHT = 900
SCREEN_SIZE = pg.Vector2(WIDTH, HEIGHT)
pg.init()
screen = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock()
bodies = []
V_REDUCE = 50
TOO_CLOSE = 15
ATTRACTION_CONSTANT = 1

class Body():
    def __init__(self, mass=10, x=0, y=0, vx=0.0, vy=0.0):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def draw(self, r, g, b):
        pg.draw.circle(screen, (r, g, b), (self.x, self.y),
                       self.mass)

def calc_distance(point1, point2):
    dx = abs(point1.x - point2.x)
    dy = abs(point1.y - point2.y)
    return math.sqrt(dx**2 + dy**2)


def midpoint(point1, point2):
    return (point1.x + point2.x) / 2, (point1.y + point2.y) / 2

def step():
    for a, b in itertools.combinations(bodies, 2):
        distance = calc_distance(a,b)
        if distance < TOO_CLOSE:
            continue

        force = ATTRACTION_CONSTANT * (a.mass*b.mass)/(distance**1.2)
        angle = math.atan2((b.y-a.y),(b.x-a.x))

        # apply changes to velocity
        a_accel = force / a.mass

        a.vx += a_accel * math.cos(angle)
        a.vy += a_accel * math.sin(angle)

        b_accel = force / b.mass

        b.vx += -b_accel * math.cos(angle)
        b.vy += -b_accel * math.sin(angle)

    for body in bodies:


        # apply changes to position
        body.x += body.vx
        body.y += body.vy

        # bounce off walls
        if not (0 < body.x < WIDTH):
            body.vx = -body.vx
        if not (0 < body.y < HEIGHT):
            body.vy = -body.vy


def main():
    running = True
    red = 0
    green = 0
    blue = 0
    on_vector = False
    target_position = (0,0)

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.MOUSEBUTTONUP:
                if not on_vector:
                    target_position = pg.mouse.get_pos()
                    on_vector = True
                else:
                    vector_position = pg.mouse.get_pos()

                    bodies.append( Body(x=target_position[0],
                                        y=target_position[1],
                             vx = (vector_position[0] - target_position[0]) /
                                  V_REDUCE,
                             vy = (vector_position[1] - target_position[1])
                                   / V_REDUCE))

                    on_vector = False

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
        for thing in bodies:
            thing.draw(255-red, 255-green, 255-blue)


        pg.display.flip()
        delta_time = clock.tick(60)
    pg.quit()

if __name__ == '__main__':
    main()
