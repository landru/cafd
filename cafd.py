#! /usr/bin/env python

import pygame
import simple3d
import view3d

debug = False

# window dimensions
w = h = 500
# colors
bgcolor = (0xf5,0xf5,0xf5)
fgcolor = (0,0,0xa0)
# CPU throttle
delay = 200
# key repeat delay, interval
key_delay = 20
key_interval = 20
# radians per key press
theta = 0.025
# displacement per key press
incr = 0.05

fish = simple3d.Simple3d()
#fish.load_object("objects", "tst2")
fish.load_object("objects", "ttt")

view = view3d.View3d((0,0, w,h), (-1.0,-1.0, 1.0,1.0), (-1.0, 1.0, -1.0, 1.0, -1.0, 1.0), (0.0, 0.0, -5.0), 1.0)

if debug :
   fish.debug()
   view.debug()

# using +1 here to avoid using -1 elsewhere
screen = pygame.display.set_mode((w+1, h+1))
clock = pygame.time.Clock()
pygame.key.set_repeat(key_delay, key_interval)
running = True

while running:
   for event in pygame.event.get() :
      if event.type == pygame.QUIT :
         running = False
      elif event.type == pygame.KEYDOWN :
         if event.key == pygame.K_i :
            # zoom in
            view.distance += incr
            if debug : print( view.distance )
         elif event.key == pygame.K_o :
            # zoom out
            view.distance -= incr
            if debug : print( view.distance )
         elif event.key == pygame.K_q : 
            # quit
            running = False
         elif event.key == pygame.K_z : 
            # rotate around Z axis (clockwise, from viewer's perspective)
            fish.rotZ(theta)
         elif event.key == pygame.K_y : 
            # rotate around Y axis
            fish.rotY(theta)
         elif event.key == pygame.K_x : 
            # rotate around X axis
            fish.rotX(theta)
         elif event.key == pygame.K_UP :
            # move up
            fish.move((0.0, -incr, 0.0))
         elif event.key == pygame.K_DOWN :
            # move down
            fish.move((0.0, incr, 0.0))
         elif event.key == pygame.K_LEFT :
            # move left
            fish.move((-incr, 0.0, 0.0))
         elif event.key == pygame.K_RIGHT :
            # move right
            fish.move((incr, 0.0, 0.0))
         
   screen.fill(bgcolor)

   for e in fish.edge :
      pygame.draw.aaline(screen, fgcolor, view.v2s(view.w2v(fish.vertex[e[0]])), view.v2s(view.w2v(fish.vertex[e[1]])))
      if debug :
         print( fish.vertex[e[0]], fish.vertex[e[1]] )
         print( view.w2v(fish.vertex[e[0]]), view.w2v(fish.vertex[e[1]]) )
         print( view.v2s(view.w2v(fish.vertex[e[0]])), view.v2s(view.w2v(fish.vertex[e[1]])) )
         debug = False

   pygame.display.flip()
   clock.tick(delay)

   