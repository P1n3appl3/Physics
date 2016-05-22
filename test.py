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

	# create test entities
	world = engine.Scene(screenWidth, screenHeight)
	for i in range(10):
		col = (int(r.random() * 255), int(r.random() * 255), int(r.random() * 255))
		speed = 500
		world.shapes.append(engine.Circle((int(r.random() * screenWidth), int(r.random() * screenHeight)), int(r.random() * 30) + 10, col))
		world.shapes[-1].dx = r.randrange(-speed, speed)
		world.shapes[-1].dy = r.randrange(-speed, speed)
		world.shapes[-1].restitution = .9 + r.random() / 10
		while any([True if world.collision(world.shapes[n], world.shapes[-1]) else False for n in range(len(world.shapes) - 1)]):
			world.shapes[-1].setPos((int(r.random() * screenWidth), int(r.random() * screenHeight)))

	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		# per second stuff
		if int(time.clock()) > int(currentTime):
			print sum(int(math.sqrt(s.dx ** 2 + s.dy ** 2)) for s in world.shapes)

		# time calculations
		accumulator += time.clock() - currentTime
		currentTime = time.clock()
		accumulator = min(accumulator, 2 * engine.Scene.fps)
		while accumulator > engine.Scene.fps:
			accumulator -= engine.Scene.fps
			# game logic
			world.step()

		# drawing
		screen.fill((0, 0, 0))
		world.draw(screen)
		pygame.display.flip()


if __name__ == "__main__":
	main()
