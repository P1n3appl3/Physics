import sys
import pygame
import time
import engine


def main():
	pygame.init()
	screenSize = screenWidth, screenHeight = 680, 480
	screen = pygame.display.set_mode(screenSize)

	currentTime = time.clock()
	dt = accumulator = 0.
	fps = 1. / 60

	# defining shapes
	world = engine.Scene()
	world.addEntity(engine.Polygon([(100, 100), (150, 100), (100, 150)]))
	world.addEntity(engine.Polygon([(130, 130), (280, 155), (155, 205)]))
	world.addEntity(engine.Rectangle((200, 300), 70, 200))
	world.addEntity(engine.Circle((100, 400), 40))
	world.shapes[3].setCollisionGroup(2)
	#world.shapes[2].addCollisionMask(2)
	world.addEntity(engine.RegularPolygon((500, 200), 8, 70))

	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		# time calculations
		dt = time.clock() - currentTime
		currentTime = time.clock()
		accumulator += dt
		accumulator = min(accumulator, 2 * fps)
		while accumulator > fps:
			accumulator -= fps
			# game logic
			for s in world.shapes:
				s.move(fps)
				s.rotate(s.center(), .01)
				s.color = (255, 255, 255)
			for x in range(len(world.shapes)):
				for y in range(len(world.shapes)):
					if x != y:
						if engine.collision(world.shapes[x], world.shapes[y]):
							world.shapes[x].color = (255, 0, 0)

		# drawing
		screen.fill((0, 0, 0))
		world.draw(screen)
		pygame.display.flip()
	# time.sleep(.005)


if __name__ == "__main__":
	main()
