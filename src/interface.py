from generate_obstacles import *
from BFS import *

def interface_terminal():

    print("=== Génération de grille avec obstacles ===")

    M = int(input("Nombre de lignes M : "))
    N = int(input("Nombre de colonnes N : "))
    P = int(input("Nombre d'obstacles P : "))

    obstacles = generate_obstacles(M, N, P)

    grid = [[0 for _ in range(N)] for _ in range(M)]
    for (i, j) in obstacles:
        grid[i][j] = 1

    print("\nGrille générée :")
    for row in grid:
        print(row)

    while True:
        print("\n=== Position de départ ===")
        i_d = int(input("i départ : "))
        j_d = int(input("j départ : "))
        d = input("direction (N/S/W/E) : ").strip().upper()

        if d not in ("N", "S", "W", "E"):
            print("Direction invalide.")
            continue

        if 0 <= i_d < M and 0 <= j_d < N and grid[i_d][j_d] == 0 and grid[i_d-1][j_d] == 0 and grid[i_d][j_d-1] == 0 and grid[i_d-1][j_d-1] == 0:
            break
        else:
            print("Position départ invalide : un obstacle est présent.")

    while True:
        print("\n=== Position d'arrivée ===")
        i_f = int(input("i arrivée : "))
        j_f = int(input("j arrivée : "))

        if 0 <= i_f < M and 0 <= j_f < N and grid[i_f][j_f] == 0:
            if grid[i_f][j_f] == 0 and grid[i_f-1][j_f] == 0 and grid[i_f][j_f-1] == 0 and grid[i_f-1][j_f-1] == 0 and not(i_f == i_d and j_f == j_d):
                break
            else:
                print("La position d’arrivée doit être différente du départ.")
        else:
            print("Position arrivée invalide : un obstacle est présent.")

    print("\nCalcul du plus court chemin...")
    path = get_shortest_path(grid, start=(i_d, j_d, d),end=(i_f, j_f, -1))

    if path is None:
        print("Aucun chemin trouvé.")
        return

    print(path)
    commands = path_to_commands(path)
    print("\n=== Commandes générées ===")
    print(" ".join(commands))


if __name__ == "__main__":
    interface_terminal()