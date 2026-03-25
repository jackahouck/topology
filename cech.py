import numpy as np
import miniball
from itertools import combinations
from sampling import place_holes, sample_points


def cech_complex(points, r):
    N = len(points)

    def is_simplex(indices):
        pts = np.array([points[i] for i in indices], dtype=float)
        _, r_squared = miniball.get_bounding_ball(pts)
        return np.sqrt(r_squared) <= r

    complex = {0: [], 1: [], 2: [], 3: []}

    # Vertices 
    complex[0] = list(combinations(range(N), 1))

    # Edges, triangles, tetrahedra
    for dim in range(1, 4):
        for simplex in combinations(range(N), dim + 1):
            if is_simplex(simplex):
                complex[dim].append(simplex)

    return complex


if __name__ == "__main__":
    hole_centers = place_holes(N=5, R=0.1)
    points = sample_points(M=50, hole_centers=hole_centers, R=0.1)
    r = 0.3

    cech = cech_complex(points, r)

    for dim, simplices in cech.items():
        print(f"Dimension {dim}: {len(simplices)} simplices")
        for s in simplices:
            print(f"  {s}")