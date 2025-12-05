import time
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

"""
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
    
def run_experiments2_TEST(file_size, file_obs):

    generer_grilles_test(file_size, file_obs)
    grids_obs = get_grid(file_obs)

    res_obs = []

    with open(OUTPUT_DIR / f'result_{file_obs}', mode='w') as fobs:
        i = 0
        cpt = 0
        for grid in grids_obs:
            t0 = time.perf_counter()
            path = get_shortest_path(*grid)
            commands = path_to_commands(path)
            t1 = time.perf_counter()

            if i == 99:
                cpt += (t1 - t0)
                res_obs.append(cpt / 100)
                i = 0
                cpt = 0
            else:
                i += 1

            fobs.write(f'{len(commands)} {commands}\n\n')

    return res_obs

"""

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

        for _ in range(100):
            grid, start, end = generate_random_grid(N)
            grids.append(grid)
            starts.append(start)
            ends.append(end)

            t0 = time.perf_counter()
            path = get_shortest_path(grid, start, end)
            commands = path_to_commands(path)
            t1 = time.perf_counter()

            commands_all.append(commands)
            times.append(t1 - t0)  # time per grid

        save_instances_to_file(N, grids, starts, ends)
        save_results_for_size(N, starts, ends, commands_all)

        results[N] = {"commands": commands_all, "times": times}

    return results


def run_experiments2_TEST(file_size, file_obs):
    """Obstacle test: measures BFS time per grid individually."""

    generer_grilles_test(file_size, file_obs)
    grids_obs = get_grid(file_obs)

    times_per_grid = []

    with open(OUTPUT_DIR / f'result_{file_obs}', mode='w') as fobs:
        for grid in grids_obs:
            t0 = time.perf_counter()
            path = get_shortest_path(*grid)
            commands = path_to_commands(path)
            t1 = time.perf_counter()

            grid_time = t1 - t0
            times_per_grid.append(grid_time)

            fobs.write(f'{len(commands)} {commands}\n\n')

    return times_per_grid



def run(mode, file_size=None, file_obs=None):

    if mode == "size":
        return run_experiments()

    elif mode == "obstacles":
        if file_size is None or file_obs is None:
            raise ValueError("file_size and file_obs are required in 'obstacles' mode'")
        return run_experiments2_TEST(file_size, file_obs)

    else:
        raise ValueError("Mode must be 'size' or 'obstacles'")


    
import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run BFS evaluations.")
    
    parser.add_argument(
        "--mode",
        choices=["size", "obstacles"],
        required=True,
        help="Choose evaluation mode: 'size' or 'obstacles'"
    )

    parser.add_argument(
        "--file_size",
        type=str,
        default="test_run_size.txt",
        help="Only needed because generer_grilles_test requires both files"
    )

    parser.add_argument(
        "--file_obs",
        type=str,
        default="test_run_obs.txt",
        help="Grid file used for obstacles evaluation"
    )

    args = parser.parse_args()

    results = run(
        mode=args.mode,
        file_size=args.file_size,
        file_obs=args.file_obs
    )

    # ------------------------------------------------------------
    # SIZE MODE PLOT
    # ------------------------------------------------------------
    if args.mode == "size":
        sizes = sorted(results.keys())
        avg_times_per_size = [sum(results[N]["times"]) / len(results[N]["times"]) for N in sizes]

        plt.figure(figsize=(10, 6))
        plt.plot(sizes, avg_times_per_size, marker='o', label="Average BFS time")
        plt.xlabel("Grid size N x N")
        plt.ylabel("BFS time (s)")
        plt.title("BFS Performance vs Grid Size")
        plt.grid(True)
        plt.ticklabel_format(style='plain', axis='y')  # disable scientific notation
        plt.legend()
        plt.savefig(OUTPUT_DIR / "plot_size_mode.png")
        plt.show()

        print("Plot saved: outputs/plot_size_mode.png")


    # ------------------------------------------------------------
    # OBSTACLES MODE PLOT
    # ------------------------------------------------------------
    if args.mode == "obstacles":
        times_per_grid = results  # list of per-grid times
        num_obstacles = [sum(sum(row) for row in grid) for grid, *_ in get_grid(args.file_obs)]
        
        avg_time = sum(times_per_grid) / len(times_per_grid)

        plt.figure(figsize=(12, 6))
        plt.scatter(num_obstacles, times_per_grid, label="Per-grid BFS time", color="blue")
        plt.axhline(avg_time, color='red', linestyle='--', linewidth=2, label=f"Mean = {avg_time:.6f}")
        plt.xlabel("Number of obstacles")
        plt.ylabel("BFS time (s)")
        plt.title("BFS Performance vs Number of Obstacles for Grid Size 20x20")
        plt.ticklabel_format(style='plain', axis='y')
        plt.grid(True)
        plt.legend()
        plt.savefig(OUTPUT_DIR / "plot_obstacles_mode.png")
        plt.show()

        print("Plot saved: outputs/plot_obstacles_mode.png")

    print("Evaluation finished.")