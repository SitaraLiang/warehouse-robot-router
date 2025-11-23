import numpy as np
from queue import Queue
import os
from icecream import ic

DIRS = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1)
}

ROT_RIGHT = {
    'N': 'E',
    'E': 'S',
    'S': 'W',
    'W': 'N'
}

ROT_LEFT = {
    'N': 'W',
    'W': 'S',
    'S': 'E',
    'E': 'N'
}

def get_grid(txt_file):
	#Retourne une liste de grilles, les grilles pour l'instant c'est un tuple avec la grille et les deux points de départ et d'arrivée, c'est dégueu mais bon
	script_dir = os.path.dirname(os.path.abspath(__file__))
	file_path = os.path.join(script_dir, txt_file)

	with open(file_path, mode='r') as txt:
		
		#Orientation selon les aiguilles d'une montre, complètement arbitraire ptdr
		orientation_map = {
        "nord":  'N',
        "est":   'E',
        "sud":   'S',
        "ouest": 'W'
        }
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
			debut = (int(infos[0]), int(infos[1]), orientation_map[infos[4].strip('\n')])
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
				if grid[i-1][y] == 1:
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
				if grid[x-1][j] == 1:
					return False
				if grid[x-1][j-1] == 1:
					return False
			if grid[x][j] == 1:
				return False
		return True

def get_neighbors(grid, state):
	#Retourne une liste de voisins, on sait qu'un état peut avoir 5 voisins en théorie mais parfois il y a un obstacle qui bloque, ou alors un voisin qui n'existe pas
	#ic(state)
	neighbors = []
	i, j, d = state
	n = len(grid)
	m = len(grid[0])
	neighbors.append((i, j, ROT_RIGHT[d]))
	neighbors.append((i, j, ROT_LEFT[d]))
	di, dj = DIRS[d]
	
	for k in range(1,4):
		ni = i + k * di
		nj = j + k * dj
		
		if not (0 <= ni < n and 0 <= nj < m):
		    continue
		
		if clear_path(grid, i, j, ni, nj):
		   	neighbors.append((ni, nj, d))
	#ic(neighbors)
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
                    ic(neigh, end)
                    path = [neigh]
                    k = neigh
                    while k != start:
                        k = prev[k]
                        path.append(k)
                    path.reverse()
                    return path
    return []

def path_to_commands(path):
    """
    D: turn right
    G: turn left
    aN: advance N cells
    """
    if len(path) < 2:
        return []
    commands = []
    ROT_RIGHT = {'N':'E','E':'S','S':'W','W':'N'}
    ROT_LEFT  = {'N':'W','W':'S','S':'E','E':'N'}

    for k in range(1, len(path)):
        (i1, j1, d1) = path[k-1]
        (i2, j2, d2) = path[k]
        if d2 != d1:
            if ROT_RIGHT[d1] == d2:
                commands.append("D")
            elif ROT_LEFT[d1] == d2:
                commands.append("G")
        dist = abs(i2 - i1) + abs(j2 - j1)
        if dist > 0:
            commands.append(f"a{dist}")

    return commands


	
grille = get_grid('../res/grille.txt')
#print(grille[0][0])
i, j, d = grille[0][1]
depart = (i, j, d)
#ic(depart)
i2, j2, d2 = grille[0][2]
fin = (i2, j2, d2)
#ic(fin)
#k = get_neighbors(grille[0][0], depart)
t = get_shortest_path(grille[0][0], depart, fin)
print(t)
commands = path_to_commands(t)
print(commands)
print(len(commands))
#print(grille[0][1], k)

	
	
