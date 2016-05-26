from abc import abstractmethod
import pygame
import math
import numpy


class Scene:
	shapes = []
	width = 0
	height = 0
	bounds = True
	boundRect = {}
	fps = 1. / 60
	maxSpeed = 700

	def __init__(self, w, h, s=[]):
		self.width = w
		self.height = h
		for i in s:
			self.shapes.append(i)

	def removeEntity(self, e):
		self.shapes[:] = [i for i in self.shapes if not (i is e)]

	def addEntity(self, e):
		self.shapes.append(e)

	def draw(self, s):
		for e in self.shapes:
			e.draw(s)
			x, y = e.center()
			pygame.draw.line(s, (255 - e.color[0], 255 - e.color[1], 255 - e.color[2]), (x, y),
			                 (x + e.dx / (e.mass * 5000), y + e.dy / (e.mass * 5000)), 2)

	def step(self):
		collisionPairs = []
		for s in range(len(self.shapes)):
			# self.applyGravity(.1)
			# self.applyRelativeGravity()
			# self.applyFriction(.00005)
			self.shapes[s].move(self.fps)
			self.shapes[s].rotate(self.shapes[s].center(), self.shapes[s].dz)
			self.shapes[s].color = (255, 255, 255)
			broad = AABB(self.shapes[s])
			for s2 in range(len(self.shapes)):
				broad2 = AABB(self.shapes[s2])
				if s != s2:
					if not ((s2, s) in collisionPairs):
						if broad.intersect(broad2):
							collisionPairs.append((s, s2))

			if self.bounds:
				center = self.shapes[s].center()
				if broad.right > self.width:
					self.shapes[s].setPos((self.width - (broad.right - center[0]), center[1]))
					self.shapes[s].dx *= -self.shapes[s].restitution
				if broad.top > self.height:
					self.shapes[s].setPos((center[0], self.height - (broad.top - center[1])))
					self.shapes[s].dy *= -self.shapes[s].restitution
				if broad.left < 0:
					self.shapes[s].setPos((center[0] - broad.left, center[1]))
					self.shapes[s].dx *= -self.shapes[s].restitution
				if broad.bottom < 0:
					self.shapes[s].setPos((center[0], center[1] - broad.bottom))
					self.shapes[s].dy *= -self.shapes[s].restitution

		for c in collisionPairs:
			if Scene.collision(self.shapes[c[0]], self.shapes[c[1]]):
				self.shapes[c[0]].color = (255, 0, 0)
				self.shapes[c[1]].color = (255, 0, 0)
			# self.circleBounce(self.shapes[c[-1][0]], self.shapes[c[-1][1]])

	def applyGravity(self, strength):
		for s in self.shapes:
			s.dy = min(s.dy + strength, self.maxSpeed)

	def applyRelativeGravity(self):
		for s in self.shapes:
			for s2 in self.shapes:
				x, y = s.center()
				x2, y2 = s2.center()
				if not (s is s2):
					norm = numpy.array([x - x2, y - y2]) / math.sqrt((x - x2) ** 2 + (y - y2) ** 2)
					s2V = numpy.array([s2.dx, s2.dy]) + norm / (5000. * s.mass)

					s2.dx = s2V[0]
					s2.dy = s2V[1]

	def applyFriction(self, strength):
		for s in self.shapes:
			s.dx *= 1 - strength
			s.dy *= 1 - strength

	@staticmethod
	def circleBounce(a, b):
		dist = math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)
		norm = numpy.array([a.x - b.x, a.y - b.y]) / dist
		minimumTransVector = norm * (a.radius + b.radius - dist)
		av = numpy.array([a.dx, a.dy])
		bv = numpy.array([b.dx, b.dy])
		aMag = numpy.linalg.norm(av)
		bMag = numpy.linalg.norm(bv)
		a.setPos(tuple(numpy.array([a.x, a.y]) + minimumTransVector * aMag / (aMag + bMag)))
		b.setPos(tuple(numpy.array([b.x, b.y]) - minimumTransVector * bMag / (aMag + bMag)))
		r = min(a.restitution, b.restitution)
		p = 2 * r * ((av[0] * norm[0] + av[1] * norm[1]) - (bv[0] * norm[0] + bv[1] * norm[1])) / (a.mass + b.mass)
		av = av - p * a.mass * norm
		bv = bv + p * b.mass * norm
		a.dx = av[0]
		a.dy = av[1]
		b.dx = bv[0]
		b.dy = bv[1]

	@staticmethod
	def polyBounce(a, b, minTrans):
		# todo: make SAT return minTrans so that this works
		dist = math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)
		norm = numpy.array([a.x - b.x, a.y - b.y]) / dist
		minimumTransVector = norm * minTrans
		av = numpy.array([a.dx, a.dy])
		bv = numpy.array([b.dx, b.dy])
		aMag = numpy.linalg.norm(av)
		bMag = numpy.linalg.norm(bv)
		a.setPos(tuple(numpy.array([a.x, a.y]) + minimumTransVector * aMag / (aMag + bMag)))
		b.setPos(tuple(numpy.array([b.x, b.y]) - minimumTransVector * bMag / (aMag + bMag)))
		r = min(a.restitution, b.restitution)
		p = 2 * r * ((av[0] * norm[0] + av[1] * norm[1]) - (bv[0] * norm[0] + bv[1] * norm[1])) / (a.mass + b.mass)
		av = av - p * a.mass * norm
		bv = bv + p * b.mass * norm
		a.dx = av[0]
		a.dy = av[1]
		b.dx = bv[0]
		b.dy = bv[1]

	@staticmethod
	def SAT(v, a, b):
		aa = []
		bb = []
		for i in a:
			aa.append(numpy.dot(v, i))
		for i in b:
			bb.append(numpy.dot(v, i))
		return max(aa) > min(bb) and max(bb) > min(aa)

	@staticmethod
	def collision(a, b):
		if b.collisionMask % a.collisionGroup != 0 or a.collisionMask % b.collisionGroup != 0:
			return False
		newA = a
		newB = b
		if isinstance(a, Circle) and isinstance(b, Circle):
			return (a.radius + b.radius) ** 2 > (a.x - b.x) ** 2 + (a.y - b.y) ** 2
		elif isinstance(a, Polygon) and isinstance(b, Circle):
			# todo: add voronoi region real circle checking
			newB = RegularPolygon((b.x, b.y), 10, b.radius)
		elif isinstance(a, Circle) and isinstance(b, Polygon):
			# todo: add voronoi region real circle checking
			newA = RegularPolygon((a.x, a.y), 10, a.radius)

		for i in range(len(newA.points)):
			temp = tuple(numpy.subtract(newA.points[i], newA.points[i + 1 if i < len(newA.points) - 1 else 0]))
			if not (Scene.SAT((temp[1] * -1, temp[0]), newA.points, newB.points)):
				return False
		for i in range(len(newB.points)):
			temp = tuple(numpy.subtract(newB.points[i], newB.points[i + 1 if i < len(newB.points) - 1 else 0]))
			if not (Scene.SAT((temp[1] * -1, temp[0]), newA.points, newB.points)):
				return False
		return True


class Entity:
	"""Parent class for all physics objects"""
	dx = 0.
	dy = 0.
	dz = 0.
	color = (255, 255, 255)
	fixed = False
	mass = 1.
	restitution = 1.
	collisionGroup = 1
	collisionMask = 1

	def addCollisionMask(self, n):
		self.collisionMask |= (n + 1)

	def removeCollisionMask(self, n):
		self.collisionMask -= (n + 1) ** 2

	def setCollisionGroup(self, n):
		self.collisionGroup = 2 ** n

	def __init__(self):
		return

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
	def setPos(self, (x, y)):
		return


class Circle(Entity):
	radius = 1
	x = 0.
	y = 0.

	def __init__(self, (x, y), r, c=(255, 255, 255)):
		self.x = x
		self.y = y
		self.radius = r
		self.color = c
		self.mass = 1. / int(r ** 2)

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

	def setPos(self, pos):
		self.x, self.y = pos

	def move(self, fps):
		self.x += self.dx * fps
		self.y += self.dy * fps


class Polygon(Entity):
	points = [(0., 0.)]

	def __init__(self, p, c=(255, 255, 255)):
		self.points = p
		self.color = c
		self.mass = 1. / self.area()

	def draw(self, s):
		pygame.draw.polygon(s, self.color, self.points, 0)

	def center(self):
		return sum(((float(i[0]) for i in self.points))) / len(self.points), sum(
			(float(i[1]) for i in self.points)) / len(self.points)

	def area(self):
		return abs(sum(self.points[i][0] * self.points[i + 1 if i < len(self.points) - 1 else 0][1] - self.points[i][1] *
		           self.points[i + 1 if i < len(self.points) - 1 else 0][0] for i in range(len(self.points))) / 2)

	def rotate(self, (x, y), ang=math.pi / 4):
		self.points = [(x + (p[0] - x) * math.cos(ang) - (p[1] - y) * math.sin(ang),
		                y + (p[0] - x) * math.sin(ang) + (p[1] - y) * math.cos(ang)) for p in self.points]

	def setPos(self, pos):
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


class AABB:
	top = float('-inf')
	bottom = float('inf')
	left = float('inf')
	right = float('-inf')

	def __init__(self, s):
		if isinstance(s, Circle):
			self.top = s.y + s.radius
			self.bottom = s.y - s.radius
			self.left = s.x - s.radius
			self.right = s.x + s.radius
		else:
			for p in s.points:
				self.left = p[0] if p[0] < self.left else self.left
				self.right = p[0] if p[0] > self.right else self.right
				self.top = p[1] if p[1] > self.top else self.top
				self.bottom = p[1] if p[1] < self.bottom else self.bottom

	def intersect(self, other):
		return not (
			self.bottom > other.top or self.top < other.bottom or self.left > other.right or self.right < other.left)
