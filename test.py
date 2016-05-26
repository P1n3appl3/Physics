import sys
import pygame
import time
import engine
import math
import random as r


def main():
	pygame.init()
	screenSize = screenWidth, screenHeight = 800, 800
	screen = pygame.display.set_mode(screenSize)

	currentTime = time.clock()
	accumulator = 0.

	energy = 0

	# create test entities
	world = engine.Scene(screenWidth, screenHeight)
	for i in range(10):
		col = (int(r.random() * 255), int(r.random() * 255), int(r.random() * 255))
		speed = 700
		if r.random() > .49:
			world.shapes.append(engine.RegularPolygon((int(r.random() * screenWidth), int(r.random() * screenHeight)),
		                                          int(r.random() * 2) + 3, int(r.random() * 40) + 10))
		else:
			world.shapes.append(engine.Circle((int(r.random() * screenWidth), int(r.random() * screenHeight)),
		                                          int(r.random() * 10) + 30))
		world.shapes[-1].dx = r.randrange(-speed, speed)
		world.shapes[-1].dy = r.randrange(-speed, speed)
		world.shapes[-1].restitution = .49 + r.random() / 100
		while any([True if world.collision(world.shapes[n], world.shapes[-1]) else False for n in
		           range(len(world.shapes) - 1)]):
			world.shapes[-1].setPos((int(r.random() * screenWidth), int(r.random() * screenHeight)))

	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		# per second stuff
		if int(time.clock()) > int(currentTime):
			print "Energy: "+ str(energy) + "  Entities: " + str(len(world.shapes))

		# time calculations
		accumulator += time.clock() - currentTime
		currentTime = time.clock()
		accumulator = min(accumulator, 2 * engine.Scene.fps)
		while accumulator > world.fps:
			accumulator -= world.fps
			# game logic
			energy = int(sum(int(math.sqrt(s.dx ** 2 + s.dy ** 2)) for s in world.shapes))
			if not(pygame.key.get_pressed()[pygame.K_SPACE]):
				world.step()

		# drawing
		screen.fill((100, 100, 100))
		world.draw(screen)
		screen.blit(pygame.font.Font(None, 40).render(str(energy), False, (0, 0, 0)), (0, 0))
		pygame.display.flip()


if __name__ == "__main__":
	main()
