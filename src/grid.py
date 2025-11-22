import numpy as np
from queue import Queue

def get_grid(txt_file):
	#Retourne une liste de grilles, les grilles pour l'instant c'est un tuple avec la grille et les deux points de départ et d'arrivée, c'est dégueu mais bon

	with open(txt_file, mode='r') as txt:
		
		#Orientation selon les aiguilles d'une montre, complètement arbitraire ptdr
		orts = {'nord': 0, 'sud': 2, 'est': 1, 'ouest': 3}
		grids = []
		
		lines = txt.readlines()
		cpt = 0
		while cpt < len(lines):
			i, j = lines[cpt].split(' ')
			grid = []
			#cpt +1 pour passer la taille de la grille
			for l in range(cpt+1, cpt+int(i)+1):
				line = lines[l].strip('\n').split(' ')
				line = [int(x) for x in line]
				grid.append(line)
			
			infos = lines[cpt+int(i)+1].split(' ')
			debut = (int(infos[0]), int(infos[1]), orts[infos[4].strip('\n')])
			fin = (int(infos[2]), int(infos[3]), -1)
			
			grids.append([grid, debut, fin])
			#Pour aller au bloc suivant, on ajoute i+4 (toutes les lignes du bloc précédant + 1 ligne d'espace) à cpt
			cpt += int(i) + 4
			
		return grids

def clear_path(grid, i, j, ni, nj):
	#Vérifie si on peut aller d'une case à l'autre

	if i == ni:
		step = 1 if nj > j else -1
		for y in range(j+step, nj+step, step):
			if i < len(grid) - 1:
				if grid[i+1][y] == 1:
					return False
			if grid[i][y] == 1:
				return False
		return True
	
	if j == nj:
		step = 1 if ni > i else -1
		for x in range(i+step, ni+step, step):
			if j > 0:
				if grid[x][j-1] == 1:
					return False
			if grid[x][j] == 1:
				return False
		return True

def get_neighbors(grid, state):
	#Retourne une liste de voisins, on sait qu'un état peut avoir 5 voisins en théorie mais parfois il y a un obstacle qui bloque, ou alors un voisin qui n'existe pas
	
	neighbors = []
	i, j, d = state
	n = len(grid)
	m = len(grid[0])
	orientations = {0: (-1, 0),
					1: (0, 1),
					2: (1, 0),
					3: (0, -1)
					}
	#print(grid.shape)
	i1, j1 = orientations[d]
	
	neighbors.append((i, j, (d+1)%4))
	neighbors.append((i, j, (d-1)%4))
	
	for k in range(1,4):
		ni = i + k * i1
		nj = j + k * j1

		if not (0 <= ni < n and 0 <= nj < m):
		    continue
		
		if clear_path(grid, i, j, ni, nj):
		   	neighbors.append((ni, nj, d))
	
	return neighbors
		
def get_shortest_path(grid, start, end):
	#Retourne le chemin le plus court, en utilisant un BFS

    q = Queue()
    q.put(start)
    visited = dict()
    visited[start] = True
    prev = dict()

    while not q.empty():
        curr = q.get()
        neighbors = get_neighbors(grid, curr)

        for neigh in neighbors:
            if neigh not in visited:
                q.put(neigh)
                visited[neigh] = True
                prev[neigh] = curr
                if neigh[0] == end[0] and neigh[1] == end[1]:
                    path = [neigh]
                    k = neigh
                    while k != start:
                        k = prev[k]
                        path.append(k)
                    path.reverse()
                    return path
    return []
	
grille = get_grid('../res/grille.txt')
print(grille[0][0])
i, j, d = grille[0][1]
depart = (i-1, j, d)
i2, j2, d2 = grille[0][2]
fin = (i2 -1, j2, d2)
print(fin)
k = get_neighbors(grille[0][0], depart)
t = get_shortest_path(grille[0][0], depart, fin)
print(t)
print(len(t))
#print(grille[0][1], k)

	
	
