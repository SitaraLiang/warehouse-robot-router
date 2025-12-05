# Projet de MOGPL Sorbonne M1


Ce projet permet :

* de **générer automatiquement une grille** contenant un nombre donné d’obstacles,
* de l'utilisateur choisir le point de départ et d'arrivée,
* de **résoudre un modèle linéaire avec Gurobi** pour déterminer la meilleure position d’obstacles selon des contraintes structurelles,
* de calculer le **plus court chemin** entre ces deux points à l’aide d’un algorithme BFS adapté à un robot orienté.

## Dépendances

* Python 3
* `gurobipy`
* `collections`
* `sortedcontainers`

## Set up

```bash
pip install -r requirements.txt
```


## Utilisation

### Interface graphique
Pour lancer l'interface :
```bash
python src/interface.py
```

### Évaluation

Pour lancer les tests de performance :

```bash
python src/evaluation.py --mode <size|obstacles>
```

* `size` : teste la performance du BFS en fonction de la taille des grilles.
* `obstacles` : teste la performance en fonction du nombre d'obstacles.

  * Optionnel : vous pouvez préciser les fichiers à utiliser pour les tests d'obstacles avec `--file_size` et `--file_obs` (par défaut `test_run_size.txt` et `test_run_obs.txt`).

## Structure du code

#### `generate_obstacles(M, N, P)`

* Génère un poids aléatoire pour chaque case de la grille.
* Formule et résout un **programme linéaire** avec Gurobi.
* Contraintes respectées :

  * max. `2P/M` obstacles par ligne,
  * max. `2P/N` obstacles par colonne,
  * interdiction du motif `101` horizontal ou vertical.
* Retourne la liste des coordonnées d’obstacles.


#### `get_shortest_path(grid, start, end)`

* Version adaptée d’un BFS classique.
* États représentés comme `(i, j, direction)` et `(i, j, -1)` pour le point d'arrivée
* Transitions possibles :

  * avancer,
  * tourner gauche,
  * tourner droite.
* Renvoie le chemin sous forme de liste de états (i, j, d).


#### `path_to_commands(path)`

* Convertit un chemin en liste de commandes robot :
  `A` (avancer), `G` (tourner à gauche), `D` (tourner à droite)
* Reconstruit les transitions à partir des orientations successives.


#### `interface_terminal()`

Interface interactive guidant l’utilisateur :

1. Saisie de **M, N, P**
2. Génération des obstacles via Gurobi
3. Création de la grille et affichage
4. Saisie du **point de départ** et de l’orientation initiale
5. Saisie du **point d’arrivée**
6. Vérification que départ et arrivée ne sont pas sur des obstacles
7. Calcul du plus court chemin
8. Conversion du chemin en commandes
9. Affichage des commandes finales

