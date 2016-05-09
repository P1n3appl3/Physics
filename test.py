import sys
from engine import AABB, Circle
import pygame
import time


def main():
	pygame.init()
	screenSize = screenWidth, screenHeight = 680, 480
	screen = pygame.display.set_mode(screenSize)

	currentTime = time.clock()
	currentSecond = int(time.time())
	dt = 0.

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

		for s in shapes:
			s.move(dt)

		if testCircle2.collision(testCircle1):
			print "contact"

		# time calculations
		dt = time.clock() - currentTime
		currentTime = time.clock()
		if int(time.time()) > currentSecond:
			currentSecond += 1

		# drawing
		screen.fill((0, 0, 0))
		for s in shapes:
			s.draw(screen)
		pygame.display.flip()
		time.sleep(.005)


if __name__ == "__main__":
	main()
