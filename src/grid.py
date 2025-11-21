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
		
def get_neighbors(grid, state):
	#Retourne une liste de voisins, on sait qu'un état peut avoir 5 voisins en théorie mais parfois il y a un obstacle qui bloque, ou alors un voisin qui n'existe pas
	
	neighbors = []
	i, j, d = state
	orientations = {0: (-1, 0),
					1: (0, 1),
					2: (1, 0),
					3: (0, -1)
					}
	
	i1, j1 = orientations[d]
	for k in range(1,4):
		#A FAIRE vérifier si on est encore dans la grille avant d'ajouter le voisin
		neighbors.append((i + k * i1, j + k * j1, d))
		
	neighbors.append((i, j, (d+1)%4))
	neighbors.append((i, j, (d-1)%4))
	
	
	
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
        neighbors = get_neighbors(grid, *curr)

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
k = get_neighbors(grille[0][0], grille[0][1])
print(grille[0][1], k)

	
	