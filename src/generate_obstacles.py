#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 11:20:36 2025

@author: 21500112
"""

from gurobipy import *
import numpy as np


def generate_obstacles(M, N, P):
    
    # Tire aléatoirement un poids entier entre 0 et 1000 pour chaque case
    poids = np.random.randint(0, 1001, size=(M, N))
    
    m = Model("mogplex")
    
    # declaration variables de decision
    x = {}
    for i in range(M):
        for j in range(N):
            x[i,j] = m.addVar(vtype=GRB.BINARY, name="x_{i}_{j}")
        
    # maj du modele pour integrer les nouvelles variables
    m.update()
    
    # definition de l'objectif
    obj = quicksum(poids[i][j] * x[i,j] for i in range(M) for j in range(N))
    m.setObjective(obj, GRB.MINIMIZE)
    
    # Contrainte 1: Nombre total d'obstacles égale à P
    m.addConstr(quicksum(x[i,j] for i in range(M) for j in range(N)) == P)
    
    # Contrainte 2: Chaque ligne de la grille ne peut contenir plus de 2P/M obstacles
    for i in range(M):
        m.addConstr(quicksum(x[i,j] for j in range(N)) <= 2*P/M)
        # Contrainte 4: Aucune ligne ne peut contenir la s´equence 101 
        for j in range(1, N-1):
            m.addConstr(x[i,j-1] + x[i,j+1] - x[i,j] <= 1)
            
    # Contrainte 3: Chaque colonne de la grille ne peut contenir plus de 2P/N obstacles
    for j in range(N):
        m.addConstr(quicksum(x[i,j] for i in range(M)) <= 2*P/N)
        # Contrainte 5: Aucune colonne ne peut contenir la s´equence 101
        for i in range(1, M-1):
            m.addConstr(x[i-1,j] + x[i+1,j] - x[i,j] <= 1)
        
    
    # Resolution
    m.optimize()
    
    # .X – primal solution value
    obstacles = [(i, j) for (i, j), var in x.items() if var.X == 1]
    return obstacles


M, N, P = 9, 10, 10
obstacles = generate_obstacles(M, N, P)
print(f"Coordonates des obstacles:\n{obstacles}")
grille = np.zeros((M, N), dtype=int)
for i, j in obstacles:
    grille[i][j] = 1
    
print(grille)

"""
Coordonates des obstacles:
[(0, 2), (0, 3), (2, 1), (2, 4), (3, 4), (3, 8), (4, 3), (6, 6), (8, 0), (8, 9)]
[[0 0 1 1 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0]
 [0 1 0 0 1 0 0 0 0 0]
 [0 0 0 0 1 0 0 0 1 0]
 [0 0 0 1 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 1 0 0 0]
 [0 0 0 0 0 0 0 0 0 0]
 [1 0 0 0 0 0 0 0 0 1]]
"""

        
        