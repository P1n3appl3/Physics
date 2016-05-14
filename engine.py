from abc import abstractmethod
import pygame
import math
import numpy


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

	@abstractmethod
	def setpos(self, (x, y)):
		return


class Circle(Entity):
	radius = 1
	x = 0
	y = 0

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

	def setpos(self, pos):
		self.x, self.y = pos

	def move(self, fps):
		self.x += self.dx * fps
		self.y += self.dy * fps


class Polygon(Entity):
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

	def setpos(self, pos):
		c = self.center()
		self.points = [(i[0] - c[0] + pos[0], i[1] - c[1] + pos[1]) for i in self.points]

	def move(self, fps):
		self.points = [(i[0] + self.dx * fps, i[1] + self.dy * fps) for i in self.points]


class RegularPolygon(Polygon):
	def __init__(self, p, s, r, c=(255, 255, 255)):
		n = math.pi * 2 / s
		Polygon.__init__(self, [(math.sin(n * i) * r + p[0], math.cos(n * i) * r + p[1]) for i in range(s)], c)


class Rectangle(Polygon):
	def __init__(self, p, w, h, c=(255, 255, 255)):
		Polygon.__init__(self, [(p[0], p[1]), (p[0] + w, p[1]), (p[0] + w, p[1] + h), (p[0], p[1] + h)], c)


def SAT(v, a, b):
	aa = []
	bb = []
	for i in a:
		aa.append(numpy.dot(v, i))
	for i in b:
		bb.append(numpy.dot(v, i))
	return max(aa) > min(bb) and max(bb) > min(aa)


def collision(a, b):
	newA = a
	newB = b
	if isinstance(a, Circle) and isinstance(b, Circle):
		return (a.radius + b.radius) ** 2 > (a.x - b.x) ** 2 + (a.y - b.y) ** 2
	elif isinstance(a, Polygon) and isinstance(b, Circle):
		# todo: add voronoi region real circle checking
		t = RegularPolygon((b.x, b.y), 10, b.radius)
		newB = t
	elif isinstance(a, Circle) and isinstance(b, Polygon):
		# todo: add voronoi region real circle checking
		t = RegularPolygon((a.x, a.y), 10, a.radius)
		newA = t
	for i in range(len(newA.points)):
		temp = tuple(numpy.subtract(newA.points[i], newA.points[i + 1 if i < len(newA.points) - 1 else 0]))
		if not (SAT((temp[1] * -1, temp[0]), newA.points, newB.points)):
			return False
	for i in range(len(newB.points)):
		temp = tuple(numpy.subtract(newB.points[i], newB.points[i + 1 if i < len(newB.points) - 1 else 0]))
		if not (SAT((temp[1] * -1, temp[0]), newA.points, newB.points)):
			return False
	return True
