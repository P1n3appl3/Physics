import sys
from engine import AABB, Circle
import pygame
import time


def main():
	pygame.init()
	screenSize = screenWidth, screenHeight = 680, 480
	screen = pygame.display.set_mode(screenSize)

	currentTime = time.clock()
	dt = accumulator = 0.
	fps = 1. / 60

	# defining shapes
	shapes = [AABB(0, 0, 0, screenHeight),
	          AABB(0, 0, screenWidth, 0),
	          AABB(screenWidth, 0, 0, screenHeight),
	          AABB(0, screenHeight, screenWidth, 0)]
	testCircle1 = AABB(100, 100, 10, 10)
	testCircle1.applyImpulse(1, .25)
	testCircle2 = AABB(400, 150, 50, 50)
	shapes.append(testCircle1)
	shapes.append(testCircle2)

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
			for s in shapes:
				s.move(fps)

		# drawing
		screen.fill((0, 0, 0))
		for s in shapes:
			s.draw(screen)
		pygame.display.flip()
		#time.sleep(.005)


if __name__ == "__main__":
	main()
