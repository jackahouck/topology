import numpy as np
import miniball
from itertools import combinations
from sampling import place_holes, sample_points


def cech_complex(points, r):
    N = len(points)

    complex = {0: [], 1: [], 2: [], 3: []}

    # Vertices
    complex[0] = list(combinations(range(N), 1))

    for simplex in combinations(range(N), 2):
        pts = np.array([points[i] for i in simplex], dtype=float)
        _, r_squared = miniball.get_bounding_ball(pts)
        if np.sqrt(r_squared) <= r:
            complex[1].append(simplex)

    edge_set = set(complex[1])

    for dim in range(2, 4):
        for simplex in combinations(range(N), dim + 1):
            # early exit: all pairs must be edges
            if any((i, j) not in edge_set for i, j in combinations(simplex, 2)):
                continue
            pts = np.array([points[i] for i in simplex], dtype=float)
            _, r_squared = miniball.get_bounding_ball(pts)
            if np.sqrt(r_squared) <= r:
                complex[dim].append(simplex)

    return complex

if __name__ == "__main__":
    holes = place_holes(N=5, R=0.1)
    points = sample_points(M=50, holes=holes)
    r = 0.3

    cech = cech_complex(points, r)

    for dim, simplices in cech.items():
        print(f"Dimension {dim}: {len(simplices)} simplices")
        for s in simplices:
            print(f"  {s}")