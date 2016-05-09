from abc import abstractmethod
import pygame


class Entity:
	x = 0
	y = 0
	dx = 0
	dy = 0
	color = (255, 255, 255)
	fixed = False
	mass = 1.
	restitution = 1.
	collisionGroup = 0

	@abstractmethod
	def draw(self, s):
		return

	@abstractmethod
	def collision(self, other):
		return

	def move(self, dt):
		self.x += self.dx
		self.y += self.dy

	def applyImpulse(self, a, b):
		self.dx += a
		self.dy += b


class Circle(Entity):
	radius = 1

	def __init__(self, x, y, r, color=(255, 255, 255)):
		self.x = x
		self.y = y
		self.radius = r
		self.color = color

	def draw(self, s):
		pygame.draw.circle(s, self.color, (int(self.x), int(self.y)), self.radius)

	def collision(self, other):
		if isinstance(other, Circle):
			return (self.radius + other.radius) ** 2 > (self.x - other.x) ** 2 + (self.y - other.y) ** 2
		else:
			return False


class AABB(Entity):
	height = 1
	width = 1

	def __init__(self, x, y, w, h, color=(255, 255, 255)):
		self.x = x
		self.y = y
		self.height = h
		self.width = w
		self.color = color

	def draw(self, s):
		pygame.draw.rect(s, self.color, (self.x, self.y, self.width, self.height))

	def collision(self, other):
		if isinstance(other, AABB):
			return not (self.x > other.x + other.width or self.y > other.y + other.height or
			            self.x + self.width < other.x or self.y + self.height < other.y)
		else:
			return False
