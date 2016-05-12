import sys
import pygame
import time
import engine
import math


def main():
	pygame.init()
	screenSize = screenWidth, screenHeight = 680, 480
	screen = pygame.display.set_mode(screenSize)

	currentTime = time.clock()
	dt = accumulator = 0.
	fps = 1. / 60

	# defining shapes
	shapes = []
	shapes.append(engine.Polygon([(100, 100), (150, 100), (100, 150)]))
	shapes.append(engine.Rectangle((100, 300), 70, 200))
	shapes.append(engine.Circle((500, 200), 40))
	shapes.append(engine.RegularPolygon((400, 400), 8, 70))

	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		# time calculations
		dt = time.clock() - currentTime
		currentTime = time.clock()
		accumulator += dt;
		if accumulator > fps:
			accumulator -= fps
			# game logic
			for s in shapes:
				s.move(fps)
				s.rotate(s.center(), .01)

		# drawing
		screen.fill((0, 0, 0))
		for s in shapes:
			s.draw(screen)
		pygame.display.flip()
	# time.sleep(.005)


if __name__ == "__main__":
	main()
