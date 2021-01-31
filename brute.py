import numpy as np
import math
from python_tsp.exact import solve_tsp_dynamic_programming

nodes = []
f = open("oliver30", "r", newline='')
lines = f.readlines()
for l in lines:
	s = [float(x) for x in l.split(" ")]
	nodes.append(s)

edges = [[math.sqrt((nodes[i][0]-nodes[j][0]) ** 2.0 + (nodes[i][1]-nodes[j][1]) ** 2.0) for i in range(len(nodes))] for j in range(len(nodes))]

edges = np.array(edges)

permutation, distance = solve_tsp_dynamic_programming(edges)
print(distance)

# slozenost ovog algoritma za skup od 30 gradova je 2^30 * 30^2 sto znaci da bi se algoritam izvrsavao preko 3 sata
# za vece skupove nisam ni pokusavao brute force algoritam
