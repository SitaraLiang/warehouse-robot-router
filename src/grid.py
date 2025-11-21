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
				grid.append(line)
			
			infos = lines[cpt+int(i)+1].split(' ')
			debut = (int(infos[0]), int(infos[1]), orts[infos[4].strip('\n')])
			fin = (int(infos[2]), int(infos[3]), -1)
			
			grids.append([np.array(grid).astype(int), debut, fin])
			#Pour aller au bloc suivant, on ajoute i+4 (toutes les lignes du bloc précédant + 1 ligne d'espace) à cpt
			cpt += int(i) + 4
			
		return grids
		
def possible_mov(grid, state1, state2):
	#Retourne vrai si le déplacement est possible, faux sinon
	
	i1, j1 = state1[0], state1[1]
	i2, j2 = state2[0], state2[1]
	if i1 == i2:
		if j1 > j2:
			tmp = j1
			j1 = j2
			j2 = tmp
		if i1 == grid.shape[0] - 1:
			if grid[i1-1, j1+1:j2+1].sum() == 0: return True; return False
		else:
			if grid[i1-1, j1+1:j2+1].sum() == 0 and grid[i1+1, j1+1:j2+1].sum() == 0: return True; return False
	else:
		if i1 > i2:
			tmp = i1
			i1 = i2
			i2 = tmp
			if j1 == 0:
				if grid[i1+1:i2+1, j1].sum() == 0: return True; return False
			else:
				if grid[i1+1:i2+1, j1].sum() == 0 and grid[i1:i2+1, j1-1].sum() == 0: return True; return False
		
def get_neighbors(grid, state):
	#Retourne une liste de voisins, on sait qu'un état peut avoir 5 voisins en théorie mais parfois il y a un obstacle qui bloque, ou alors un voisin qui n'existe pas
	
	neighbors = []
	
	neighbors.append((state[0], state[1], (state[2] - 1)%4))
	neighbors.append((state[0], state[1], (state[2] + 1)%4))
	
	if state[2] % 2 == 0:
		if state[2] == 0:
			if state[0] > 0 and possible_mov(grid, state, (state[0] - 1, state[1], state[2])):
				neighbors.append((state[0] - 1, state[1], state[2]))
			if state[0] > 1 and possible_mov(grid, state, (state[0] - 2, state[1], state[2])):
				neighbors.append((state[0] - 2, state[1], state[2]))
		else:
			if state[0] < grid.shape[0] - 1 and possible_mov(grid, state, (state[0] + 1, state[1], state[2])):
				neighbors.append((state[0]+1, state[1], state[2]))
			if state[0] < grid.shape[0] - 2 and possible_mov(grid, state, (state[0] + 2, state[1], state[2])):
				neighbors.append((state[0] + 2, state[1], state[2]))
	else:
		if state[2] == 3:
			if state[1] > 0 and possible_mov(grid, state, (state[0], state[1] - 1, state[2])):
				neighbors.append((state[0], state[1] - 1, state[2]))
			if state[1] > 1 and possible_mov(grid, state, (state[0], state[1] - 2, state[2])):
				neighbors.append((state[0], state[1] - 2, state[2]))
		else:
			if state[1] < grid.shape[1] - 1 and possible_mov(grid, state, (state[0], state[1] + 1, state[2])):
				neighbors.append((state[0], state[1] + 1, state[2]))
			if state[1] < grid.shape[1] - 2 and possible_mov(grid, state , (state[0], state[1] + 2, state[2])):
				neighbors.append((state[0], state[1] + 2, state[2]))
			
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
#print(grille[0][0])
neighbors = get_neighbors(grille[0][0], grille[0][1])
print(grille[0][1])
print(neighbors)
#test = get_shortest_path(grille[0][0], grille[0][1], grille[0][2])
#print(grille[0][2])
#print(test)
#print(len(test))
#print(len(test))
	
	