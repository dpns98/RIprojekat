import numpy as np
import math
import more_itertools
from matplotlib import pyplot as plt

nodes = []
f = open("10gradova", "r", newline='')
lines = f.readlines()
for l in lines:
	s = [float(x) for x in l.split(" ")]
	nodes.append(s)

edges = [[math.sqrt((nodes[i][0]-nodes[j][0]) ** 2.0 + (nodes[i][1]-nodes[j][1]) ** 2.0) for i in range(len(nodes))] for j in range(len(nodes))]

edges = np.array(edges)
n = len(nodes)
best = float('inf')
i = ()

for p in more_itertools.distinct_permutations(range(n)):
	s = sum([edges[p[i]][p[(i + 1) % n]] for i in range(n)])
	if s < best:
		best = s
		i = p
		print(best)
		print(p)

print("najbolji rezultat")
print(best)

x = [nodes[j][0] for j in i]
x.append(x[0])
y = [nodes[j][1] for j in i]
y.append(y[0])
plt.plot(x, y, linewidth=1)
plt.scatter(x, y, s=math.pi * (math.sqrt(2.0) ** 2.0))
plt.show()
