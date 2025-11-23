import time
from statistics import mean
from generate_grid import *
from BFS import *
from pathlib import Path
import matplotlib.pyplot as plt

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

def save_instances_to_file(N, grids, starts, ends):
    """ Save the 10 generated grids for size N x N with N obstacles into one file: instances_N.txt """
    filename = OUTPUT_DIR / f"instances_{N}.txt"
    with open(filename, "w") as f:
        for i in range(10):
            grid = grids[i]
            start = starts[i]
            end = ends[i]
            f.write(f"{len(grid)} {len(grid[0])}\n")
            for row in grid:
                f.write(" ".join(map(str, row)) + "\n")
            si, sj, sd = start
            ei, ej, _ = end
            f.write(f"{si} {sj} {ei} {ej} {sd}\n")
            f.write("\n")

def save_results_for_size(N, starts, ends, commands_list):
    """ Save the 10 result commands for grid size N x N into results_N.txt """
    filename = OUTPUT_DIR / f"results_{N}.txt"
    with open(filename, "w") as f:
        for i in range(10):
            si, sj, sd = starts[i]
            ei, ej, _ = ends[i]
            commands = commands_list[i]

            f.write(f"START: {si} {sj} ORIENT: {sd}\n")
            f.write(f"END:   {ei} {ej}\n")

            f.write(f"{len(commands)} " + " ".join(commands) + "\n")
            f.write("\n")

def run_experiments():
    sizes = [10, 20, 30, 40, 50]
    results = {}

    for N in sizes:
        print(f"--- Test N={N} ---")
        grids = []
        starts = []
        ends = []
        commands_all = []
        times = []
        for _ in range(10):
            # generate grid
            grid, start, end = generate_random_grid(N)
            grids.append(grid)
            starts.append(start)
            ends.append(end)
            # timer
            t0 = time.perf_counter()
            path = get_shortest_path(grid, start, end)
            commands = path_to_commands(path)
            t1 = time.perf_counter()
            # store results for each instance
            commands_all.append(commands)
            times.append(t1 - t0)

        # store grid & results
        save_instances_to_file(N, grids, starts, ends)
        save_results_for_size(N, starts, ends, commands_all)

        results[N] = {
            "commands": commands_all,
            "times": times
        }

    return results


if __name__ == "__main__":
    results = run_experiments()

    print("\n--- Average times ---")
    for N in sorted(results.keys()):
        avg = mean(results[N]["times"])
        print(f"N={N} → average time = {avg:.6f} s")

    sizes = [10, 20, 30, 40, 50]
    avg_times = [mean(results[N]["times"]) for N in sizes]

    plt.plot(sizes, avg_times, marker='o')
    plt.xlabel("Size of grid N x N")
    plt.ylabel("Average Time (s)")
    plt.title("Average Time for BFS vs Grid Size")
    plt.grid(True)
    plt.show()
