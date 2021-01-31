import math
import random
from matplotlib import pyplot as plt
# Koristi se ova klasa kada su date koordinate cvorova
class Edge:
	def __init__(self, a, b):
		self.a = a
		self.b = b
		self.pheromone = 1.0
		self.length = math.sqrt((a[0]-b[0]) ** 2.0 + (a[1]-b[1]) ** 2.0)
# Ova klasa se koristi kada je data matrica rastojanja
class Edge1:
	def __init__(self, l):
		self.pheromone = 1.0
		self.length = l

class Ant:
	def __init__(self, num_nodes, edges):
		self.num_nodes = num_nodes
		self.edges = edges
		self.alpha = 2.0
		self.beta = 6.0
		self.tour = None
		self.distance = 0.0
		self.find_tour()
	# Verovatnoca da ce se cvor n izabrati
	def _probability(self, n):
		return pow(self.edges[self.tour[-1]][n].pheromone, self.alpha)*pow((self.edges[self.tour[-1]][n].length), -self.beta)
	# Pronadji sledici cvor sistemom ruleta
	def _select_node(self):
		unvisited_nodes = [node for node in range(self.num_nodes) if node not in self.tour]
		total_sum = sum([self._probability(n) for n in unvisited_nodes])
		random_value = random.uniform(0.0, total_sum)
		current_sum = 0.0
		for unvisited_node in unvisited_nodes:
			current_sum += self._probability(unvisited_node)
			if current_sum >= random_value:
				return unvisited_node
	# Pronadji putanju i duzinu te putanje
	def find_tour(self):
		self.tour = [random.randint(0, self.num_nodes - 1)]
		while len(self.tour) < self.num_nodes:
			self.tour.append(self._select_node())
		self.distance = sum([self.edges[self.tour[i]][self.tour[(i + 1) % self.num_nodes]].length for i in range(self.num_nodes)])

class TSP:
	def __init__(self, colony_size, generations, nodes):
		self.colony_size = colony_size
		self.generations = generations
		self.nodes = nodes
		self.num_nodes = len(nodes)
		self.rho = 0.005
		self.Q = 100.0
		self.edges = [[Edge(nodes[i], nodes[j]) for i in range(self.num_nodes)] for j in range(self.num_nodes)]
		#self.edges = [[Edge1(nodes[i][j]) for i in range(self.num_nodes)] for j in range(self.num_nodes)]
		self.colony = [Ant(self.num_nodes, self.edges) for _ in range(self.colony_size)]
		self.best_tour = None
		self.best_distance = float("inf")

	def solve(self):
		for step in range(self.generations):
			best_iter = float("inf")
			for ant in self.colony:
				# Nadji putanju za mrava
				ant.find_tour()
				d = ant.distance
				if d < best_iter:
					best_iter = d
				# Dodaj feromone na putanju kojom se mrav kretao
				for i in range(self.num_nodes):
					self.edges[ant.tour[i]][ant.tour[(i + 1) % self.num_nodes]].pheromone += self.Q / ant.distance
				# Ispis ako je pronadjena bolja putanja
				if ant.distance < self.best_distance:
					self.best_tour = ant.tour
					self.best_distance = ant.distance
					print('Generation: ' + str(step))
					print('Best distance: ' + str(self.best_distance))
					print()
			print(best_iter)
			# Elitizam - dodaj feromone na najbolju putanju
			for i in range(self.num_nodes):
				self.edges[self.best_tour[i]][self.best_tour[(i + 1) % self.num_nodes]].pheromone += self.Q / self.best_distance
			# Isparavanje - na svakoj ivici smanji broj feromona
			for i in range(self.num_nodes):
				for j in range(i + 1, self.num_nodes):
					self.edges[i][j].pheromone *= (1.0 - self.rho)
			#if step % 10 == 0:
				#print('Generation: ' + str(step))
				#print('Best distance: ' + str(self.best_distance))
		print('Best distance overall: ' + str(self.best_distance))

	def plot(self, line_width=1, point_radius=math.sqrt(2.0)):
		x = [self.nodes[i][0] for i in self.best_tour]
		x.append(x[0])
		y = [self.nodes[i][1] for i in self.best_tour]
		y.append(y[0])
		plt.plot(x, y, linewidth=line_width)
		plt.scatter(x, y, s=math.pi * (point_radius ** 2.0))
		plt.show()

colony_size = 10
generations = 1000
nodes = []
f = open("KroA100", "r", newline='')
lines = f.readlines()
for l in lines:
	s = [float(x) for x in l.split(" ")]
	nodes.append(s)
tsp = TSP(colony_size, generations, nodes)
tsp.solve()
tsp.plot()
