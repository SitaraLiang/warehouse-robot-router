import random

def generate_random_grid(N):
    """
    Generate a random grid of size N x N with N obstacles and positions 
    de départ et d'arrivée valides
    """
    # shape: N x N
    grid = [[0]*N for _ in range(N)]
    
    # placer N obstacle aléatoirement
    count = 0
    while count < N:
        i = random.randint(0, N-1)
        j = random.randint(0, N-1)
        if grid[i][j] == 0:
            grid[i][j] = 1
            count += 1

    # positions départ / arrivée (ne doivent pas être des obstacles)
    while True:
        i_d, j_d = random.randint(0,N-1), random.randint(0,N-1)
        if grid[i_d][j_d] == 0 and grid[i_d-1][j_d] == 0 and grid[i_d][j_d-1] == 0 and grid[i_d-1][j_d-1] == 0:
            break
    while True:
        i_f, j_f = random.randint(0,N-1), random.randint(0,N-1)
        if grid[i_f][j_f] == 0 and grid[i_f-1][j_f] == 0 and grid[i_f][j_f-1] == 0 and grid[i_f-1][j_f-1] == 0 and (i_f != i_d or j_f != j_d):
            break

    # orientation du départ aleatoire
    orientations = ["nord", "est", "sud", "ouest"]
    orientation_map = {
        "nord":  'N',
        "est":   'E',
        "sud":   'S',
        "ouest": 'W'
        }
    d = random.choice(orientations)
    orientation = orientation_map[d]

    return grid, (i_d, j_d, orientation), (i_f, j_f, -1)


def save_grid_to_file(filename, grid, start, end):
    N = len(grid)

    with open(filename, "w") as f:
        f.write(f"{N} {N}\n")

        for row in grid:
            f.write(" ".join(str(x) for x in row) + "\n")

        i_d, j_d, o = start
        i_f, j_f, _ = end

        f.write(f"{i_d} {j_d} {i_f} {j_f} {o}\n")
        f.write("0 0\n")   # fin du bloc
