from abc import abstractmethod
import pygame
import math


class Entity:
	"""Parent class for all physics objects"""
	dx = dy = dz = 0.
	color = (255, 255, 255)
	fixed = False
	mass = 1.
	restitution = 1.
	collisionGroup = 0

	@abstractmethod
	def draw(self, s):
		return

	@abstractmethod
	def rotate(self, (x, y), ang=math.pi / 4):
		return

	@abstractmethod
	def center(self):
		return

	@abstractmethod
	def move(self, fps):
		return


class Circle(Entity):
	radius = 1
	points = x, y = (0, 0)

	def __init__(self, (x, y), r, c=(255, 255, 255)):
		self.x = x
		self.y = y
		self.radius = r
		self.color = c

	def draw(self, s):
		pygame.draw.circle(s, self.color, (int(self.x), int(self.y)), self.radius)

	def collision(self, other):
		if isinstance(other, Circle):
			return (self.radius + other.radius) ** 2 > (self.x - other.x) ** 2 + (self.y - other.y) ** 2
		else:
			return False

	def rotate(self, (x, y), ang=math.pi / 4):
		return

	def center(self):
		return self.x, self.y

	def move(self, fps):
		self.x += self.dx * fps
		self.y += self.dy * fps


class Polygon(Entity):
	"""Convex polygon"""
	points = [(0, 0)]

	def __init__(self, p, c=(255, 255, 255)):
		self.points = p
		self.color = c

	def draw(self, s):
		pygame.draw.polygon(s, self.color, self.points, 0)

	def center(self):
		return sum([i[0] for i in self.points]) / len(self.points), sum([i[1] for i in self.points]) / len(self.points)

	def rotate(self, (x, y), ang=math.pi / 4):
		self.points = [(x + (p[0] - x) * math.cos(ang) - (p[1] - y) * math.sin(ang),
		                y + (p[0] - x) * math.sin(ang) + (p[1] - y) * math.cos(ang)) for p in self.points]

	def move(self, fps):
		self.points = [(i[0] + self.dx * fps, i[1] + self.dy * fps) for i in self.points]


class RegularPolygon(Polygon):
	def __init__(self, (x, y), s, len, c=(255, 255, 255)):
		n = math.pi * 2 / s
		Polygon.__init__(self, [(math.sin(n * i) * len + x, math.cos(n * i) * len + y) for i in range(s)], c)


class Rectangle(Polygon):
	def __init__(self, (x, y), w, h, c=(255, 255, 255)):
		Polygon.__init__(self, [(x, y), (x + w, y), (x + w, y + h), (x, y + h)], c)


def collision(a, b):
	if isinstance(a, Rectangle) and isinstance(b, Rectangle):
		# todo: check object's AABBs
		return False
	elif isinstance(a, Circle) and isinstance(b, Circle):
		return (a.radius + b.radius) ** 2 > (a.x - b.x) ** 2 + (a.y - b.y) ** 2
	else:
		# todo: add SAT collision
		return
